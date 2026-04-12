from .solution import Solution


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

    def evaluate(self):
        return self.cout_total

    def validate(self):
        return self.status in {"OPTIMAL_SOLUTION", "SATISFIED", "ALL_SOLUTIONS"}