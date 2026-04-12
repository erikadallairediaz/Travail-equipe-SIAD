from amplpy import AMPL
from probleme_stoch import ProblemeStochastique
from solution_stoch import SolutionStochastique
 
 
class SolveurStochastique:
 
    def __init__(self, modele_path, solveur_ampl="gurobi"):
        self.modele_path = modele_path
        self.solveur_ampl = solveur_ampl
 
    def resoudre(self, probleme):
        ampl = AMPL()
        ampl.read(self.modele_path)
        ampl.set_option("solver", self.solveur_ampl)
 
        ampl.get_set("I").set_values(probleme.I)
        ampl.get_set("K").set_values(probleme.K)
        ampl.get_set("S").set_values(probleme.S)
 
        ampl.param["prob"]           = probleme.prob
        ampl.param["stock"]          = probleme.stock
        ampl.param["cap"]            = probleme.capacite
        ampl.param["cout_rupture"]   = probleme.cout_rupture
        ampl.param["cout_transport"] = probleme.cout_transport
        ampl.param["demande"]        = probleme.demande
 
        ampl.solve()
 
        statut     = str(ampl.get_value("solve_result"))
        cout_total = ampl.get_objective("CoutTotal").value()
 
        x = self._extraire(ampl, "x")
        y = self._extraire(ampl, "y")
        r = self._extraire(ampl, "r")
        e = self._extraire(ampl, "e")
 
        return SolutionStochastique(probleme, x, y, r, e, cout_total, statut)
 
    def _extraire(self, ampl, nom):
        df = ampl.get_variable(nom).get_values().to_pandas()
        resultat = {}
        for idx, row in df.iterrows():
            cle = idx if isinstance(idx, tuple) else (idx,)
            resultat[cle] = int(round(row.iloc[0]))
        return resultat