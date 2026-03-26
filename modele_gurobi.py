import math
import pandas as pd
from gurobipy import Model, GRB, quicksum
demande_df = pd.read_excel("donnees.xlsx", sheet_name="demande")
cout_rupture_df = pd.read_excel("donnees.xlsx", sheet_name="cout_rupture")
stock_df = pd.read_excel("donnees.xlsx", sheet_name="stock")
capacite_df = pd.read_excel("donnees.xlsx", sheet_name="capacite")

#Modèle
model = Model("Modele_1")

#Ensemble I et K
I=demande_df["Succursales"].unique()
K=demande_df["Machines"].unique()
print("Succursales :", I)
print("Machines :", K)

#position
y = model.addVars(I, I, K, vtype=GRB.INTEGER, name="y")
pos = {}
for _, row in capacite_df.iterrows():
    i = row["Succursales"]
    pos[i] = (row["Position en X"], row ["Position en Y"])

#Dictionnnaire dik
d={}
for _, row in demande_df.iterrows():
    i = row["Succursales"]
    k = row["Machines"]
    d[(i, k)] = row["Demande"]

print(d)

#nombre de machines de type k à la succ i
x = model.addVars(I, K, vtype=GRB.INTEGER, name="x")
#rupture
r = model.addVars(I, K, vtype=GRB.INTEGER, name="r")
print(x)

#cout de rupture
p = {}
for _, row in cout_rupture_df.iterrows():
    k = row["Type"]
    p[k] = row["Cout de rupture"]
print(p)

#contrainte flux
for i in I:
    for k in K:
        model.addConstr(
            x[i, k]
            + quicksum(y[j, i, k] for j in I if j != i)
            - quicksum(y[i, j, k] for j in I if j != i)
            + r[i, k]
            == d[(i, k)]
        )
#contrainte limite d'envoi
for i in I:
    for k in K:
        model.addConstr(
            quicksum(y[i, j, k] for j in I if j != i) <= x[i, k]
        )

#stock total
#dictio stock
s = {}
for _, row in stock_df.iterrows():
    k = row["Type"]
    s[k] = row["Quantite"]
print(s)
#contrainte
for k in K:
    model.addConstr(
        quicksum(x[i, k] for i in I) <= s[k]
    )

#capacite
#dictio cpacite
cap = {}
for _, row in capacite_df.iterrows():
    i = row["Succursales"]
    cap[i] = row["Capacite"]
print(cap)
#contrainte
for i in I:
    model.addConstr(
        quicksum(x[i, k] for k in  K) <= cap[i]
    )

#calcul distances
dist = {}
for i in I:
    for j in I:
        xi, yi = pos[i]
        xj, yj = pos[j]
        dist[(i, j)] = math.sqrt((xi - xj) ** 2+ (yi-yj) ** 2)

#Cout transport
c = {}
cout_kilo = 0.55
for i in I:
    for j in I:
        c[(i,j)] = dist[(i,j)] * cout_kilo

#Empecher transfert d'une succu a elle meme
for i in I:
    for k in K:
        model.addConstr(y[i, i, k] == 0)

#Fonction objectif
model.setObjective(
    quicksum(p[k] * r[i, k] for i in I for k in K)
    +
    quicksum(c[i, j] * y[i, j, k] for i in I for j in I if i != j for k in K),
    GRB.MINIMIZE
)

#resolution
model.optimize()
