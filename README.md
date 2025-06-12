# 2048 Game in Python - Refactored Edition

## Description

This is a fully refactored implementation of the classic 2048 puzzle game in Python using Pygame.
The game features a clean, modular architecture with improved performance, better user experience,
and robust error handling.

In 2048, players slide numbered tiles on a 4×4 grid to combine tiles with the same value, creating
larger numbers. The goal is to reach the tile with value 2048 (or beyond).

## ✨ Key Features

- **Modern Architecture**: Object-oriented design with separate classes for game logic, rendering,
  and score management
- **Enhanced UX**: Victory and game over overlays with clear instructions
- **Flexible Controls**: Support for both arrow keys and WASD
- **Robust Score System**: Persistent best score with error handling
- **Performance Optimized**: 60 FPS gameplay with efficient algorithms
- **Type Safety**: Full type hints for better code reliability
- **Extensible Design**: Easy to add new features like animations or themes

## Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/AlexTkDev/game2048.git
   cd game2048
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Game

```bash
python main.py
```

## 🎮 Controls

### Movement

- **Arrow Keys**: ←/↑/↓/→ to move tiles
- **WASD Keys**: W/A/S/D as alternative movement controls

### Game Controls

- **R Key**: Restart the game
- **ESC/Q Key**: Quit the game
- **Space**: Continue playing after reaching 2048

## 🎯 Game Rules

1. **Movement**: Use controls to slide all tiles in the chosen direction
2. **Combining**: When two tiles with identical numbers collide, they merge into one tile with
   double the value
3. **New Tiles**: After each move, a new tile (2 or 4) appears in a random empty spot
4. **Victory**: Reach the 2048 tile to win (you can continue playing for higher scores)
5. **Game Over**: When no more moves are possible, the game ends

## 🏆 Scoring System

- **Points**: Earned by combining tiles (equal to the new tile's value)
- **Best Score**: Automatically saved and persists between game sessions
- **File Storage**: Scores saved in `best_score.json` with error handling

## 🏗️ Architecture

The refactored codebase follows modern software engineering principles:

### Core Components

- **`Game2048`**: Main game logic and state management
- **`GameRenderer`**: All visual rendering and display logic
- **`ScoreManager`**: Score tracking and persistence
- **`GameEventHandler`**: Input processing and event management
- **`Game2048App`**: Application orchestration and main game loop

### Design Patterns

- **Separation of Concerns**: Each class has a single responsibility
- **State Management**: Clear game states (Playing, Game Over, etc.)
- **Error Handling**: Comprehensive exception handling for file operations
- **Type Safety**: Full type annotations for better maintainability

## 🎨 Customization

The game is designed for easy customization:

- **Colors**: Modify the `Colors` dataclass for different themes
- **Grid Size**: Change `GRID_SIZE` constant (requires UI adjustments)
- **Tile Values**: Extend `TILE_COLORS` dictionary for higher numbers
- **Controls**: Add new key mappings in `GameEventHandler.KEY_MAP`

## 🚀 Future Enhancements

The modular architecture makes it easy to add:

- Smooth tile animations
- Sound effects and music
- Multiple grid sizes (3×3, 5×5, etc.)
- Undo functionality
- Online leaderboards
- Custom themes and skins
- Mobile touch controls

## 🧪 Development

### Code Quality

- **Type Hints**: Full typing support for better IDE integration
- **Error Handling**: Robust exception management
- **Performance**: Optimized algorithms and 60 FPS rendering
- **Documentation**: Comprehensive docstrings and comments

### Testing

The modular design enables easy unit testing of individual components:

- Game logic testing
- Score management verification
- Renderer component testing

## 📝 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! The refactored architecture makes it easy to:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 🐛 Bug Reports

Found a bug? Please create an issue with:

- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior

## 📊 Technical Requirements

- **Python**: 3.7+
- **Pygame**: 2.6.0
- **Memory**: ~10MB RAM
- **Storage**: <1MB disk space

---

**Enjoy playing 2048!** 🎮

*This refactored version provides a solid foundation for further development while maintaining the
classic 2048 gameplay experience.*