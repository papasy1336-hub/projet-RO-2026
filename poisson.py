from pulp import *

# --- Données ---
ports = ["Nouadhibou", "Tanit"]
villes = ["Nouakchott", "Rosso", "Atar"]

# Capacités des ports (tonnes)
capacites = {"Nouadhibou": 200, "Tanit": 150}

# Demandes des villes (tonnes)
demandes = {"Nouakchott": 150, "Rosso": 80, "Atar": 100}

# Coûts de transport (MRU/tonne) basés sur distance
couts = {
    ("Nouadhibou", "Nouakchott"): 470,
    ("Nouadhibou", "Rosso"):      550,
    ("Nouadhibou", "Atar"):       400,
    ("Tanit",      "Nouakchott"): 300,
    ("Tanit",      "Rosso"):      380,
    ("Tanit",      "Atar"):       350
}

# Temps de trajet (heures) - contrainte périssabilité
temps = {
    ("Nouadhibou", "Nouakchott"): 7,
    ("Nouadhibou", "Rosso"):      9,
    ("Nouadhibou", "Atar"):       6,
    ("Tanit",      "Nouakchott"): 5,
    ("Tanit",      "Rosso"):      6,
    ("Tanit",      "Atar"):       5
}
temps_max = 12  # heures max avant détérioration

# --- Modèle ---
modele = LpProblem("Transport_Poissons", LpMinimize)

# Variables : quantité envoyée de port p vers ville v
x = LpVariable.dicts("x",
    [(p, v) for p in ports for v in villes],
    lowBound=0)

# --- Objectif : minimiser coût total ---
modele += lpSum(couts[p,v] * x[p,v] 
                for p in ports for v in villes)

# --- Contrainte 1 : capacité des ports ---
for p in ports:
    modele += lpSum(x[p,v] for v in villes) <= capacites[p]

# --- Contrainte 2 : demande des villes ---
for v in villes:
    modele += lpSum(x[p,v] for p in ports) >= demandes[v]

# --- Contrainte 3 : périssabilité ---
# On n'utilise que les routes où temps <= temps_max
for p in ports:
    for v in villes:
        if temps[p,v] > temps_max:
            modele += x[p,v] == 0

# --- Résolution ---
modele.solve(PULP_CBC_CMD(msg=0))

# --- Résultats ---
print("=" * 45)
print("   TRANSPORT DE POISSONS - MAURITANIE")
print("=" * 45)
print(f"Statut       : {LpStatus[modele.status]}")
print(f"Coût total   : {value(modele.objective):,.0f} MRU")
print()
print("Plan de livraison optimal :")
print("-" * 45)
for p in ports:
    for v in villes:
        val = x[p,v].value()
        if val and val > 0:
            t = temps[p,v]
            print(f"  {p} → {v}")
            print(f"    Quantité : {val:.0f} tonnes")
            print(f"    Temps    : {t}h ✅")
            print(f"    Coût     : {couts[p,v]*val:,.0f} MRU")
            print()

# Vérification des demandes
print("Vérification des demandes :")
print("-" * 45)
for v in villes:
    total = sum(x[p,v].value() or 0 for p in ports)
    print(f"  {v} : {total:.0f}/{demandes[v]} tonnes ✅")