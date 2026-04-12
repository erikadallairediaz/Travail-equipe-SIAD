% =========================
% ENSEMBLES ET PARAMETRES
% =========================

int: nI;   % nombre de succursales
int: nK;   % nombre de types de machines
int: nS;   % nombre de scenarios

set of int: I = 1..nI;
set of int: K = 1..nK;
set of int: S = 1..nS;

array[I, K, S] of int: demande;          % demande[i,k,s]
array[S] of float: prob;                 % probabilite des scenarios
array[K] of int: stock;                  % stock total disponible par type de machine
array[I] of int: capacite;               % capacite maximale de chaque succursale
array[K] of float: cout_rupture;         % cout d'une rupture par type de machine
array[I, I] of float: cout_transport;    % cout de transfert entre succursales

% Parametre de priorite par proximite
int: nP = nI - 1;
set of int: P = 1..nP;

% ordre_sources[j,p] = p-ieme source la plus proche de la destination j
array[I, P] of int: ordre_sources;

% Bornes utiles
int: stock_max = max(k in K)(stock[k]);
int: demande_max = max(i in I, k in K, s in S)(demande[i, k, s]);

% =========================
% VARIABLES DE DECISION
% =========================

% x[i,k] = allocation initiale de machines k a la succursale i
array[I, K] of var 0..stock_max: x;

% y[i,j,k,s] = nombre de machines k transferees de i vers j au scenario s
array[I, I, K, S] of var 0..stock_max: y;

% r[i,k,s] = rupture pour la succursale i, machine k, scenario s
array[I, K, S] of var 0..demande_max: r;

% e[i,k,s] = surplus pour la succursale i, machine k, scenario s
array[I, K, S] of var 0..demande_max: e;

% utilise_source[j,p,k,s] = 1 si la p-ieme source la plus proche de j
% est utilisee pour envoyer au moins une machine k dans le scenario s
array[I, P, K, S] of var 0..1: utilise_source;

% =========================
% CONTRAINTES
% =========================

% 1) Le stock total alloue pour chaque type ne peut pas depasser le stock disponible
constraint
forall(k in K) (
    sum(i in I)(x[i, k]) <= stock[k]
);

% 2) La capacite totale de chaque succursale ne peut pas etre depassee
constraint
forall(i in I) (
    sum(k in K)(x[i, k]) <= capacite[i]
);

% 3) Aucun transfert vers soi-meme
constraint
forall(i in I, k in K, s in S) (
    y[i, i, k, s] = 0
);

% 4) Une succursale ne peut pas envoyer plus que son allocation initiale
constraint
forall(i in I, k in K, s in S) (
    sum(j in I where j != i)(y[i, j, k, s]) <= x[i, k]
);

% 5) Equilibre des machines a chaque succursale, pour chaque scenario
constraint
forall(i in I, k in K, s in S) (
    x[i, k]
    + sum(j in I where j != i)(y[j, i, k, s])
    - sum(j in I where j != i)(y[i, j, k, s])
    + r[i, k, s]
    - e[i, k, s]
    = demande[i, k, s]
);

% =========================
% CONTRAINTES DE PRIORITE PAR PROXIMITE
% =========================

% Liaison entre y et utilise_source
constraint
forall(j in I, p in P, k in K, s in S) (
    let { int: i = ordre_sources[j, p] } in
        y[i, j, k, s] <= stock_max * utilise_source[j, p, k, s]
);

constraint
forall(j in I, p in P, k in K, s in S) (
    let { int: i = ordre_sources[j, p] } in
        y[i, j, k, s] >= utilise_source[j, p, k, s]
);

% On ne peut pas utiliser une source plus lointaine
% sans utiliser toutes les sources plus proches avant
constraint
forall(j in I, p in 1..nP-1, k in K, s in S) (
    utilise_source[j, p+1, k, s] <= utilise_source[j, p, k, s]
);

% =========================
% FONCTION OBJECTIF
% =========================

var float: CoutTotal =
    sum(s in S)(
        prob[s] * (
            sum(i in I, k in K)(cout_rupture[k] * r[i, k, s]) +
            sum(i in I, j in I, k in K where i != j)(
                cout_transport[i, j] * y[i, j, k, s]
            )
        )
    );

solve minimize CoutTotal;

% =========================
% AFFICHAGE
% =========================

output [

"===== ALLOCATION INITIALE x =====\n",
"        Chariot  Excavatrice  Nacelle\n",

concat([
    show(i) ++ " :    " ++
    show(x[i,1]) ++ "         " ++
    show(x[i,2]) ++ "            " ++
    show(x[i,3]) ++ "\n"
    | i in I
]),

"\n===== RUPTURES r (par scenario) =====\n",

concat([
    "Scenario " ++ show(s) ++ "\n" ++
    concat([
        show(i) ++ " : " ++
        show([r[i,k,s] | k in K]) ++ "\n"
        | i in I
    ]) ++ "\n"
    | s in S
]),

"\n===== SURPLUS e (par scenario) =====\n",

concat([
    "Scenario " ++ show(s) ++ "\n" ++
    concat([
        show(i) ++ " : " ++
        show([e[i,k,s] | k in K]) ++ "\n"
        | i in I
    ]) ++ "\n"
    | s in S
]),

"\n===== SOURCES PRIORITAIRES UTILISEES =====\n",

concat([
    "Scenario " ++ show(s) ++ ", machine " ++ show(k) ++ "\n" ++
    concat([
        "Destination " ++ show(j) ++ " : " ++
        show([utilise_source[j,p,k,s] | p in P]) ++ "\n"
        | j in I
    ]) ++ "\n"
    | s in S, k in K
]),

"\nCoutTotal = ", show(CoutTotal), "\n"
];
