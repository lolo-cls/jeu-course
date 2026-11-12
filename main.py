import random

from voiture import Voiture
from pilotes import Pilote
from circuits import Circuit
from course import Course

PILOTES_DISPONIBLES = [
    ("Charles Leclerc", 8),
    ("Lewis Hamilton", 9),
    ("George Russell", 8),
    ("Kimi Antonelli", 7),
    ("Lando Norris", 9),
    ("Oscar Piastri", 8),
    ("Max Verstappen", 10),
    ("Isack Hadjar", 7)
]

VOITURES_DISPONIBLES = [
    ("Ferrari", 320, 25),
    ("Mercedes", 300, 30),
    ("McLaren", 310, 28),
    ("Red Bull", 315, 27)
]

CIRCUITS_DISPONIBLES = [
    ("Monaco", 3.3, 10),
    ("Monza", 5.8, 10),
    ("Spa-Francorchamps", 7.0, 10),
    ("Las Vegas", 6.1, 10)
]


def demander_choix(message, minimum, maximum):
    """Demande un numéro valide à l'utilisateur."""
    while True:
        choix = input(message)

        if choix.isdigit():
            choix = int(choix)

            if minimum <= choix <= maximum:
                return choix

        print(f"Veuillez entrer un nombre entre {minimum} et {maximum}.")


def choisir_mode():
    print("\n=== MODE DE JEU ===")
    print("1. Jouer seul contre l'ordinateur")
    print("2. Jouer à deux joueurs")

    choix = demander_choix("Votre choix : ", 1, 2)
    return choix


def choisir_pilote(joueur):
    print(f"\n=== CHOIX DU PILOTE - {joueur} ===")

    for i, (nom, niveau) in enumerate(PILOTES_DISPONIBLES, start=1):
        print(f"{i}. {nom} (niveau {niveau}/10)")

    choix = demander_choix(
        "Choisissez votre pilote : ",
        1,
        len(PILOTES_DISPONIBLES)
    )

    nom, niveau = PILOTES_DISPONIBLES[choix - 1]
    return Pilote(nom, niveau)


def choisir_voiture(joueur):
    print(f"\n=== CHOIX DE LA VOITURE - {joueur} ===")

    for i, (marque, vitesse, acceleration) in enumerate(
        VOITURES_DISPONIBLES, start=1
    ):
        print(
            f"{i}. {marque} "
            f"(vitesse max : {vitesse}, accélération : {acceleration})"
        )

    choix = demander_choix(
        "Choisissez votre voiture : ",
        1,
        len(VOITURES_DISPONIBLES)
    )

    marque, vitesse, acceleration = VOITURES_DISPONIBLES[choix - 1]
    return Voiture(marque, vitesse, acceleration)


def choisir_circuit():
    print("\n=== CHOIX DU CIRCUIT ===")

    for i, (nom, longueur, tours) in enumerate(
        CIRCUITS_DISPONIBLES, start=1
    ):
        print(f"{i}. {nom} ({longueur} km, {tours} tours)")

    choix = demander_choix(
        "Choisissez votre circuit : ",
        1,
        len(CIRCUITS_DISPONIBLES)
    )

    nom, longueur, tours = CIRCUITS_DISPONIBLES[choix - 1]
    return Circuit(nom, longueur, tours)


def creer_ia(pilote_humain, voiture_humaine):
    """Crée un adversaire IA avec un pilote et une voiture."""
    pilotes_restants = [
        pilote for pilote in PILOTES_DISPONIBLES
        if pilote[0] != pilote_humain.nom
    ]

    nom, niveau = random.choice(pilotes_restants)
    pilote_ia = Pilote(nom, niveau)

    voitures_restantes = [
        voiture for voiture in VOITURES_DISPONIBLES
        if voiture[0] != voiture_humaine.marque
    ]

    marque, vitesse, acceleration = random.choice(voitures_restantes)

    # Modification des performances selon la difficulté
    if difficulte == "Facile":
        vitesse = vitesse * 0.80
        acceleration = acceleration * 0.80

    elif difficulte == "Moyen":
        vitesse = vitesse * 0.90
        acceleration = acceleration * 0.90

    elif difficulte == "Difficile":
        vitesse = vitesse * 1.10
        acceleration = acceleration * 1.10

    voiture_ia = Voiture(marque, vitesse, acceleration)

    pilote_ia.choisir_voiture(voiture_ia)

    return pilote_ia


    nom, niveau = random.choice(pilotes_restants)
    pilote_ia = Pilote(nom, niveau)

    voitures_restantes = [
        voiture for voiture in VOITURES_DISPONIBLES
        if voiture[0] != voiture_humaine.marque
    ]

    marque, vitesse, acceleration = random.choice(voitures_restantes)
    voiture_ia = Voiture(marque, vitesse, acceleration)

    pilote_ia.choisir_voiture(voiture_ia)
    return pilote_ia


def afficher_recapitulatif(circuit, pilotes, mode):
    print("\n=== RÉCAPITULATIF DE LA COURSE ===")
    print(f"Circuit : {circuit.nom}")
    print(f"Longueur : {circuit.longueur} km")
    print(f"Nombre de tours : {circuit.nombre_tours}")

    for i, pilote in enumerate(pilotes):
        if mode == 1 and i == 1:
            print("\n--- ADVERSAIRE IA (ORDINATEUR) ---")
        else:
            print(f"\n--- JOUEUR {i + 1} ---")

        print(f"Pilote : {pilote.nom}")
        print(f"Voiture : {pilote.voiture.marque}")
        print(f"Vitesse maximale : {pilote.voiture.vitesse_max}")
        print(f"Accélération : {pilote.voiture.acceleration}")

def choisir_difficulte():
    print("\n=== DIFFICULTÉ DE L'IA ===")
    print("1. Facile")
    print("2. Moyen")
    print("3. Difficile")

    choix = demander_choix("Choisissez la difficulté : ", 1, 3)

    difficultes = {
        1: "Facile",
        2: "Moyen",
        3: "Difficile"
    }

    return difficultes[choix]

def main():
    print("================================")
    print("       JEU DE COURSE")
    print("================================")

    mode = choisir_mode()

    pilote_1 = choisir_pilote("Joueur 1")
    voiture_1 = choisir_voiture("Joueur 1")
    pilote_1.choisir_voiture(voiture_1)

    pilotes = [pilote_1]

    if mode == 2:
    pilote_2 = choisir_pilote("Joueur 2")
    voiture_2 = choisir_voiture("Joueur 2")
    pilote_2.choisir_voiture(voiture_2)
    pilotes.append(pilote_2)
else:
difficulte = choisir_difficulte()
print(f"\nDifficulté choisie : {difficulte}")

pilote_ia = creer_ia(pilote_1, voiture_1, difficulte)
PILOTES_DISPONIBLES.append(pilote_ia)

def choisir_difficulte():
    print("\n=== DIFFICULTÉ DE L'IA ===")
    print("1. Facile")
    print("2. Moyen")
    print("3. Difficile")

    choix = demander_choix("Choisissez la difficulté : ", 1, 3)

    difficultes = {
        1: "Facile",
        2: "Moyen",
        3: "Difficile"
    }

    return difficultes[choix]

    circuit = choisir_circuit()



    afficher_recapitulatif(circuit, pilotes,mode)

    confirmation = input("\nAppuyez sur Entrée pour lancer la course...")
    course = Course(circuit, pilotes)
    course.lancer()




if __name__ == "__main__":
    main()
