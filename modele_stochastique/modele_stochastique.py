from amplpy import AMPL


def executer_instance(fichier_data):

    ampl = AMPL()

    ampl.read("modele_stochastique/modele_stochastique.mod")
    ampl.read_data(f"modele_stochastique/{fichier_data}")
    ampl.set_option("solver", "gurobi")
    ampl.solve()

    cout = ampl.get_objective("CoutTotal").value()
    print(f"\nInstance : {fichier_data}")
    print(f"Fonction objectif : {cout:.2f}")

    x_data = ampl.get_variable("x").get_values().to_pandas()
    x_data.index.names = ["succursale", "machine"]

    r_data = ampl.get_variable("r").get_values().to_pandas()
    r_data.index.names = ["succursale", "machine", "scenario"]

    y_data = ampl.get_variable("y").get_values().to_pandas()
    y_data.index.names = ["origine", "destination", "machine", "scenario"]

    e_data = ampl.get_variable("e").get_values().to_pandas()
    e_data.index.names = ["succursale", "machine", "scenario"]

    

    print("\nRépartition des équipements entre les succursales:")
    repartition = x_data[x_data["x.val"] > 0]
    if repartition.empty:
        print("Aucune allocation")
    else:
        print(repartition)

    print("\nRuptures r :")
    rupture = r_data[r_data["r.val"] > 0]
    if rupture.empty:
        print("Aucune rupture")
    else:
        print(rupture)

    print("\nTransferts y :")
    transfert = y_data[y_data["y.val"] > 0]
    if transfert.empty:
        print("Aucun transfert")
    else:
        print(transfert)

    print("\nSurplus e :")
    surplus = e_data[e_data["e.val"] > 0]
    if surplus.empty:
        print("Aucun surplus")
    else:
        print(surplus)