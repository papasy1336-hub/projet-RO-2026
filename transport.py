from pulp import *

# --- Données ---
usines = [1, 2]
entrepots = [1, 2, 3]

capacites = {1: 100, 2: 150}
demandes  = {1: 80, 2: 120, 3: 50}

couts = {
    (1,1): 2, (1,2): 3, (1,3): 1,
    (2,1): 5, (2,2): 4, (2,3): 8
}

# --- Modèle ---
modele = LpProblem("Transport", LpMinimize)

# Variables : x[i,j] = quantité envoyée de usine i à entrepôt j
x = LpVariable.dicts("x", [(i,j) for i in usines 
                             for j in entrepots], 
                      lowBound=0)

# --- Objectif : minimiser le coût total ---
modele += lpSum(couts[i,j] * x[i,j] 
                for i in usines 
                for j in entrepots)

# --- Contraintes capacité usines ---
for i in usines:
    modele += lpSum(x[i,j] for j in entrepots) <= capacites[i]

# --- Contraintes demande entrepôts ---
for j in entrepots:
    modele += lpSum(x[i,j] for i in usines) >= demandes[j]

# --- Résolution ---
modele.solve(PULP_CBC_CMD(msg=0))

# --- Résultats ---
print("=== Résultat Transport ===")
print(f"Statut : {LpStatus[modele.status]}")
print(f"Coût total minimum : {value(modele.objective)} MRU")
print()
print("Plan de transport :")
for i in usines:
    for j in entrepots:
        v = x[i,j].value()
        if v > 0:
            print(f"  Usine {i} → Entrepôt {j} : {v} unités")