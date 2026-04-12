import unittest
from probleme_stoch import ProblemeStochastique
from solution_stoch import SolutionStochastique
from solveur_stoch import SolveurStochastique
 
DOSSIER_CSV = "modele_heuristique"
MODELE = "modele_stochastique/modele_stochastique.mod"
 
 
class TestProblemeStochastique(unittest.TestCase):
 
    def setUp(self):
        self.prob = ProblemeStochastique(instance_id=1, dossier_csv=DOSSIER_CSV)
 
    def test_ensembles(self):
        self.assertEqual(len(self.prob.I), 4)
        self.assertEqual(len(self.prob.K), 3)
        self.assertEqual(len(self.prob.S), 3)
 
    def test_probabilites_somme(self):
        self.assertAlmostEqual(sum(self.prob.prob.values()), 1.0)
 
    def test_stock_positif(self):
        for k in self.prob.K:
            self.assertGreater(self.prob.stock[k], 0)
 
    def test_capacite_positive(self):
        for i in self.prob.I:
            self.assertGreater(self.prob.capacite[i], 0)
 
 
class TestSolutionStochastique(unittest.TestCase):
 
    def setUp(self):
        prob = ProblemeStochastique(instance_id=1, dossier_csv=DOSSIER_CSV)
        solveur = SolveurStochastique(modele_path=MODELE)
        self.sol = solveur.resoudre(prob)
 
    def test_validate(self):
        self.assertTrue(self.sol.validate())
 
    def test_evaluate_positif(self):
        self.assertGreater(self.sol.evaluate(), 0)
 
    def test_evaluate_egal_solveur(self):
        self.assertAlmostEqual(self.sol.evaluate(), self.sol.cout_total, places=2)
 
    def test_statut_optimal(self):
        self.assertEqual(self.sol.statut, "solved")
 
 
if __name__ == "__main__":
    unittest.main()