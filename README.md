# Minesweeper Game

A complete Python implementation of the classic Minesweeper game with comprehensive BDD (Behavior-Driven Development) tests and a clean Text User Interface (TUI).

## Project Structure

```
minesweeper/
├── features/           # BDD feature files (Gherkin scenarios)
├── tests/             # Test implementations and step definitions
├── src/               # Source code
│   ├── minesweeper.py # Core game logic
│   ├── tui.py         # Text User Interface
│   └── main.py        # Entry point with dependency injection
└── README.md          # This file
```

## Architecture

This project demonstrates **dependency injection** with a clean separation of concerns:

- **Game Logic** (`minesweeper.py`): Pure business logic, UI-agnostic
- **TUI** (`tui.py`): Text interface that depends on game logic
- **Main** (`main.py`): Entry point that injects game into TUI

## Features

- **Complete Minesweeper Logic**: Cell revelation, mine placement, flagging, win/lose detection
- **Smart Mine Placement**: First click is always safe (for random games)
- **Explicit Board Patterns**: Support for predefined mine layouts using Gherkin docstrings
- **Auto-reveal**: Empty areas expand automatically  
- **Beautiful TUI**: Modern text interface with emojis and clear formatting
- **Multiple Difficulties**: Easy, Medium, Hard, and Custom board sizes
- **BDD Test Coverage**: Comprehensive behavioral tests using pytest-bdd

## Installation

```bash
# Clone or navigate to project directory
cd minesweeper

# Install dependencies (if using virtual environment)
pip install pytest pytest-bdd

# Or install from requirements
pip install -r requirements.txt
```

## Usage

### Playing the Game

```bash
# Run the main game with TUI
python src/main.py
```

### Game Features

- **🚩 Flag/Unflag**: Mark suspected mine locations
- **💣 Mine Detection**: Numbers show adjacent mine counts  
- **🎯 Multiple Difficulties**: Easy (9x9), Medium (16x16), Hard (16x30)
- **🎮 Game Controls**: New game, quit, custom board sizes

### Commands in TUI

- `r <row> <col>` - Reveal cell at position
- `f <row> <col>` - Toggle flag at position  
- `n` - Start new game
- `q` - Quit game

### Programmatic Usage

```python
from src.minesweeper import Minesweeper
from src.tui import MinsweeperTUI

# Create game (dependency)
game = Minesweeper(9, 9, 10)

# Inject into TUI (dependent)
tui = MinsweeperTUI(game)
tui.run()

# Or use explicit board patterns
game.setup_board_from_pattern("""
*..
.*.
..*
""")
```

### Running BDD Tests

```bash
# Run all BDD tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run specific feature
pytest tests/test_game_initialization.py -v
```

## BDD Feature Examples

The project uses Gherkin scenarios with explicit board patterns:

```gherkin
Scenario: Initialize game with explicit board pattern
  Given I want to start a new game
  And the board is:
    """
    *..
    .*.
    ..*
    """
  When I set up the game with this board pattern
  Then the board should be 3x3
  And there should be 3 mines
```

## Game Rules

1. **Objective**: Clear all cells without mines
2. **Numbers**: Show count of adjacent mines (1-8)
3. **Mines**: Hitting a mine ends the game
4. **Flags**: Mark suspected mine locations
5. **Auto-reveal**: Clicking empty cells reveals connected areas
6. **Win Condition**: All non-mine cells revealed

## BDD Test Coverage

The test suite covers:
- ✅ Game initialization and board setup
- ✅ Explicit board pattern setup  
- ✅ Cell revelation mechanics
- ✅ Mine placement and detection
- ✅ Flag/unflag operations
- ✅ Win/lose condition detection
- ✅ Auto-reveal functionality
- ✅ Edge cases and error handling

## Architecture Benefits

**Dependency Injection Pattern:**
- Game logic is pure and testable
- TUI can be easily replaced (GUI, web, etc.)
- Clean separation of concerns
- Follows SOLID principles

**Single File Design:**
- Simple structure without over-engineering
- Easy to understand and maintain
- Clear dependency flow

## TUI Testing Design

To implement BDD tests for the TUI, we need to separate the TUI logic from external dependencies (ncurses, OS layer). This requires architectural segregation between:

### Current TUI Architecture
```
TUI Logic + ncurses calls + Input handling (tightly coupled)
```

### Proposed Testable TUI Architecture
```
TUI Logic ←→ Display Interface ←→ ncurses Implementation
     ↑              ↑                      ↑
     |              |                   Production
     |              └── Mock Implementation
     |                        ↑
     └── BDD Tests ───────────┘
```

### Key Abstractions Needed

**1. Display Interface**
```python
class DisplayInterface:
    def clear_screen(self)
    def draw_text(self, row, col, text, color)
    def draw_board(self, board_data)
    def show_status(self, status_data)
    def refresh(self)
```

**2. Input Interface**
```python
class InputInterface:
    def get_key(self) -> int
    def is_key_pressed(self, key) -> bool
```

**3. TUI State Management**
```python
class TUIState:
    cursor_position: Tuple[int, int]
    display_mode: str
    current_screen: str
    
    def move_cursor(self, direction)
    def handle_action(self, action)
    def get_display_data(self) -> dict
```

### BDD Testing Strategy

**Given/When/Then for TUI:**
```gherkin
Feature: TUI Navigation
  Scenario: Moving cursor with arrow keys
    Given the TUI is displaying a 3x3 board
    And the cursor is at position (0,0)
    When I press the right arrow key
    Then the cursor should be at position (0,1)
    And the display should highlight the new position

  Scenario: Revealing a cell with keyboard
    Given the TUI is displaying a board with a mine at (1,1)
    And the cursor is at position (1,1)
    When I press 'r' to reveal
    Then the game should end
    And the TUI should display "GAME OVER"
```

**Test Implementation Pattern:**
```python
def test_cursor_movement():
    # Arrange
    game = Minesweeper(3, 3, 1)
    mock_display = MockDisplay()
    mock_input = MockInput(['KEY_RIGHT'])
    tui = TUILogic(game, mock_display, mock_input)
    
    # Act
    tui.handle_input()
    
    # Assert
    assert tui.cursor_position == (0, 1)
    assert mock_display.highlighted_cell == (0, 1)
```

### Implementation Benefits

**Testability:**
- Mock external dependencies (ncurses, keyboard)
- Test TUI logic in isolation
- Verify display state without rendering
- Simulate user input programmatically

**Separation of Concerns:**
- TUI logic focuses on state management
- Display layer handles rendering
- Input layer handles OS interaction
- Clean interfaces between layers

**BDD Coverage:**
- Navigation behavior
- Visual feedback
- Keyboard shortcuts
- Game state display
- Error handling
- User experience flows

This design enables comprehensive BDD testing of the TUI while maintaining the current simple architecture for production use.

## API Reference

### Core Classes

- `Minesweeper(rows=9, cols=9, mines=10)` - Main game class
- `MinsweeperTUI(game)` - Text user interface
- `CellState` - Enum: HIDDEN, REVEALED, FLAGGED  
- `GameState` - Enum: PLAYING, WON, LOST

### Key Methods

- `game.reveal(row, col) -> bool` - Reveal cell, returns success
- `game.flag(row, col) -> bool` - Toggle flag, returns success
- `game.setup_board_from_pattern(pattern)` - Set explicit board layout
- `game.get_game_state() -> GameState` - Current game status
- `game.reset()` - Start fresh game
- `tui.run()` - Start the text interface

## Dependencies

- **Runtime**: Python 3.7+ (uses standard library only)
- **Testing**: pytest, pytest-bdd
- **Development**: No additional dependencies

## License

This project is open source and available under the MIT License.
