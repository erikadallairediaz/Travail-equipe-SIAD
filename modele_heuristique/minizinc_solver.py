from minizinc import Instance, Model, Solver, Status
import datetime


class MiniZincSolver:

    def __init__(self, model_path, solver_name="coin-bc", time_limit=60):
        self.model_path = model_path
        self.solver = Solver.lookup(solver_name)
        self.time_limit = time_limit

    def solve_dzn(self, dzn_path):
        model = Model(self.model_path)
        model.add_file(dzn_path)

        instance = Instance(self.solver, model)

        result = instance.solve(
            timeout=datetime.timedelta(seconds=self.time_limit)
        )

        return self.format_result(result)

    def format_result(self, result):
        sol = {
            "status": str(result.status),
            "objectif": None,
            "x": None,
            "r": None,
            "e": None,
            "y": None
        }

        if result.status in [Status.SATISFIED, Status.OPTIMAL_SOLUTION]:
            for var in ["x", "r", "e", "y"]:
                try:
                    sol[var] = result[var]
                except Exception:
                    pass

            # 1) objectif officiel du solveur
            try:
                sol["objectif"] = result.objective
            except Exception:
                pass

            # 2) variable du modèle
            if sol["objectif"] is None:
                try:
                    sol["objectif"] = result["CoutTotal"]
                except Exception:
                    pass

            # 3) attribut de solution
            if sol["objectif"] is None:
                try:
                    sol["objectif"] = result.solution.CoutTotal
                except Exception:
                    pass

        return sol