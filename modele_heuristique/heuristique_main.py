from pathlib import Path
from minizinc_solver import MiniZincSolver
from solution import print_solution

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "modele_heuristique_lns.mzn"
SOLVER_NAME = "coin-bc"
TIME_LIMIT = 60

INSTANCES = [
    BASE_DIR / "inst_deterministe.dzn",
    BASE_DIR / "inst_stoch1.dzn",
    BASE_DIR / "inst_stoch2.dzn"
]

def main():
    solver = MiniZincSolver(
        model_path=str(MODEL_PATH),
        solver_name=SOLVER_NAME,
        time_limit=TIME_LIMIT
    )

    resultats = []

    for instance in INSTANCES:
        print(f"\nRésolution de l'instance : {instance}")

        sol = solver.solve_dzn(str(instance))

        print_solution(sol, str(instance))

        resultats.append((str(instance), sol["objectif"]))

if __name__ == "__main__":
    main()