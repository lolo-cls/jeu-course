import pygame
from voiture import Voiture

# Initialisation
pygame.init()

# Dimensions de la fenêtre
LARGEUR = 1000
HAUTEUR = 700

fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Jeu de course")

horloge = pygame.time.Clock()

# Couleurs
VERT = (40, 140, 40)
GRIS = (65, 65, 65)
BLANC = (255, 255, 255)
ROUGE = (200, 30, 30)

# Création du circuit
def dessiner_circuit():

    # Pelouse
    fenetre.fill(VERT)

    # Forme extérieure de la piste
    piste_exterieure = [
        (100, 150),
        (800, 150),
        (900, 200),
        (900, 400),
        (800, 500),
        (200, 500),
        (100, 400)
    ]

    # Forme intérieure de la piste
    piste_interieure = [
        (250, 250),
        (750, 250),
        (800, 280),
        (800, 350),
        (750, 400),
        (250, 400),
        (200, 350),
        (200, 280)
    ]

    # Dessiner la piste
    pygame.draw.polygon(fenetre, GRIS, piste_exterieure)

    # Retirer le centre pour créer la piste
    pygame.draw.polygon(fenetre, VERT, piste_interieure)

    # Murs extérieurs
    pygame.draw.lines(
        fenetre, BLANC, True, piste_exterieure, 6
    )

    # Murs intérieurs
    pygame.draw.lines(
        fenetre, BLANC, True, piste_interieure, 6
    )

    # Ligne de départ et d'arrivée
    pygame.draw.line(
        fenetre,
        BLANC,
        (300, 150),
        (300, 250),
        8
    )

    # Bordure rouge et blanche sur la ligne
    for i in range(5):
        couleur = ROUGE if i % 2 == 0 else BLANC

        pygame.draw.rect(
            fenetre,
            couleur,
            (290 + i * 4, 150, 4, 100)
        )
# Création des voitures
pilote_1 = Voiture(
    "Ferrari", 320, 25,
    (220, 0, 0), 350, 200
)

pilote_2 = Voiture(
    "Mercedes", 300, 30,
    (65, 65, 65), 350, 300
)

# Boucle principale
jeu_en_cours = True

while jeu_en_cours:

    for evenement in pygame.event.get():

        if evenement.type == pygame.QUIT:
            jeu_en_cours = False

    dessiner_circuit()
    pilote_1.dessiner(fenetre)
    pilote_2.dessiner(fenetre)

    pygame.display.flip()

    horloge.tick(60)

pygame.quit()