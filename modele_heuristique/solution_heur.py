from solution import Solution


class SolutionHeur(Solution):
    def __init__(self, x=None, y=None, r=None, e=None, cout_total=None, status=None):
        super().__init__()
        print("SolutionHeur::init")

        self.x = x
        self.y = y
        self.r = r
        self.e = e
        self.cout_total = cout_total
        self.status = status

        self.succursales = ["A", "B", "C", "D"]
        self.machines = ["Chariot_elevateur", "Excavatrice", "Nacelle"]
        self.scenarios = ["faible", "moyen", "eleve"]

    def evaluate(self):
        return self.cout_total

    def validate(self):
        return self.status in {"OPTIMAL_SOLUTION", "SATISFIED"}

    def print_propre(self):
        print("\n=== SOLUTION ===")
        print(f"Statut : {self.status}")
        print(f"Coût total : {self.cout_total:.4f}")

        self._print_x()
        self._print_r()
        self._print_e()
        self._print_nonzero_transfers()

    def _print_x(self):
        if self.x is None:
            print("\nAllocation initiale x : aucune donnée")
            return

        print("\n=== ALLOCATION INITIALE x ===")
        print(f"{'Succursale':<12}{'Chariot':>12}{'Excavatrice':>15}{'Nacelle':>12}")

        for i, succ in enumerate(self.succursales):
            print(
                f"{succ:<12}"
                f"{self.x[i][0]:>12}"
                f"{self.x[i][1]:>15}"
                f"{self.x[i][2]:>12}"
            )

    def _print_r(self):
        if self.r is None:
            print("\nRuptures r : aucune donnée")
            return

        print("\n=== RUPTURES r ===")
        for s, scenario in enumerate(self.scenarios):
            print(f"\nScénario : {scenario}")
            print(f"{'Succursale':<12}{'Chariot':>12}{'Excavatrice':>15}{'Nacelle':>12}")

            for i, succ in enumerate(self.succursales):
                print(
                    f"{succ:<12}"
                    f"{self.r[i][0][s]:>12}"
                    f"{self.r[i][1][s]:>15}"
                    f"{self.r[i][2][s]:>12}"
                )

    def _print_e(self):
        if self.e is None:
            print("\nSurplus e : aucune donnée")
            return

        print("\n=== SURPLUS e ===")
        for s, scenario in enumerate(self.scenarios):
            print(f"\nScénario : {scenario}")
            print(f"{'Succursale':<12}{'Chariot':>12}{'Excavatrice':>15}{'Nacelle':>12}")

            for i, succ in enumerate(self.succursales):
                print(
                    f"{succ:<12}"
                    f"{self.e[i][0][s]:>12}"
                    f"{self.e[i][1][s]:>15}"
                    f"{self.e[i][2][s]:>12}"
                )

    def _print_nonzero_transfers(self):
        if self.y is None:
            print("\nTransferts y : aucune donnée")
            return

        print("\n=== TRANSFERTS y NON NULS ===")
        found = False

        for i, src in enumerate(self.succursales):
            for j, dst in enumerate(self.succursales):
                if i == j:
                    continue

                for k, machine in enumerate(self.machines):
                    for s, scenario in enumerate(self.scenarios):
                        qty = self.y[i][j][k][s]
                        if qty != 0:
                            found = True
                            print(
                                f"{src} -> {dst} | "
                                f"machine : {machine} | "
                                f"scénario : {scenario} | "
                                f"quantité : {qty}"
                            )

        if not found:
            print("Aucun transfert non nul.")