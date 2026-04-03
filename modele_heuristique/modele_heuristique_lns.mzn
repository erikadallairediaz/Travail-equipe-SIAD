int: nI;  %nb. succursales
int: nK;  %nb. types de machines
int: nS;  %nb. scenarios

% Ensembles
set of int: I = 1..nI;
set of int: K = 1..nK;
set of int: S = 1..nS;

array[I, K, S] of int: demande; % Demande de succ i de la machine k pour le scenario s
array[S] of float: prob; % Prob de chaque scenario
array[K] of int: stock; % Machines dispos par type
array[I] of int: capacite; % Cap max de chaque succ
array[K] of float: cout_rupture;
array[I, I] of float: cout_transport; 

% Si -1 : valeur non fixe
array[I, K] of int: xFix;

int: stock_max = max(k in K)(stock[k]);
int: demande_max = max(i in I, k in K, s in S)(demande[i, k, s]);
 
array[I,K] of var 0..stock_max: x;
array[I, I, K, S] of var 0..stock_max: y;
array[I, K, S] of var 0..demande_max: r;
array[I, K, S] of var 0..demande_max: e;

% Fixer les x partiellement
constraint
forall(i in I, k in K) (
    if xFix[i, k] >= 0 then
        x[i, k] = xFix[i, k]
    else
        true
    endif
);

% Contraintes

% Stock tot dispo pour chaque type de machine
constraint
forall(k in K) (
    sum(i in I)(x[i, k]) <= stock[k]
);

% Capacite max de chaque succursale
constraint
forall(i in I) (
    sum(k in K)(x[i, k]) <= capacite[i]
);

% Equilibre des flux
constraint
forall(i in I, k in K, s in S) (
    x[i, k]
    + sum(j in I where j != i)(y[j, i, k, s])
    - sum(j in I where j != i)(y[i, j, k, s])
    + r[i, k, s]
    - e[i, k, s]
    = demande[i, k, s]
);

% Une succursale ne peut pas envoyer plus que ce qu'elle a 
constraint
forall(i in I, k in K, s in S) (
    sum(j in I where j != i)(y[i, j, k, s]) <= x[i, k]
);

% Fct. obj
var float: CoutTotal :: output_var =
    sum(s in S)(
        prob[s] * (
            sum(i in I, k in K)(cout_rupture[k] * r[i, k, s]) +
            sum(i in I, j in I, k in K where i != j)(
                cout_transport[i, j] * y[i, j, k, s]
            )
        )
    );

solve minimize CoutTotal;

output [
  "CoutTotal = ", show(CoutTotal), "\n"
];