from pulp import *

# --- Données ---
objets  = [1, 2, 3]
poids   = {1: 2, 2: 3, 3: 4}
valeurs = {1: 3, 2: 4, 3: 5}
capacite = 5

# --- Modèle ---
modele = LpProblem("Sac_a_dos", LpMaximize)

# Variables : x[i] = 1 si on prend l'objet, 0 sinon
x = LpVariable.dicts("x", objets, cat="Binary")

# --- Objectif : maximiser la valeur totale ---
modele += lpSum(valeurs[i] * x[i] for i in objets)

# --- Contrainte : ne pas dépasser la capacité ---
modele += lpSum(poids[i] * x[i] for i in objets) <= capacite

# --- Résolution ---
modele.solve(PULP_CBC_CMD(msg=0))

# --- Résultats ---
print("=== Résultat Sac à dos ===")
print(f"Statut : {LpStatus[modele.status]}")
for i in objets:
    if x[i].value() == 1:
        print(f"  ✅ Objet {i} (poids={poids[i]}, valeur={valeurs[i]}) → PRIS")
    else:
        print(f"  ❌ Objet {i} (poids={poids[i]}, valeur={valeurs[i]}) → non pris")
print(f"Valeur totale : {value(modele.objective)}")