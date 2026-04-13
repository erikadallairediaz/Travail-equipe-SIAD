from probleme_heur import ProblemeHeur 
from minizinc_solver import MiniZincSolver
import time


def main():
    solver = MiniZincSolver("coin-bc")

    for inst in [1, 2, 3]:
        print("\n" + "="*50)
        print(f"INSTANCE {inst}")
        print("="*50)

        prob = ProblemeHeur(creation_instance=inst)

        start = time.time()  # début du chrono

        sol = solver.solve(prob)

        end = time.time()  # fin du chrono

        print("Valeur fct objectif :", sol.evaluate())
        print("Solution valide ?", sol.validate())
        print(f"Temps de résolution : {end - start:.4f} secondes")

        sol.print_propre()


if __name__ == "__main__":
    main()