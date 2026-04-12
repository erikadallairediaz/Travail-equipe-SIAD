import unittest
from modele_deterministe import ModeleDeterministe

class TestModeleDeterministe(unittest.TestCase):

    def setUp(self):
        self.modele = ModeleDeterministe(scenario=1)
        self.modele.resoudre()

    def test_soliution_existe(self):
        self.assertEqual(self.modele.model.status, 2) #optimal

    def test_stock_respecte(self):
        for k in self.modele.K:
            total = sum(self.modele.x[i, k].X for i in self.modele.I)
            self.assertLessEqual(total, self.modele.s[k])

    def test_capacite_respectee(self):
        for i in self.modele.I:
            total = sum(self.modele.x[i, k].X for k in self.modele.K)
            self.assertLessEqual(total, self.modele.cap[i])

    def test_pas_de_transfert_vers_soi(self):
        for i in self.modele.I:
            for k in self.modele.K:
                self.assertEqual(self.modele.y[i, i, k].X, 0)

if __name__ == "__main__":
    unittest.main()

