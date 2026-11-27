
import pygame
import math
import sys
import random

pygame.init()

# =====================================================
# CONFIGURATION
# =====================================================

WIDTH, HEIGHT = 1100, 760
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("F1 Racing")

CLOCK = pygame.time.Clock()
FPS = 60

WHITE = (245, 245, 245)
BLACK = (15, 15, 18)
RED = (220, 25, 40)
GREY = (90, 90, 95)
DARK = (25, 27, 32)
GREEN = (35, 110, 65)
YELLOW = (245, 205, 50)

FONT = pygame.font.SysFont("Arial", 22)
BIG_FONT = pygame.font.SysFont("Arial", 52, bold=True)
SMALL_FONT = pygame.font.SysFont("Arial", 16)

# =====================================================
# DONNEES DU JEU
# =====================================================

CARS = {
    "Ferrari": (220, 25, 35),
    "Mercedes": (0, 190, 175),
    "McLaren": (255, 125, 20),
    "Red Bull": (30, 65, 160)
}

DRIVERS = [
    "Charles Leclerc",
    "Lewis Hamilton",
    "George Russell",
    "Kimi Antonelli",
    "Lando Norris",
    "Oscar Piastri",
    "Max Verstappen",
    "Isack Hadjar"
]

TRACKS = {
    "Monaco": {
        "points": [
            (160, 180), (350, 130), (560, 145),
            (790, 155), (920, 230), (880, 350),
            (950, 480), (790, 570), (600, 545),
            (450, 620), (260, 560), (120, 440),
            (145, 300)
        ],
        "width": 90,
        "night": False
    },

    "Monza": {
        "points": [
            (150, 170), (420, 150), (780, 150),
            (930, 240), (830, 340), (920, 470),
            (800, 570), (530, 550), (250, 560),
            (120, 450), (210, 340), (120, 250)
        ],
        "width": 100,
        "night": False
    },

    "Spa-Francorchamps": {
        "points": [
            (150, 530), (250, 390), (160, 260),
            (300, 130), (480, 110), (620, 175),
            (790, 125), (940, 240), (830, 360),
            (940, 490), (760, 590), (570, 500),
            (420, 600), (250, 570)
        ],
        "width": 88,
        "night": False
    },

    "Las Vegas": {
        "points": [
            (150, 530), (150, 370), (150, 190),
            (320, 140), (530, 140), (660, 140),
            (670, 270), (850, 270), (960, 270),
            (960, 400), (820, 440), (660, 440),
            (600, 540), (420, 570), (250, 570)
        ],
        "width": 82,
        "night": True
    }
}

# =====================================================
# OUTILS GRAPHIQUES
# =====================================================

def draw_text(surface, text, font, color, x, y, center=True):
    image = font.render(str(text), True, color)
    rect = image.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    surface.blit(image, rect)


def distance(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def smooth_track(points, steps=12):
    result = []

    count = len(points)

    for i in range(count):
        p0 = points[(i - 1) % count]
        p1 = points[i]
        p2 = points[(i + 1) % count]
        p3 = points[(i + 2) % count]

        for j in range(steps):
            t = j / steps
            t2 = t * t
            t3 = t2 * t

            x = 0.5 * (
                2 * p1[0]
                + (-p0[0] + p2[0]) * t
                + (2*p0[0] - 5*p1[0] + 4*p2[0] - p3[0]) * t2
                + (-p0[0] + 3*p1[0] - 3*p2[0] + p3[0]) * t3
            )

            y = 0.5 * (
                2 * p1[1]
                + (-p0[1] + p2[1]) * t
                + (2*p0[1] - 5*p1[1] + 4*p2[1] - p3[1]) * t2
                + (-p0[1] + 3*p1[1] - 3*p2[1] + p3[1]) * t3
            )

            result.append((int(x), int(y)))

    return result


def point_segment_distance(p, a, b):
    dx = b[0] - a[0]
    dy = b[1] - a[1]

    if dx == 0 and dy == 0:
        return distance(p, a)

    t = ((p[0]-a[0])*dx + (p[1]-a[1])*dy) / (dx*dx + dy*dy)
    t = max(0, min(1, t))

    closest = (a[0] + t*dx, a[1] + t*dy)
    return distance(p, closest)


# =====================================================
# CIRCUIT
# =====================================================

class Circuit:

    def __init__(self, name):
        data = TRACKS[name]

        self.name = name
        self.points = smooth_track(data["points"])
        self.width = data["width"]
        self.night = data["night"]

        self.length = len(self.points)

        self.surface = pygame.Surface((WIDTH, HEIGHT))
        self.make_surface()

    def make_surface(self):

        if self.night:
            self.surface.fill((20, 22, 38))
        else:
            self.surface.fill((45, 115, 65))

        # Bordure extérieure
        pygame.draw.lines(
            self.surface, (230, 230, 230),
            True, self.points, self.width + 18
        )

        # Bande rouge et blanche
        pygame.draw.lines(
            self.surface, (190, 35, 40),
            True, self.points, self.width + 10
        )

        # Route
        pygame.draw.lines(
            self.surface, (55, 57, 62),
            True, self.points, self.width
        )

        # Ligne centrale
        pygame.draw.lines(
            self.surface, (105, 105, 108),
            True, self.points, 2
        )

        # Ligne d'arrivée
        p = self.points[0]
        next_p = self.points[5]

        dx = next_p[0] - p[0]
        dy = next_p[1] - p[1]

        length = math.hypot(dx, dy)
        nx = -dy / length
        ny = dx / length

        a = (p[0] - nx*self.width/2, p[1] - ny*self.width/2)
        b = (p[0] + nx*self.width/2, p[1] + ny*self.width/2)

        pygame.draw.line(
            self.surface, WHITE, a, b, 7
        )

    def draw(self, screen):
        screen.blit(self.surface, (0, 0))

    def distance_from_road(self, position):

        best = 999999

        for i in range(self.length):
            a = self.points[i]
            b = self.points[(i+1) % self.length]

            d = point_segment_distance(position, a, b)

            if d < best:
                best = d

        return best

    def nearest_index(self, position):

        best_index = 0
        best_distance = 999999

        for i, point in enumerate(self.points):
            d = distance(position, point)

            if d < best_distance:
                best_distance = d
                best_index = i

        return best_index


# =====================================================
# VOITURE
# =====================================================

class Car:

    def __init__(self, x, y, color, driver, ai=False):

        self.x = float(x)
        self.y = float(y)

        self.angle = 0
        self.speed = 0

        self.color = color
        self.driver = driver

        self.ai = ai

        self.max_speed = 390
        self.acceleration = 245
        self.braking = 390

        self.laps = 0
        self.previous_index = 0
        self.has_started = False
        self.finish_cooldown = 0

    def draw(self, screen):

        car_surface = pygame.Surface((54, 30), pygame.SRCALPHA)

        # Corps
        pygame.draw.rect(
            car_surface, self.color,
            (5, 6, 44, 18), border_radius=7
        )

        # Cockpit
        pygame.draw.rect(
            car_surface, (25, 28, 35),
            (20, 9, 15, 12), border_radius=5
        )

        # Ailerons
        pygame.draw.rect(
            car_surface, (15, 15, 18),
            (1, 3, 7, 24)
        )

        pygame.draw.rect(
            car_surface, (15, 15, 18),
            (46, 3, 7, 24)
        )

        # Roues
        for wx in (10, 38):
            pygame.draw.rect(
                car_surface, BLACK,
                (wx, 0, 9, 5)
            )
            pygame.draw.rect(
                car_surface, BLACK,
                (wx, 25, 9, 5)
            )

        rotated = pygame.transform.rotate(
            car_surface, -self.angle
        )

        rect = rotated.get_rect(
            center=(int(self.x), int(self.y))
        )

        screen.blit(rotated, rect)

    def update(self, dt, circuit, keys=None, rival=None):

        if self.ai:
            self.update_ai(dt, circuit)

        else:
            self.update_player(dt, keys)

        # Déplacement
        radians = math.radians(self.angle)

        self.x += math.cos(radians) * self.speed * dt
        self.y -= math.sin(radians) * self.speed * dt

        # Sortie de piste
        road_distance = circuit.distance_from_road(
            (self.x, self.y)
        )

        if road_distance > circuit.width / 2 - 4:
            self.speed *= max(0, 1 - 1.8*dt)

        self.speed = max(-70, min(self.max_speed, self.speed))

        # Empêcher de sortir complètement de l'écran
        self.x = max(20, min(WIDTH-20, self.x))
        self.y = max(20, min(HEIGHT-20, self.y))

        self.update_laps(circuit, dt)

    def update_player(self, dt, keys):

        if keys is None:
            return

        if keys[pygame.K_UP]:
            self.speed += self.acceleration * dt

        elif keys[pygame.K_DOWN]:
            self.speed -= self.braking * dt

        else:
            self.speed *= max(0, 1 - 0.65*dt)

        if abs(self.speed) > 8:

            steering = 155 * dt

            if keys[pygame.K_LEFT]:
                self.angle += steering * min(1, abs(self.speed)/100)

            if keys[pygame.K_RIGHT]:
                self.angle -= steering * min(1, abs(self.speed)/100)

        if keys[pygame.K_SPACE]:
            self.speed *= max(0, 1 - 2.5*dt)

    def update_ai(self, dt, circuit):

        index = circuit.nearest_index((self.x, self.y))

        target = circuit.points[
            (index + 15) % circuit.length
        ]

        desired_angle = math.degrees(
            math.atan2(
                -(target[1]-self.y),
                target[0]-self.x
            )
        )

        difference = (desired_angle - self.angle + 180) % 360 - 180

        self.angle += max(-100*dt, min(100*dt, difference))

        if abs(difference) > 65:
            target_speed = 150
        elif abs(difference) > 35:
            target_speed = 230
        else:
            target_speed = 330

        if self.speed < target_speed:
            self.speed += self.acceleration * dt
        else:
            self.speed -= 100 * dt

        self.speed = max(0, min(self.max_speed, self.speed))

    def update_laps(self, circuit, dt):

        index = circuit.nearest_index((self.x, self.y))

        if self.finish_cooldown > 0:
            self.finish_cooldown -= dt

        # Détection du passage sur la ligne de départ
        if index < 15 and self.previous_index > circuit.length - 15:

            if self.has_started and self.finish_cooldown <= 0:
                self.laps += 1
                self.finish_cooldown = 4

            self.has_started = True

        self.previous_index = index


# =====================================================
# INTERFACE
# =====================================================

def draw_button(screen, text, rect, mouse, selected=False):

    color = (190, 30, 45) if selected else (55, 58, 68)

    if rect.collidepoint(mouse):
        color = (225, 45, 55)

    pygame.draw.rect(
        screen, color, rect, border_radius=9
    )

    pygame.draw.rect(
        screen, WHITE, rect, 2, border_radius=9
    )

    draw_text(
        screen, text, FONT, WHITE,
        rect.centerx, rect.centery
    )


def menu_background(screen):

    screen.fill((17, 19, 25))

    # Décoration
    pygame.draw.rect(
        screen, (28, 30, 37),
        (0, 0, WIDTH, 105)
    )

    pygame.draw.line(
        screen, RED, (0, 105), (WIDTH, 105), 4
    )


def selection_menu():

    selected_track = 0
    selected_car = 0
    selected_driver = 0
    mode = 0
    difficulty = 1

    track_names = list(TRACKS.keys())
    car_names = list(CARS.keys())

    while True:

        mouse = pygame.mouse.get_pos()

        menu_background(SCREEN)

        draw_text(
            SCREEN, "F1 RACING",
            BIG_FONT, WHITE, WIDTH//2, 55
        )

        draw_text(
            SCREEN, "CHOISIS TON GRAND PRIX",
            FONT, YELLOW, WIDTH//2, 155
        )

        # Circuits
        draw_text(
            SCREEN, "CIRCUIT",
            FONT, WHITE, 180, 220
        )

        for i, name in enumerate(track_names):

            rect = pygame.Rect(55, 255+i*58, 250, 45)

            draw_button(
                SCREEN, name, rect, mouse,
                selected_track == i
            )

        # Ecuries
        draw_text(
            SCREEN, "ECURIE",
            FONT, WHITE, 535, 220
        )

        for i, name in enumerate(car_names):

            rect = pygame.Rect(405, 255+i*58, 250, 45)

            draw_button(
                SCREEN, name, rect, mouse,
                selected_car == i
            )

        # Pilotes
        draw_text(
            SCREEN, "PILOTE",
            FONT, WHITE, 890, 220
        )

        for i, name in enumerate(DRIVERS):

            rect = pygame.Rect(755, 255+i*42, 300, 36)

            draw_button(
                SCREEN, name, rect, mouse,
                selected_driver == i
            )

        # Mode de jeu
        draw_text(
            SCREEN, "MODE DE JEU",
            FONT, WHITE, 280, 510
        )

        solo_rect = pygame.Rect(125, 540, 220, 45)
        duo_rect = pygame.Rect(125, 595, 220, 45)

        draw_button(
            SCREEN, "SOLO VS IA",
            solo_rect, mouse, mode == 0
        )

        draw_button(
            SCREEN, "2 JOUEURS",
            duo_rect, mouse, mode == 1
        )

        # Difficulté
        draw_text(
            SCREEN, "DIFFICULTE IA",
            FONT, WHITE, 550, 510
        )

        for i, name in enumerate(["Facile", "Normal", "Difficile"]):

            rect = pygame.Rect(430+i*100, 550, 90, 45)

            draw_button(
                SCREEN, name, rect, mouse,
                difficulty == i
            )

        # Lancer
        start_rect = pygame.Rect(790, 570, 230, 70)

        draw_button(
            SCREEN, "LANCER LA COURSE",
            start_rect, mouse
        )

        draw_text(
            SCREEN,
            "Fleches : piloter | Espace : freiner | Echap : pause",
            SMALL_FONT, WHITE, WIDTH//2, 700
        )

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:

                    for i in range(4):

                        rect = pygame.Rect(55, 255+i*58, 250, 45)

                        if rect.collidepoint(event.pos):
                            selected_track = i

                    for i in range(4):

                        rect = pygame.Rect(405, 255+i*58, 250, 45)

                        if rect.collidepoint(event.pos):
                            selected_car = i

                    for i in range(8):

                        rect = pygame.Rect(755, 255+i*42, 300, 36)

                        if rect.collidepoint(event.pos):
                            selected_driver = i

                    if solo_rect.collidepoint(event.pos):
                        mode = 0

                    if duo_rect.collidepoint(event.pos):
                        mode = 1

                    for i in range(3):

                        rect = pygame.Rect(430+i*100, 550, 90, 45)

                        if rect.collidepoint(event.pos):
                            difficulty = i

                    if start_rect.collidepoint(event.pos):

                        return (
                            track_names[selected_track],
                            car_names[selected_car],
                            DRIVERS[selected_driver],
                            mode,
                            difficulty
                        )


# =====================================================
# HUD
# =====================================================

def draw_hud(screen, player, circuit, elapsed, paused):

    pygame.draw.rect(
        screen, (15, 17, 22),
        (0, 0, WIDTH, 62)
    )

    pygame.draw.line(
        screen, RED, (0, 62), (WIDTH, 62), 3
    )

    draw_text(
        screen, circuit.name,
        FONT, WHITE, 100, 30
    )

    draw_text(
        screen, player.driver,
        FONT, WHITE, 390, 30
    )

    draw_text(
        screen, "TOUR : " + str(player.laps),
        FONT, YELLOW, 690, 30
    )

    draw_text(
        screen, str(int(player.speed)) + " km/h",
        FONT, WHITE, 900, 30
    )

    minutes = int(elapsed // 60)
    seconds = elapsed % 60

    draw_text(
        screen,
        "%02d:%05.2f" % (minutes, seconds),
        FONT, WHITE, 1030, 30
    )

    if paused:

        overlay = pygame.Surface(
            (WIDTH, HEIGHT), pygame.SRCALPHA
        )

        overlay.fill((0, 0, 0, 170))
        screen.blit(overlay, (0, 0))

        draw_text(
            screen, "PAUSE",
            BIG_FONT, WHITE, WIDTH//2, HEIGHT//2 - 30
        )

        draw_text(
            screen, "Echap pour reprendre",
            FONT, WHITE, WIDTH//2, HEIGHT//2 + 35
        )


# =====================================================
# COURSE
# =====================================================

def start_race(track_name, car_name, driver, mode, difficulty):

    circuit = Circuit(track_name)

    start = circuit.points[0]
    second = circuit.points[8]

    angle = math.degrees(
        math.atan2(
            -(second[1]-start[1]),
            second[0]-start[0]
        )
    )

    player = Car(
        start[0] - 20,
        start[1] - 20,
        CARS[car_name],
        driver
    )

    player.angle = angle

    if mode == 0:

        rival = Car(
            start[0] - 70,
            start[1] + 35,
            (40, 80, 180),
            random.choice(DRIVERS),
            ai=True
        )

        rival.angle = angle

        if difficulty == 0:
            rival.max_speed = 250
        elif difficulty == 1:
            rival.max_speed = 330
        else:
            rival.max_speed = 390

    else:

        rival = Car(
            start[0] - 70,
            start[1] + 35,
            (30, 190, 180),
            "Joueur 2"
        )

        rival.angle = angle

    elapsed = 0
    paused = False

    running = True

    while running:

        dt = CLOCK.tick(FPS) / 1000
        dt = min(dt, 0.04)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    paused = not paused

                if event.key == pygame.K_BACKSPACE:
                    return

        if not paused:

            elapsed += dt

            keys = pygame.key.get_pressed()

            player.update(dt, circuit, keys)

            if mode == 0:
                rival.update(dt, circuit)
            else:
                # Joueur 2 : ZQSD
                rival_keys = {
                    pygame.K_UP: keys[pygame.K_z],
                    pygame.K_DOWN: keys[pygame.K_s],
                    pygame.K_LEFT: keys[pygame.K_q],
                    pygame.K_RIGHT: keys[pygame.K_d],
                    pygame.K_SPACE: False
                }

                class KeyWrapper:
                    def __getitem__(self, key):
                        return rival_keys.get(key, False)

                rival.update(dt, circuit, KeyWrapper())

        # Affichage
        circuit.draw(SCREEN)

        rival.draw(SCREEN)
        player.draw(SCREEN)

        draw_hud(
            SCREEN, player, circuit,
            elapsed, paused
        )

        if mode == 1:
            draw_text(
                SCREEN, "Joueur 2 : ZQSD",
                SMALL_FONT, WHITE, 120, HEIGHT-25
            )

        else:
            draw_text(
                SCREEN, "Joueur 1 : fleches",
                SMALL_FONT, WHITE, 120, HEIGHT-25
            )

        draw_text(
            SCREEN, "Retour arriere : menu",
            SMALL_FONT, WHITE, 900, HEIGHT-25
        )

        pygame.display.flip()


# =====================================================
# PROGRAMME PRINCIPAL
# =====================================================

def main():

    while True:

        settings = selection_menu()

        track_name = settings[0]
        car_name = settings[1]
        driver = settings[2]
        mode = settings[3]
        difficulty = settings[4]

        start_race(
            track_name,
            car_name,
            driver,
            mode,
            difficulty
        )


if __name__ == "__main__":
    main()


