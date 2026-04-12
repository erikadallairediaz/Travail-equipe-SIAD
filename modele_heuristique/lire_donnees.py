# Lit les fichiers CSV
import csv

# Ordres FIXES (doivent correspondre au .mzn)
I_list = ["A", "B", "C", "D"]
K_list = ["Chariot_elevateur", "Excavatrice", "Nacelle"]
S_list = ["faible", "moyen", "eleve"]


# =========================
# PROBABILITES
# =========================
def lire_prob(fichier):
    prob = [0.0] * len(S_list)

    with open(fichier, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            s = row["scenario"].strip()
            val = float(row["prob"])
            prob[S_list.index(s)] = val

    return prob


# =========================
# STOCK
# =========================
def lire_stock(fichier):
    stock = [0] * len(K_list)

    with open(fichier, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            k = row["machine"].strip()
            val = int(row["stock"])
            stock[K_list.index(k)] = val

    return stock


# =========================
# CAPACITE
# =========================
def lire_capacite(fichier):
    capacite = [0] * len(I_list)

    with open(fichier, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            i = row["succursale"].strip()
            val = int(row["capacite"])
            capacite[I_list.index(i)] = val

    return capacite


# =========================
# COUT RUPTURE
# =========================
def lire_cout_rupture(fichier):
    cout = [0.0] * len(K_list)

    with open(fichier, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            k = row["machine"].strip()
            val = float(row["cout_rupture"])
            cout[K_list.index(k)] = val

    return cout


# =========================
# COUT TRANSPORT (MATRICE)
# =========================
def lire_transport(fichier):
    n = len(I_list)
    mat = [[0.0 for _ in range(n)] for _ in range(n)]

    with open(fichier, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            i = row["origine"].strip()
            j = row["destination"].strip()
            val = float(row["cout"])

            mat[I_list.index(i)][I_list.index(j)] = val

    return mat


# =========================
# ORDRE DES SOURCES
# =========================
def lire_ordre_sources(fichier):
    nI = len(I_list)
    nP = nI - 1

    ordre = [[0 for _ in range(nP)] for _ in range(nI)]

    with open(fichier, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            j = row["destination"].strip()
            p = int(row["rang"]) - 1   # index 0
            i = row["source"].strip()

            ordre[I_list.index(j)][p] = I_list.index(i) + 1  # MiniZinc = index 1-based

    return ordre


# =========================
# DEMANDE (3D)
# =========================
def lire_demande(fichier, instance_id):
    nI = len(I_list)
    nK = len(K_list)
    nS = len(S_list)

    # tableau 3D
    demande = [[[0 for _ in range(nS)] for _ in range(nK)] for _ in range(nI)]

    with open(fichier, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            inst = int(row["instance"])
            if inst != instance_id:
                continue

            i = row["succursale"].strip()
            k = row["machine"].strip()
            s = row["scenario"].strip()
            val = int(row["valeur"])

            demande[I_list.index(i)][K_list.index(k)][S_list.index(s)] = val

    return demande


    