import unittest

from probleme_heur import ProblemeHeur
from minizinc_solver import MiniZincSolver
from solution_heur import SolutionHeur


class TestProblemeHeur(unittest.TestCase):

    def setUp(self):
        self.prob = ProblemeHeur(creation_instance=1)

    def test_dimensions(self):
        self.assertEqual(self.prob.nI, 4)
        self.assertEqual(self.prob.nK, 3)
        self.assertEqual(self.prob.nS, 3)

    def test_creation_instance(self):
        self.assertEqual(self.prob.creation_instance, 1)

    def test_model_path_existe(self):
        self.assertIsInstance(self.prob.model_path, str)
        self.assertTrue(self.prob.model_path.endswith(".mzn"))

    def test_paths_csv(self):
        self.assertTrue(self.prob.prob_path.endswith(".csv"))
        self.assertTrue(self.prob.stock_path.endswith(".csv"))
        self.assertTrue(self.prob.capacite_path.endswith(".csv"))
        self.assertTrue(self.prob.cout_rupture_path.endswith(".csv"))
        self.assertTrue(self.prob.cout_transport_path.endswith(".csv"))
        self.assertTrue(self.prob.ordre_sources_path.endswith(".csv"))
        self.assertTrue(self.prob.demande_path.endswith(".csv"))


class TestSolutionHeur(unittest.TestCase):

    def setUp(self):
        prob = ProblemeHeur(creation_instance=1)
        solver = MiniZincSolver("coin-bc")
        self.sol = solver.solve(prob)

    def test_type_solution(self):
        self.assertIsInstance(self.sol, SolutionHeur)

    def test_validate(self):
        self.assertTrue(self.sol.validate())

    def test_evaluate_positif(self):
        self.assertGreater(self.sol.evaluate(), 0)

    def test_evaluate_egal_cout_total(self):
        self.assertAlmostEqual(self.sol.evaluate(), self.sol.cout_total, places=2)

    def test_statut_optimal_ou_satisfait(self):
        self.assertIn(self.sol.status, {"OPTIMAL_SOLUTION", "SATISFIED"})

    def test_x_non_nul(self):
        self.assertIsNotNone(self.sol.x)

    def test_r_non_nul(self):
        self.assertIsNotNone(self.sol.r)

    def test_e_non_nul(self):
        self.assertIsNotNone(self.sol.e)
        

class TestTroisInstances(unittest.TestCase):

    def test_toutes_les_instances(self):
        solver = MiniZincSolver("coin-bc")

        for inst in [1, 2, 3]:
            prob = ProblemeHeur(creation_instance=inst)
            sol = solver.solve(prob)

            self.assertTrue(sol.validate(), f"Instance {inst} invalide")
            self.assertGreater(sol.evaluate(), 0, f"Instance {inst} coût invalide")
            self.assertIn(sol.status, {"OPTIMAL_SOLUTION", "SATISFIED"})


if __name__ == "__main__":
    unittest.main()