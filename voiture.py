import pygame


class Voiture:
    def __init__(self, marque, vitesse_max, acceleration, couleur, x, y):

        # Caractéristiques de la voiture
        self.marque = marque
        self.vitesse_max = vitesse_max
        self.acceleration = acceleration
        self.vitesse = 0

        # Caractéristiques graphiques
        self.couleur = couleur
        self.x = x
        self.y = y
        self.largeur = 40
        self.hauteur = 25
        self.angle = 0

    def accelerer(self):
        self.vitesse += self.acceleration

        if self.vitesse > self.vitesse_max:
            self.vitesse = self.vitesse_max

    def freiner(self, freinage=10):
        self.vitesse -= freinage

        if self.vitesse < 0:
            self.vitesse = 0

    def dessiner(self, fenetre):

        # Création de la forme de la voiture
        voiture = pygame.Surface(
            (self.largeur, self.hauteur),
            pygame.SRCALPHA
        )

        pygame.draw.rect(
            voiture,
            self.couleur,
            (0, 0, self.largeur, self.hauteur),
            border_radius=6
        )

        # Rotation de la voiture
        voiture_tournee = pygame.transform.rotate(
            voiture, self.angle
        )

        # Positionnement au centre de la voiture
        rectangle = voiture_tournee.get_rect(
            center=(self.x, self.y)
        )

        fenetre.blit(voiture_tournee, rectangle)

