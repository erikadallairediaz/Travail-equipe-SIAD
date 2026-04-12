import os
from probleme_stoch import ProblemeStochastique
from solveur_stoch import SolveurStochastique
 
DOSSIER_CSV = os.path.join(os.path.dirname(__file__), "..", "modele_heuristique")
 
 
def main():
    solveur = SolveurStochastique(modele_path="modele_stochastique/modele_stochastique.mod")
 
    for instance_id in [1, 2, 3]:
        probleme = ProblemeStochastique(instance_id, dossier_csv=DOSSIER_CSV)
        solution = solveur.resoudre(probleme)
 
        print(f"\nRéalisable : {'Oui' if solution.validate() else 'NON'}")
        solution.afficher()
 
 
if __name__ == "__main__":
    main()