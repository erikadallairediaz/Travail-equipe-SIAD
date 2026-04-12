from amplpy import AMPL

class ModeleStochastique:
    
    def __init__(self, fichier_mod, solveur="gurobi"):
        self.fichier_mod = fichier_mod
        self.solveur = solveur
        self.ampl = None
        self.cout_total = None
    
    def charger(self, fichier_data):
        self.ampl = AMPL()
        self.ampl.read(self.fichier_mod)
        self.ampl.read_data(fichier_data)
        self.ampl.set_option("solver", self.solveur)
    
    def resoudre(self):
        self.ampl.solve()
        self.cout_total = self.ampl.get_objective("CoutTotal").value()
    
    def get_resultats(self):
        return {
            "x": self.ampl.get_variable("x").get_values().to_pandas(),
            "r": self.ampl.get_variable("r").get_values().to_pandas(),
            "y": self.ampl.get_variable("y").get_values().to_pandas(),
            "e": self.ampl.get_variable("e").get_values().to_pandas()
        }