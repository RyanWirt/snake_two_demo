import pygame
import random
import sys

# --- Constants ---
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
CELL_SIZE = 20
COLS = WINDOW_WIDTH // CELL_SIZE
ROWS = WINDOW_HEIGHT // CELL_SIZE
FPS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)
RED = (200, 0, 0)
GRAY = (40, 40, 40)
YELLOW = (255, 220, 0)


def random_food(snake_body):
    """Return a random (col, row) position not occupied by the snake."""
    while True:
        pos = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
        if pos not in snake_body:
            return pos


def draw_grid(surface):
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        pygame.draw.line(surface, GRAY, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
        pygame.draw.line(surface, GRAY, (0, y), (WINDOW_WIDTH, y))


def draw_cell(surface, col, row, color, border_color=None):
    rect = pygame.Rect(col * CELL_SIZE + 1, row * CELL_SIZE + 1,
                       CELL_SIZE - 2, CELL_SIZE - 2)
    pygame.draw.rect(surface, color, rect, border_radius=3)
    if border_color:
        pygame.draw.rect(surface, border_color, rect, width=1, border_radius=3)


def draw_snake(surface, body):
    for i, (col, row) in enumerate(body):
        color = DARK_GREEN if i == 0 else GREEN
        draw_cell(surface, col, row, color)


def draw_food(surface, pos):
    draw_cell(surface, pos[0], pos[1], RED)


def show_message(surface, font, text, sub_text=""):
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    surface.blit(overlay, (0, 0))

    msg = font.render(text, True, YELLOW)
    surface.blit(msg, msg.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30)))

    if sub_text:
        small_font = pygame.font.SysFont("monospace", 22)
        sub = small_font.render(sub_text, True, WHITE)
        surface.blit(sub, sub.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20)))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 36, bold=True)
    score_font = pygame.font.SysFont("monospace", 22)

    def reset():
        start = (COLS // 2, ROWS // 2)
        body = [start, (start[0] - 1, start[1]), (start[0] - 2, start[1])]
        direction = (1, 0)
        food = random_food(body)
        score = 0
        return body, direction, food, score

    body, direction, food, score = reset()
    next_direction = direction
    game_over = False
    paused = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if game_over:
                    if event.key == pygame.K_r:
                        body, direction, food, score = reset()
                        next_direction = direction
                        game_over = False
                        paused = False
                    continue

                if event.key == pygame.K_p:
                    paused = not paused

                if not paused:
                    if event.key in (pygame.K_UP, pygame.K_w) and direction != (0, 1):
                        next_direction = (0, -1)
                    elif event.key in (pygame.K_DOWN, pygame.K_s) and direction != (0, -1):
                        next_direction = (0, 1)
                    elif event.key in (pygame.K_LEFT, pygame.K_a) and direction != (1, 0):
                        next_direction = (-1, 0)
                    elif event.key in (pygame.K_RIGHT, pygame.K_d) and direction != (-1, 0):
                        next_direction = (1, 0)

        if not game_over and not paused:
            direction = next_direction
            head = (body[0][0] + direction[0], body[0][1] + direction[1])

            # Wall collision
            if not (0 <= head[0] < COLS and 0 <= head[1] < ROWS):
                game_over = True
            # Self collision
            elif head in body:
                game_over = True
            else:
                body.insert(0, head)
                if head == food:
                    score += 1
                    food = random_food(body)
                else:
                    body.pop()

        # --- Drawing ---
        screen.fill(BLACK)
        draw_grid(screen)
        draw_food(screen, food)
        draw_snake(screen, body)

        # Score
        score_surf = score_font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_surf, (8, 6))

        if game_over:
            show_message(screen, font, "GAME OVER",
                         f"Score: {score}   Press R to restart")
        elif paused:
            show_message(screen, font, "PAUSED", "Press P to resume")

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
