import csv
import os

I_LIST = ["A", "B", "C", "D"]
K_LIST = ["Chariot_elevateur", "Excavatrice", "Nacelle"]
S_LIST = ["faible", "moyen", "eleve"]


class ProblemeStochastique:

    def __init__(self, instance_id, dossier_csv="."):
        self.instance_id = instance_id
        self.dossier_csv = dossier_csv
        self.I = I_LIST
        self.K = K_LIST
        self.S = S_LIST
        self.prob = {}
        self.stock = {}
        self.capacite = {}
        self.cout_rupture = {}
        self.cout_transport = {}
        self.demande = {}
        self._charger()

    def _path(self, nom):
        return os.path.join(self.dossier_csv, nom)

    def _charger(self):
        self._lire_prob(self._path("prob.csv"))
        self._lire_stock(self._path("stock.csv"))
        self._lire_capacite(self._path("capacite.csv"))
        self._lire_cout_rupture(self._path("cout_rupture.csv"))
        self._lire_cout_transport(self._path("cout_transport.csv"))
        self._lire_demande(self._path("demande.csv"))

    def _lire_prob(self, fichier):
        with open(fichier, newline='', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f, delimiter=';'):
                self.prob[row["scenario"].strip()] = float(row["prob"])

    def _lire_stock(self, fichier):
        with open(fichier, newline='', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f, delimiter=';'):
                self.stock[row["machine"].strip()] = int(row["stock"])

    def _lire_capacite(self, fichier):
        with open(fichier, newline='', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f, delimiter=';'):
                self.capacite[row["succursale"].strip()] = int(row["capacite"])

    def _lire_cout_rupture(self, fichier):
        with open(fichier, newline='', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f, delimiter=';'):
                self.cout_rupture[row["machine"].strip()] = float(row["cout_rupture"])

    def _lire_cout_transport(self, fichier):
        with open(fichier, newline='', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f, delimiter=';'):
                i = row["origine"].strip()
                j = row["destination"].strip()
                self.cout_transport[(i, j)] = float(row["cout"])

    def _lire_demande(self, fichier):
        with open(fichier, newline='', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f, delimiter=';'):
                if int(row["instance"]) != self.instance_id:
                    continue
                i = row["succursale"].strip()
                k = row["machine"].strip()
                s = row["scenario"].strip()
                self.demande[(i, k, s)] = int(row["valeur"])
