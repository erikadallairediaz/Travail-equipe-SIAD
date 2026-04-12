import pandas as pd
 
 
class SolutionStochastique:
 
    def __init__(self, probleme, x, y, r, e, cout_total, statut="unknown"):
        self.probleme = probleme
        self.x = x
        self.y = y
        self.r = r
        self.e = e
        self.cout_total = cout_total
        self.statut = statut
 
    def validate(self):
        prob = self.probleme
        valide = True
 
        for k in prob.K:
            total = sum(self.x.get((i, k), 0) for i in prob.I)
            if total > prob.stock.get(k, 0) + 1e-6:
                print(f"Stock dépassé pour {k}: {total} > {prob.stock[k]}")
                valide = False
 
        for i in prob.I:
            total = sum(self.x.get((i, k), 0) for k in prob.K)
            if total > prob.capacite.get(i, 0) + 1e-6:
                print(f"Capacité dépassée pour {i}: {total} > {prob.capacite[i]}")
                valide = False
 
        return valide
 
    def evaluate(self):
        prob = self.probleme
        cout = 0.0
        for (i, j, k, s), val in self.y.items():
            cout += prob.prob[s] * prob.cout_transport.get((i, j), 0) * val
        for (i, k, s), val in self.r.items():
            cout += prob.prob[s] * prob.cout_rupture.get(k, 0) * val
        return cout
 
    def afficher(self):
        print(f"\nInstance : {self.probleme.instance_id}")
        print(f"Fonction objectif : {self.cout_total:.2f}")
 
        print("\nRépartition des équipements entre les succursales:")
        x_data = {(i, k): int(v) for (i, k), v in self.x.items() if v > 1e-6}
        df_x = pd.Series(x_data, name="x.val")
        df_x.index.names = ["succursale", "machine"]
        print(df_x.to_string())
 
        print("\nRuptures r :")
        r_data = {(i, k, s): int(v) for (i, k, s), v in self.r.items() if v > 1e-6}
        if r_data:
            df_r = pd.Series(r_data, name="r.val")
            df_r.index.names = ["succursale", "machine", "scenario"]
            print(df_r.to_string())
        else:
            print("Aucune rupture")
 
        print("\nTransferts y :")
        y_data = {(i, j, k, s): int(v) for (i, j, k, s), v in self.y.items() if v > 1e-6}
        if y_data:
            df_y = pd.Series(y_data, name="y.val")
            df_y.index.names = ["origine", "destination", "machine", "scenario"]
            print(df_y.to_string())
        else:
            print("Aucun transfert")
 
        print("\nSurplus e :")
        e_data = {(i, k, s): int(v) for (i, k, s), v in self.e.items() if v > 1e-6}
        if e_data:
            df_e = pd.Series(e_data, name="e.val")
            df_e.index.names = ["succursale", "machine", "scenario"]
            print(df_e.to_string())
        else:
            print("Aucun surplus")