import random
import json
import os
from typing import List, Tuple
from enum import Enum
from dataclasses import dataclass
import pygame


# Game constants
GRID_SIZE = 4
TILE_SIZE = 100
SCORE_PANEL_HEIGHT = 100
WIDTH = GRID_SIZE * TILE_SIZE
HEIGHT = GRID_SIZE * TILE_SIZE + SCORE_PANEL_HEIGHT
SCORE_FILE = 'best_score.json'


# Colors
@dataclass
class Colors:
    BACKGROUND = (187, 173, 160)
    GAME_OVER_OVERLAY = (255, 255, 255, 128)
    TEXT_DARK = (119, 110, 101)
    TEXT_LIGHT = (249, 246, 242)
    SCORE_TEXT = (255, 255, 255)
    GAME_OVER_TEXT = (255, 0, 0)

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
    }

    @classmethod
    def get_tile_color(cls, value: int) -> Tuple[int, int, int]:
        return cls.TILE_COLORS.get(value, cls.TILE_COLORS[4096])

    @classmethod
    def get_text_color(cls, value: int) -> Tuple[int, int, int]:
        return cls.TEXT_LIGHT if value > 4 else cls.TEXT_DARK


class Direction(Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3


class GameState(Enum):
    PLAYING = 0
    GAME_OVER = 1
    PAUSED = 2


class ScoreManager:
    """Manages game scores and persistence"""

    def __init__(self):
        self.current_score = 0
        self.best_score = self._load_best_score()

    def _load_best_score(self) -> int:
        """Load best score from file"""
        try:
            if os.path.exists(SCORE_FILE):
                with open(SCORE_FILE, 'r') as file:
                    return json.load(file)
        except (json.JSONDecodeError, OSError) as e:
            print(f"Error loading best score: {e}")
        return 0

    def _save_best_score(self) -> None:
        """Save best score to file"""
        try:
            with open(SCORE_FILE, 'w') as file:
                json.dump(self.best_score, file)
        except OSError as e:
            print(f"Error saving best score: {e}")

    def add_score(self, points: int) -> None:
        """Add points to current score"""
        self.current_score += points
        if self.current_score > self.best_score:
            self.best_score = self.current_score
            self._save_best_score()

    def reset_current_score(self) -> None:
        """Reset current score to 0"""
        self.current_score = 0

    def get_scores(self) -> Tuple[int, int]:
        """Get current and best scores"""
        return self.current_score, self.best_score


class Game2048:
    """Core game logic for 2048"""

    def __init__(self):
        self.grid: List[List[int]] = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.score_manager = ScoreManager()
        self.state = GameState.PLAYING
        self.reset()

    def reset(self) -> None:
        """Reset game to initial state"""
        self.grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.score_manager.reset_current_score()
        self.state = GameState.PLAYING
        self._add_random_tile()
        self._add_random_tile()

    def _add_random_tile(self) -> bool:
        """Add a random tile (2 or 4) to an empty cell"""
        empty_cells = [(r, c) for r in range(GRID_SIZE)
                       for c in range(GRID_SIZE) if self.grid[r][c] == 0]

        if not empty_cells:
            return False

        row, col = random.choice(empty_cells)
        self.grid[row][col] = 2 if random.random() < 0.9 else 4
        return True

    def _rotate_grid_clockwise(self) -> None:
        """Rotate grid 90 degrees clockwise"""
        self.grid = [[self.grid[GRID_SIZE - 1 - j][i]
                      for j in range(GRID_SIZE)] for i in range(GRID_SIZE)]

    def _move_left(self) -> bool:
        """Move all tiles left and combine identical adjacent tiles"""
        moved = False

        for row in self.grid:
            # Remove zeros and slide left
            non_zero = [cell for cell in row if cell != 0]

            # Combine identical adjacent tiles
            combined = []
            i = 0
            while i < len(non_zero):
                if i + 1 < len(non_zero) and non_zero[i] == non_zero[i + 1]:
                    # Combine tiles
                    combined_value = non_zero[i] * 2
                    combined.append(combined_value)
                    self.score_manager.add_score(combined_value)
                    i += 2  # Skip next tile as it's been combined
                else:
                    combined.append(non_zero[i])
                    i += 1

            # Pad with zeros
            new_row = combined + [0] * (GRID_SIZE - len(combined))

            # Check if row changed
            if row != new_row:
                moved = True
                row[:] = new_row

        return moved

    def move(self, direction: Direction) -> bool:
        """Move tiles in specified direction"""
        if self.state != GameState.PLAYING:
            return False

        # Rotate grid to make all moves equivalent to left move
        rotations = {
            Direction.LEFT: 0,
            Direction.DOWN: 1,
            Direction.RIGHT: 2,
            Direction.UP: 3
        }

        # Rotate to desired direction
        for _ in range(rotations[direction]):
            self._rotate_grid_clockwise()

        # Execute left move
        moved = self._move_left()

        # Rotate back
        for _ in range(4 - rotations[direction]):
            self._rotate_grid_clockwise()

        if moved:
            if not self._add_random_tile():
                # No empty cells, check if game over
                if self._is_game_over():
                    self.state = GameState.GAME_OVER

        return moved

    def _is_game_over(self) -> bool:
        """Check if no more moves are possible"""
        # Check for empty cells
        for row in self.grid:
            if 0 in row:
                return False

        # Check for possible horizontal merges
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE - 1):
                if self.grid[r][c] == self.grid[r][c + 1]:
                    return False

        # Check for possible vertical merges
        for r in range(GRID_SIZE - 1):
            for c in range(GRID_SIZE):
                if self.grid[r][c] == self.grid[r + 1][c]:
                    return False

        return True

    def get_grid(self) -> List[List[int]]:
        """Get current grid state"""
        return [row[:] for row in self.grid]  # Return copy

    def get_state(self) -> GameState:
        """Get current game state"""
        return self.state

    def has_won(self) -> bool:
        """Check if player has reached 2048"""
        for row in self.grid:
            if 2048 in row:
                return True
        return False


class GameRenderer:
    """Handles all game rendering"""

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font_large = pygame.font.SysFont("arial", 36, bold=True)
        self.font_medium = pygame.font.SysFont("arial", 24, bold=True)
        self.font_small = pygame.font.SysFont("arial", 18)

    def _get_tile_font_size(self, value: int) -> pygame.font.Font:
        """Get appropriate font size based on tile value"""
        if value < 100:
            return self.font_large
        elif value < 1000:
            return self.font_medium
        else:
            return self.font_small

    def draw_tile(self, value: int, x: int, y: int) -> None:
        """Draw a single tile"""
        # Draw tile background
        color = Colors.get_tile_color(value)
        pygame.draw.rect(self.screen, color, (x, y, TILE_SIZE, TILE_SIZE))
        pygame.draw.rect(self.screen, Colors.BACKGROUND, (x, y, TILE_SIZE, TILE_SIZE), 2)

        # Draw tile value
        if value != 0:
            font = self._get_tile_font_size(value)
            text_color = Colors.get_text_color(value)
            text = font.render(str(value), True, text_color)
            text_rect = text.get_rect(center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2))
            self.screen.blit(text, text_rect)

    def draw_grid(self, grid: List[List[int]]) -> None:
        """Draw the entire game grid"""
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                x = col * TILE_SIZE
                y = row * TILE_SIZE + SCORE_PANEL_HEIGHT
                self.draw_tile(grid[row][col], x, y)

    def draw_score_panel(self, current_score: int, best_score: int) -> None:
        """Draw score panel at the top"""
        # Clear score panel area
        score_rect = pygame.Rect(0, 0, WIDTH, SCORE_PANEL_HEIGHT)
        pygame.draw.rect(self.screen, Colors.BACKGROUND, score_rect)

        # Draw current score
        score_text = self.font_medium.render(f"Score: {current_score}", True, Colors.SCORE_TEXT)
        self.screen.blit(score_text, (10, 20))

        # Draw best score
        best_text = self.font_medium.render(f"Best: {best_score}", True, Colors.SCORE_TEXT)
        best_rect = best_text.get_rect()
        best_rect.topright = (WIDTH - 10, 20)
        self.screen.blit(best_text, best_rect)

        # Draw instructions
        instruction_text = self.font_small.render("Use arrow keys to play • R to restart", True,
                                                  Colors.SCORE_TEXT)
        instruction_rect = instruction_text.get_rect(center=(WIDTH // 2, 70))
        self.screen.blit(instruction_text, instruction_rect)

    def draw_game_over_overlay(self) -> None:
        """Draw game over overlay"""
        # Semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # Game over text
        game_over_text = self.font_large.render("Game Over!", True, Colors.GAME_OVER_TEXT)
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
        self.screen.blit(game_over_text, game_over_rect)

        # Restart instruction
        restart_text = self.font_medium.render("Press R to restart", True, Colors.SCORE_TEXT)
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
        self.screen.blit(restart_text, restart_rect)

    def draw_win_overlay(self) -> None:
        """Draw win overlay when player reaches 2048"""
        # Semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(150)
        overlay.fill((255, 215, 0))  # Gold color
        self.screen.blit(overlay, (0, 0))

        # Win text
        win_text = self.font_large.render("You Win!", True, (255, 255, 255))
        win_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
        self.screen.blit(win_text, win_rect)

        # Continue instruction
        continue_text = self.font_medium.render("Press SPACE to continue or R to restart", True,
                                                (255, 255, 255))
        continue_rect = continue_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
        self.screen.blit(continue_text, continue_rect)


class GameEventHandler:
    """Handles game input events"""

    KEY_MAP = {
        pygame.K_LEFT: Direction.LEFT,
        pygame.K_RIGHT: Direction.RIGHT,
        pygame.K_UP: Direction.UP,
        pygame.K_DOWN: Direction.DOWN,
        pygame.K_a: Direction.LEFT,
        pygame.K_d: Direction.RIGHT,
        pygame.K_w: Direction.UP,
        pygame.K_s: Direction.DOWN
    }

    @staticmethod
    def handle_keydown(event: pygame.event.Event, game: Game2048) -> bool:
        """Handle keydown events. Returns True if game should continue running."""
        if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
            return False

        elif event.key == pygame.K_r:
            game.reset()

        elif event.key in GameEventHandler.KEY_MAP:
            direction = GameEventHandler.KEY_MAP[event.key]
            game.move(direction)

        return True


class Game2048App:
    """Main application class"""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("2048 - Refactored")

        self.clock = pygame.time.Clock()
        self.game = Game2048()
        self.renderer = GameRenderer(self.screen)
        self.running = True
        self.show_win_message = False

    def handle_events(self) -> None:
        """Handle all pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                # Check if player won and handle win state
                if self.game.has_won() and not self.show_win_message:
                    self.show_win_message = True
                    if event.key == pygame.K_SPACE:
                        self.show_win_message = False
                    elif event.key == pygame.K_r:
                        self.game.reset()
                        self.show_win_message = False
                else:
                    if not GameEventHandler.handle_keydown(event, self.game):
                        self.running = False

    def update(self) -> None:
        """Update game state"""
        # Game logic is handled in event processing
        pass

    def render(self) -> None:
        """Render the game"""
        # Clear screen
        self.screen.fill(Colors.BACKGROUND)

        # Draw score panel
        current_score, best_score = self.game.score_manager.get_scores()
        self.renderer.draw_score_panel(current_score, best_score)

        # Draw game grid
        self.renderer.draw_grid(self.game.get_grid())

        # Draw overlays
        if self.show_win_message:
            self.renderer.draw_win_overlay()
        elif self.game.get_state() == GameState.GAME_OVER:
            self.renderer.draw_game_over_overlay()

        # Update display
        pygame.display.flip()

    def run(self) -> None:
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)  # 60 FPS

        pygame.quit()


def main():
    """Entry point"""
    try:
        app = Game2048App()
        app.run()
    except Exception as e:
        print(f"Error running game: {e}")
        pygame.quit()


if __name__ == "__main__":
    main()
