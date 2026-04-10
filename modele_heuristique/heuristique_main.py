from .probleme_heur import ProblemeHeur
from .minizinc_solver import MiniZincSolver


def main():
    prob = ProblemeHeur(instance_id=1)
    solver = MiniZincSolver("coin-bc")

    sol = solver.solve(prob)

    print("Valeur objectif :", sol.evaluate())
    print("Solution valide ?", sol.validate())
    sol.pretty_print()


if __name__ == "__main__":
    main()