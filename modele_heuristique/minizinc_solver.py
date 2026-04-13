from minizinc import Model, Instance, Solver as MznSolver

from solver import Solver
import lire_donnees as ld
from solution_heur import SolutionHeur


class MiniZincSolver(Solver):
    def __init__(self, solver_name: str = "coin-bc"):
        super().__init__()
        print("MiniZincSolver::init")
        self.solver_name = solver_name

    def solve(self, prob=None):
        if prob is None:
            raise ValueError("Un objet problème doit être fourni au solveur.")

        print("MiniZincSolver::solve")

        # Charger le modèle MiniZinc
        model = Model(prob.model_path)

        # Choisir le solveur MiniZinc
        mzn_solver = MznSolver.lookup(self.solver_name)

        # Créer l'instance MiniZinc
        instance = Instance(mzn_solver, model)

        # Charger les dimensions
        instance["nI"] = prob.nI
        instance["nK"] = prob.nK
        instance["nS"] = prob.nS

        # Charger les données depuis les CSV
        instance["prob"] = ld.lire_prob(prob.prob_path)
        instance["stock"] = ld.lire_stock(prob.stock_path)
        instance["capacite"] = ld.lire_capacite(prob.capacite_path)
        instance["cout_rupture"] = ld.lire_cout_rupture(prob.cout_rupture_path)
        instance["cout_transport"] = ld.lire_transport(prob.cout_transport_path)
        instance["ordre_sources"] = ld.lire_ordre_sources(prob.ordre_sources_path)
        instance["demande"] = ld.lire_demande(prob.demande_path, prob.creation_instance)

        # Résoudre
        result = instance.solve()

        # Récupérer les résultats
        x = result["x"] if "x" in result.solution.__dict__ else None
        y = result["y"] if "y" in result.solution.__dict__ else None
        r = result["r"] if "r" in result.solution.__dict__ else None
        e = result["e"] if "e" in result.solution.__dict__ else None

        cout_total = result.objective
        status = str(result.status)

        return SolutionHeur(
            x=x,
            y=y,
            r=r,
            e=e,
            cout_total=cout_total,
            status=status
        )