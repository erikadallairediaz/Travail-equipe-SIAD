from .probleme_heur import ProblemeHeur 
from .minizinc_solver import MiniZincSolver


def main():
    solver = MiniZincSolver("coin-bc")

    # boucler sur les 3 instances
    for inst in [1, 2, 3]:
        print(f"\nINSTANCE {inst}\n")

        prob = ProblemeHeur(creation_instance=inst)
        sol = solver.solve(prob)

        print("Valeur fct objectif :", sol.evaluate())
        print("Solution valide ?", sol.validate())
        sol.print_propre()


if __name__ == "__main__":
    main()