import math
import pandas as pd
from gurobipy import Model, GRB, quicksum


class ModeleDeterministe:

    def __init__(self, scenario):
        self.scenario = scenario
        print("scenario:", scenario)

        self.model = Model("Modele_1")

        # données
        self.demande_df = pd.read_excel("modele_deterministe/donnees.xlsx", sheet_name="demande")
        self.cout_rupture_df = pd.read_excel("modele_deterministe/donnees.xlsx", sheet_name="cout_rupture")
        self.stock_df = pd.read_excel("modele_deterministe/donnees.xlsx", sheet_name="stock")
        self.capacite_df = pd.read_excel("modele_deterministe/donnees.xlsx", sheet_name="capacite")

        self.initialiser_ensembles()
        self.initialiser_parametres()
        self.creer_variables()
        self.ajouter_contraintes()
        self.definir_objectif()


    # ENSEMBLES

    def initialiser_ensembles(self):
        self.I = self.demande_df["Succursales"].unique()
        self.K = self.demande_df["Machines"].unique()
        print("Succursales :", self.I)
        print("Machines :", self.K)

  
    # PARAMÈTRES

    def initialiser_parametres(self):

        # positions
        self.pos = {
            row["Succursales"]: (row["Position en X"], row["Position en Y"])
            for _, row in self.capacite_df.iterrows()
        }

        # demande de base
        d_base = {
            (row["Succursales"], row["Machines"]): row["Demande"]
            for _, row in self.demande_df.iterrows()
        }

        # scénario
        self.d = {}
        for (i, k), val in d_base.items():
            if self.scenario == 1:
                self.d[(i, k)] = val
            elif self.scenario == 2:
                self.d[(i, k)] = val * 1.3
            elif self.scenario == 3:
                self.d[(i, k)] = val * 1.5 if i in ["A", "B"] else val * 0.7

        # coût rupture
        self.p = {
            row["Type"]: row["Cout de rupture"]
            for _, row in self.cout_rupture_df.iterrows()
        }

        # stock
        self.s = {
            row["Type"]: row["Quantite"]
            for _, row in self.stock_df.iterrows()
        }

        # capacité
        self.cap = {
            row["Succursales"]: row["Capacite"]
            for _, row in self.capacite_df.iterrows()
        }

        # distances + coûts
        self.dist = {}
        self.c = {}

        for i in self.I:
            for j in self.I:
                xi, yi = self.pos[i]
                xj, yj = self.pos[j]
                self.dist[(i, j)] = math.sqrt((xi - xj) ** 2 + (yi - yj) ** 2)
                self.c[(i, j)] = self.dist[(i, j)] * 0.55


    # Variables
    def creer_variables(self):
        self.x = self.model.addVars(self.I, self.K, vtype=GRB.INTEGER, name="x")
        self.y = self.model.addVars(self.I, self.I, self.K, vtype=GRB.INTEGER, name="y")
        self.r = self.model.addVars(self.I, self.K, vtype=GRB.INTEGER, name="r")

    # Contraintes
    def ajouter_contraintes(self):

        # flux
        for i in self.I:
            for k in self.K:
                self.model.addConstr(
                    self.x[i, k]
                    + quicksum(self.y[j, i, k] for j in self.I if j != i)
                    - quicksum(self.y[i, j, k] for j in self.I if j != i)
                    + self.r[i, k]
                    >= self.d[(i, k)]
                )

        # limite envoi
        for i in self.I:
            for k in self.K:
                self.model.addConstr(
                    quicksum(self.y[i, j, k] for j in self.I if j != i) <= self.x[i, k]
                )

        # stock total
        for k in self.K:
            self.model.addConstr(
                quicksum(self.x[i, k] for i in self.I) <= self.s[k]
            )

        # capacité
        for i in self.I:
            self.model.addConstr(
                quicksum(self.x[i, k] for k in self.K) <= self.cap[i]
            )

        # pas de transfert vers soi-même
        for i in self.I:
            for k in self.K:
                self.model.addConstr(self.y[i, i, k] == 0)

    # objectif
    def definir_objectif(self):
        self.model.setObjective(
            quicksum(self.p[k] * self.r[i, k] for i in self.I for k in self.K)
            +
            quicksum(self.c[i, j] * self.y[i, j, k]
                     for i in self.I for j in self.I if i != j for k in self.K),
            GRB.MINIMIZE
        )

    # Résolution
    def resoudre(self):
        self.model.optimize()

    # Affichage
    def afficher_resultats(self):

        if self.model.status == GRB.OPTIMAL:
            print(f"\nRésultats scénario {self.scenario}\n")

            print("Répartition des équipements entre les succursales:\n")
            print(f"{'Succursale':<12}{'Machine':<25}{'Quantité'}")

            for i in self.I:
                for k in self.K:
                    if self.x[i, k].X > 0:
                        print(f"{i:<12}{k:<25}{int(self.x[i, k].X)}")

            print("\nRupture :")
            rupture_existe = False
            for i in self.I:
                for k in self.K:
                    if self.r[i, k].X > 0:
                        print(f"{i:<12}{k:<25}{int(self.r[i, k].X)}")
                        rupture_existe = True
            if not rupture_existe:
                print("Aucune rupture")

            print("\nTransferts :")
            transfert_existe = False
            for i in self.I:
                for j in self.I:
                    for k in self.K:
                        if i != j and self.y[i, j, k].X > 0:
                            print(f"{i} -> {j} ({k}) =", int(self.y[i, j, k].X))
                            transfert_existe = True
            if not transfert_existe:
                print("Aucun transfert")

        else:
            print("modèle infaisable")
            
if __name__ == "__main__":
    modele = ModeleDeterministe(scenario=3)
    modele.resoudre()
    modele.afficher_resultats()