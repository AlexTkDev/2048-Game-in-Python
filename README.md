# 2048 Game in Python

## Description

This is an implementation of the 2048 game in Python using the Pygame library. 2048 is a puzzle game where the player slides tiles on a 4x4 grid to combine tiles of the same value to create larger value tiles. The goal of the game is to reach a tile with the value 2048 (or higher).

## Installation

1. Make sure you have Python 3 installed.
2. Download or clone the game repository.

```bash
   git clone https://github.com/AlexTkDev/game2048.git
```

4. Navigate to the game directory.
5. Install the dependencies:

```bash
   pip install -r requirements.txt
```

## Running the Game

1. Navigate to the game directory.
2. Run the `main.py` script:

```bash
    python main.py
```

## Controls

1. Left arrow: Move tiles left.
2. Right arrow: Move tiles right.
3. Up arrow: Move tiles up.
4. Down arrow: Move tiles down.

## Game Rules

1. Sliding tiles: Use the arrow keys to slide the tiles on the grid.
2. Combining tiles: When two tiles with the same value collide, they combine into one tile with double the value.
3. New tiles: After each move, a new tile with a value of 2 or 4 will appear on the grid.
4. Game over: The game ends when there are no more possible moves.

## Score Saving

The game automatically saves your best score to a file named `best_score.json`. When you restart the game, your best score will be loaded and displayed on the screen.

## Note

This project is educational and can be further developed to improve the gaming experience. You can add new features, enhance graphics and animations, and modify the game rules as you see fit.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

