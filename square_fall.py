import pygame
import random
import sys

# 1. Initialisierung
pygame.init()

# Fenster-Einstellungen
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GD Square Fall - v1.0")

# Farben (GreenData Style)
BLACK = (5, 5, 5)
GREEN = (0, 255, 65)
RED = (200, 0, 0)
WHITE = (255, 255, 255)

# 2. Spiel-Variablen
player_size = 50
player_pos = [WIDTH // 2, HEIGHT - player_size - 20]

enemy_size = 50
enemy_pos = [random.randint(0, WIDTH - enemy_size), 0]
enemy_list = [enemy_pos]

speed = 10
score = 0

clock = pygame.time.Clock()
font = pygame.font.SysFont("monospace", 35)

# 3. Funktionen
def set_level(score, speed):
    if score < 20:
        speed = 5
    elif score < 40:
        speed = 8
    else:
        speed = 12
    return speed

def drop_enemies(enemy_list):
    delay = random.random()
    if len(enemy_list) < 10 and delay < 0.1:
        x_pos = random.randint(0, WIDTH - enemy_size)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])

def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        pygame.draw.rect(screen, RED, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))

def update_enemy_positions(enemy_list, score):
    for idx, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >= 0 and enemy_pos[1] < HEIGHT:
            enemy_pos[1] += speed
        else:
            enemy_list.pop(idx)
            score += 1
    return score

def collision_check(enemy_list, player_pos):
    for enemy_pos in enemy_list:
        if detect_collision(player_pos, enemy_pos):
            return True
    return False

def detect_collision(player_pos, enemy_pos):
    p_x, p_y = player_pos
    e_x, e_y = enemy_pos

    if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x + enemy_size)):
        if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y + enemy_size)):
            return True
    return False

# 4. Main Game Loop
game_over = False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # Steuerung
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= 10
    if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_size:
        player_pos[0] += 10

    # Hintergrund & Logik
    screen.fill(BLACK)
    
    drop_enemies(enemy_list)
    score = update_enemy_positions(enemy_list, score)
    speed = set_level(score, speed)

    # Score Anzeige
    text = "Score: " + str(score)
    label = font.render(text, 1, WHITE)
    screen.blit(label, (WIDTH - 200, HEIGHT - 40))

    if collision_check(enemy_list, player_pos):
        game_over = True
        break

    # Zeichnen
    draw_enemies(enemy_list)
    pygame.draw.rect(screen, GREEN, (player_pos[0], player_pos[1], player_size, player_size))

    clock.tick(30)
    pygame.display.update()

print(f"Game Over! Dein Score: {score}")