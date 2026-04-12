from .probleme_heur import ProblemeHeur
from .minizinc_solver import MiniZincSolver


def main():
    prob = ProblemeHeur(creation_instance=1)
    solver = MiniZincSolver("coin-bc")

    sol = solver.solve(prob)

    print("Valeur fct objectif :", sol.evaluate())
    print("Solution valide ?", sol.validate())
    sol.print_propre()


if __name__ == "__main__":
    main()