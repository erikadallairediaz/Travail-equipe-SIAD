set I;   # succursales
set K;   # types de machines
set S;   # scenarios

param demande {I, K, S} >= 0;
param prob {S} >= 0;

param stock {K} >= 0;
param cap {I} >= 0;
param cout_rupture {K} >= 0;
param cout_transport {I, I} >= 0;

var x {I, K} integer >= 0;

var y {I, I, K, S} integer >= 0;

var r {I, K, S} integer >= 0;

var e {I, K, S} integer >= 0;

# Fonction objectif
minimize CoutTotal:
    sum {s in S} prob[s] *
    (
        sum {i in I, k in K} cout_rupture[k] * r[i,k,s]
        +
        sum {i in I, j in I, k in K: i != j} cout_transport[i,j] * y[i,j,k,s]
    );

# Contraintes
# Stock total disponible pour chaque type de machine
subject to StockTotal {k in K}:
    sum {i in I} x[i,k] <= stock[k];

# Capacite maximale de chaque succursale
subject to CapaciteSuccursale {i in I}:
    sum {k in K} x[i,k] <= cap[i];

# Equilibre des flux pour chaque scenario
subject to Flux {i in I, k in K, s in S}:
    x[i,k]
    + sum {j in I : j != i} y[j,i,k,s]
    - sum {j in I : j != i} y[i,j,k,s]
    + r[i,k,s]
    - e[i,k,s]
    = demande[i,k,s];

# Une succursale ne peut pas envoyer plus que ce qu'elle a
subject to LimiteEnvoi {i in I, k in K, s in S}:
    sum {j in I: j != i} y[i,j,k,s] <= x[i,k];