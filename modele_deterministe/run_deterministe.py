from modele_deterministe import ModeleDeterministe

scenario = [1, 2, 3]

for s in scenario:
    print(f"Scenario {s}")
    modele = ModeleDeterministe(scenario=s)
    modele.resoudre()
    modele.afficher_resultats()
    