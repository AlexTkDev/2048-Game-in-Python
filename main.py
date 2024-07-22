import pygame
import random
import os
import json

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 400, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")

# Цвета
BACKGROUND_COLOR = (187, 173, 160)
TILE_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
    4096: (60, 58, 50),
    8192: (60, 58, 50),
    16384: (60, 58, 50),
    32768: (60, 58, 50),
    65536: (60, 58, 50),
    131072: (60, 58, 50)
}

FONT = pygame.font.SysFont("arial", 40)

# Инициализация переменных
grid = [[0] * 4 for _ in range(4)]
score = 0
best_score = 0
game_over = False

# Загрузка лучших результатов
if os.path.exists('../best_score.json'):
    with open('../best_score.json', 'r') as file:
        best_score = json.load(file)


def reset():
    global grid, score, game_over
    grid = [[0] * 4 for _ in range(4)]
    score = 0
    game_over = False
    add_new_tile()
    add_new_tile()


def add_new_tile():
    empty_tiles = [(r, c) for r in range(4) for c in range(4) if grid[r][c] == 0]
    if empty_tiles:
        r, c = random.choice(empty_tiles)
        grid[r][c] = 2 if random.random() < 0.9 else 4


def move_left():
    global score
    moved = False
    for row in grid:
        new_row = [i for i in row if i != 0]
        while len(new_row) < 4:
            new_row.append(0)
        for i in range(3):
            if new_row[i] == new_row[i + 1] and new_row[i] != 0:
                new_row[i] *= 2
                new_row[i + 1] = 0
                score += new_row[i]
                moved = True
        new_row = [i for i in new_row if i != 0]
        while len(new_row) < 4:
            new_row.append(0)
        for i in range(4):
            if row[i] != new_row[i]:
                moved = True
            row[i] = new_row[i]
    return moved


def move_right():
    global grid
    grid = [row[::-1] for row in grid]
    moved = move_left()
    grid = [row[::-1] for row in grid]
    return moved


def move_up():
    global grid
    grid = list(map(list, zip(*grid)))
    moved = move_left()
    grid = list(map(list, zip(*grid)))
    return moved


def move_down():
    global grid
    grid = list(map(list, zip(*grid[::-1])))
    moved = move_left()
    grid = list(map(list, zip(*grid[::-1])))
    return moved


def check_game_over():
    for row in grid:
        if 0 in row:
            return False
    for r in range(4):
        for c in range(4):
            if r < 3 and grid[r][c] == grid[r + 1][c]:
                return False
            if c < 3 and grid[r][c] == grid[r][c + 1]:
                return False
    return True


def draw_grid():
    for r in range(4):
        for c in range(4):
            value = grid[r][c]
            pygame.draw.rect(screen, TILE_COLORS[value], (c * 100, r * 100 + 100, 100, 100))
            if value != 0:
                text = FONT.render(str(value), True, (0, 0, 0))
                screen.blit(text, (c * 100 + 50 - text.get_width() // 2, r * 100 + 150 - text.get_height() // 2))


def draw_score():
    global best_score
    score_text = FONT.render(f"Score: {score}", True, (255, 255, 255))
    best_score_text = FONT.render(f"Best: {best_score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(best_score_text, (WIDTH - best_score_text.get_width() - 10, 10))


def save_best_score():
    global best_score
    if score > best_score:
        best_score = score
        with open('../best_score.json', 'w') as file:
            json.dump(best_score, file)


reset()

# Основной цикл игры
running = True
while running:
    screen.fill(BACKGROUND_COLOR)
    draw_grid()
    draw_score()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            save_best_score()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if move_left():
                    add_new_tile()
            elif event.key == pygame.K_RIGHT:
                if move_right():
                    add_new_tile()
            elif event.key == pygame.K_UP:
                if move_up():
                    add_new_tile()
            elif event.key == pygame.K_DOWN:
                if move_down():
                    add_new_tile()
            if check_game_over():
                game_over = True

    if game_over:
        screen.fill(BACKGROUND_COLOR)
        game_over_text = FONT.render("Game Over", True, (255, 0, 0))
        screen.blit(game_over_text,
                    (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(3000)
        reset()

pygame.quit()
