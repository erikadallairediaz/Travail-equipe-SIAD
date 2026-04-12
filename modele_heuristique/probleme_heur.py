from .probleme import Probleme


class ProblemeHeur(Probleme):
    def __init__(self, creation_instance: int = 1):
        super().__init__()
        print("ProblemeHeur::init")

        self.creation_instance = creation_instance

        self.nI = 4
        self.nK = 3
        self.nS = 3

        self.model_path = "modele_heuristique/heuristique.mzn"

        self.prob_path = "modele_heuristique/prob.csv"
        self.stock_path = "modele_heuristique/stock.csv"
        self.capacite_path = "modele_heuristique/capacite.csv"
        self.cout_rupture_path = "modele_heuristique/cout_rupture.csv"
        self.cout_transport_path = "modele_heuristique/cout_transport.csv"
        self.ordre_sources_path = "modele_heuristique/ordre_sources.csv"
        self.demande_path = "modele_heuristique/demande.csv"