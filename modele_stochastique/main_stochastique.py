from modele_stochastique import ModeleStochastique

instances = ["instance1.dat", "instance2.dat", "instance3.dat"]

for instance in instances:
    modele = ModeleStochastique("modele_stochastique/modele_stochastique.mod")
    modele.charger(f"modele_stochastique/{instance}")
    modele.resoudre()
    
    print(f"\nInstance : {instance}")
    print(f"Fonction objectif : {modele.cout_total:.2f}")

    resultats = modele.get_resultats()

    print("\nRépartition des équipements entre les succursales:")
    x = resultats["x"]
    x.index.names = ["succursale", "machine"]
    repartition = x[x["x.val"] > 0]
    print(repartition if not repartition.empty else "Aucune allocation")

    print("\nRuptures r :")
    r = resultats["r"]
    r.index.names = ["succursale", "machine", "scenario"]
    rupture = r[r["r.val"] > 0]
    print(rupture if not rupture.empty else "Aucune rupture")

    print("\nTransferts y :")
    y = resultats["y"]
    y.index.names = ["origine", "destination", "machine", "scenario"]
    transfert = y[y["y.val"] > 0]
    print(transfert if not transfert.empty else "Aucun transfert")

    print("\nSurplus e :")
    e = resultats["e"]
    e.index.names = ["succursale", "machine", "scenario"]
    surplus = e[e["e.val"] > 0]
    print(surplus if not surplus.empty else "Aucun surplus")