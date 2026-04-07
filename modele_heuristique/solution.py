def print_solution(sol, title="Solution"):
    print("\n========================")
    print(title)
    print("========================")

    print("Status :", sol["status"])
    print("CoutTotal :", sol["objectif"])

    if sol["x"]:
        print("\nx (allocation):")
        for row in sol["x"]:
            print(row)

    if sol["r"]:
        print("\nr (ruptures):")
        print(sol["r"])

    if sol["e"]:
        print("\ne (excédents):")
        print(sol["e"])

    if sol["y"]:
        print("\ny (transferts):")
        print(sol["y"])