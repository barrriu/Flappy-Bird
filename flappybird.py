import pygame
import random
import sys

# Inisialisasi Pygame
pygame.init()

# Konfigurasi layar
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Memuat gambar
bird_img = pygame.image.load('Asset/bird.png').convert_alpha()
pipe_img = pygame.image.load('Asset/pipe.png').convert_alpha()
background_img = pygame.image.load('Asset/background.png').convert()
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
ground_img = pygame.image.load('Asset/ground.png').convert_alpha()
ground_img = pygame.transform.scale(ground_img, (WIDTH, ground_img.get_height()))

# Ukuran burung
bird_width = bird_img.get_width()
bird_height = bird_img.get_height()

# Variabel game
bird_x = 10
bird_y = HEIGHT // 2
bird_velocity = 0
gravity = 0.5
jump_strength = -10

pipes = []
pipe_width = pipe_img.get_width()
pipe_gap = 150
pipe_frequency = 1500  # ms
last_pipe = pygame.time.get_ticks()
score = 0
font = pygame.font.SysFont("Arial", 30)
game_started = False
game_over = False

clock = pygame.time.Clock()

def draw_bird():
    screen.blit(bird_img, (bird_x, bird_y))

def draw_pipes():
    for pipe in pipes:
        # Pipa atas
        top_pipe = pygame.transform.flip(pipe_img, False, True)
        screen.blit(top_pipe, (pipe["x"], pipe["top"] - pipe_img.get_height()))
        # Pipa bawah
        screen.blit(pipe_img, (pipe["x"], pipe["bottom"]))

def move_pipes():
    for pipe in pipes:
        pipe["x"] -= 3

def check_collision():
    if bird_y < 0 or bird_y + bird_height > HEIGHT - ground_img.get_height():
        return True

    for pipe in pipes:
        if (bird_x + bird_width > pipe["x"] and bird_x < pipe["x"] + pipe_width):
            if bird_y < pipe["top"] or bird_y + bird_height > pipe["bottom"]:
                return True
    return False

def update_score():
    global score
    for pipe in pipes:
        if pipe["x"] + pipe_width < bird_x and not pipe["counted"]:
            score += 1
            pipe["counted"] = True

def reset_game():
    global bird_y, bird_velocity, pipes, score, game_started, game_over
    bird_y = HEIGHT // 2
    bird_velocity = 0
    pipes = []
    score = 0
    game_started = False
    game_over = False

# Game loop
running = True
while running:
    clock.tick(60)
    screen.blit(background_img, (0, 0))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not game_started and not game_over:
                    game_started = True
                    bird_velocity = jump_strength
                elif game_started and not game_over:
                    bird_velocity = jump_strength
                elif game_over:
                    reset_game()

    if game_started and not game_over:
        # Update burung
        bird_velocity += gravity
        bird_y += bird_velocity

        # Generate pipa
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(100, 400)
            pipes.append({
                "x": WIDTH,
                "top": pipe_height - pipe_gap // 2,
                "bottom": pipe_height + pipe_gap // 2,
                "counted": False
            })
            last_pipe = time_now

        # Gerakkan dan hapus pipa
        move_pipes()
        pipes = [pipe for pipe in pipes if pipe["x"] > -pipe_width]

        # Cek tabrakan
        if check_collision():
            game_over = True

        # Update skor
        update_score()

    # Gambar semuanya
    draw_pipes()
    screen.blit(ground_img, (0, HEIGHT - ground_img.get_height()))
    draw_bird()
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    if not game_started and not game_over:
        start_text = font.render("Press SPACE to start", True, BLACK)
        screen.blit(start_text, (WIDTH//2 - start_text.get_width()//2, HEIGHT//2))

    if game_over:
        over_text = font.render("Game Over! Press SPACE", True, BLACK)
        screen.blit(over_text, (WIDTH//2 - over_text.get_width()//2, HEIGHT//2))
        restart_text = font.render("to restart", True, BLACK)
        screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 40))

    pygame.display.update()

pygame.quit()
sys.exit()
