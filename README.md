# Minesweeper Game

A complete Python implementation of the classic Minesweeper game with comprehensive BDD (Behavior-Driven Development) tests and a clean Text User Interface (TUI).

## Project Structure

```
minesweeper/
├── features/          # BDD feature files (Gherkin scenarios)
├── tests/             # Test implementations and step definitions
├── src/minesweeper/   # Installable Python package
│   ├── __init__.py    # Public game API
│   ├── game.py        # Core game logic
│   ├── tui.py         # Text User Interface
│   └── main.py        # Console entry point with dependency injection
├── pyproject.toml     # Package metadata, dependencies, and pytest configuration
└── README.md          # This file
```

## Architecture

This project demonstrates **dependency injection** with a clean separation of concerns:

- **Game Logic** (`game.py`): Pure business logic, UI-agnostic
- **TUI** (`tui.py`): Text interface that depends on game logic
- **Main** (`main.py`): Entry point that injects game into TUI

## Features

- **Complete Minesweeper Logic**: Cell revelation, mine placement, flagging, win/lose detection
- **Chord Reveal**: Advanced middle-click reveal feature from minesweeperonline.com
- **Smart Mine Placement**: First click is always safe (for random games)
- **Explicit Board Patterns**: Support for predefined mine layouts using Gherkin docstrings
- **Auto-reveal**: Empty areas expand automatically with cascade detection
- **Complete Board Revelation**: All mines revealed automatically upon winning
- **Beautiful TUI**: Modern text interface with emojis and clear formatting
- **Multiple Difficulties**: Easy, Medium, Hard, and Custom board sizes
- **Comprehensive BDD Test Coverage**: 41 behavioral tests including chord reveal scenarios

## Installation

```bash
# Clone or navigate to project directory
cd minesweeper

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install the package with test and lint dependencies
python3 -m pip install -e '.[test,lint]'
```

All dependencies are declared in `pyproject.toml`. For a game-only installation,
use `python3 -m pip install .` in your active environment.

## Usage

### Playing the Game

```bash
# Run the installed command with the virtual environment activated
minesweeper
```

### Game Features

- **🚩 Flag/Unflag**: Mark suspected mine locations
- **💣 Mine Detection**: Numbers show adjacent mine counts
- **⚡ Chord Reveal**: Middle-click reveal for advanced play
- **🔄 Auto-Reveal**: Empty areas expand automatically
- **🎯 Multiple Difficulties**: Easy (9x9), Medium (16x16), Hard (16x30)
- **🎮 Game Controls**: New game, quit, custom board sizes
- **🏆 Complete Victory**: All mines revealed upon winning

### Commands in TUI

- `r <row> <col>` - Reveal cell at position
- `f <row> <col>` - Toggle flag at position
- `c <row> <col>` - Chord reveal (middle-click reveal) at position
- `n` - Start new game
- `q` - Quit game

### Programmatic Usage

```python
import curses

from minesweeper import Minesweeper
from minesweeper.tui import MinesweeperTUI

# Create game (dependency)
game = Minesweeper(9, 9, 10)

# Inject into TUI (dependent)
tui = MinesweeperTUI(game)
curses.wrapper(tui.run)

# Or use explicit board patterns
game.setup_board_from_pattern("""
*..
.*.
..*
""")
```

### Running BDD Tests

```bash
# Run all BDD tests with the virtual environment activated
python3 -m pytest

# Run with verbose output
python3 -m pytest -v

# Run a specific feature
python3 -m pytest tests/test_game_initialization.py -v
```

Run Ruff and Pylint over the source and tests:

```bash
python3 -m ruff check src tests
python3 -m pylint src tests
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

## Game Logic & Rules

### Basic Rules

1. **Objective**: Clear all cells without mines
2. **Numbers**: Show count of adjacent mines (1-8)
3. **Mines**: Hitting a mine ends the game
4. **Flags**: Mark suspected mine locations
5. **Auto-reveal**: Clicking empty cells reveals connected areas
6. **Win Condition**: All non-mine cells revealed

### Advanced Features

#### Chord Reveal (Middle-Click Reveal)
A powerful feature inspired by minesweeperonline.com that allows quick revealing of multiple cells:

**How it works:**
1. Reveal a numbered cell (e.g., showing "3")
2. Flag exactly 3 adjacent cells where you think mines are
3. Chord reveal the numbered cell to instantly reveal all remaining unflagged neighbors
4. If your flags are correct, safe cells are revealed
5. If you flagged incorrectly and there's a mine in unflagged neighbors, you lose!

**Usage:**
```python
# After revealing and flagging around a numbered cell
game.chord_reveal(row, col)  # Returns True if successful, False if hit mine
```

**Safety Features:**
- Only works on already revealed cells
- Only activates when flag count matches the cell's number
- Fails safely if wrong number of flags
- Properly handles mine hits and game state transitions

#### Smart Mine Placement
- **First Click Protection**: First revealed cell is guaranteed safe
- **Neighbor Protection**: First click's neighbors are also mine-free
- **Random Distribution**: Mines placed randomly in remaining safe areas

#### Auto-Reveal Mechanics
- **Empty Cell Cascade**: Revealing a cell with 0 adjacent mines automatically reveals all connected empty areas
- **Boundary Detection**: Auto-reveal stops at numbered cells (mine boundaries)
- **Recursive Algorithm**: Uses flood-fill algorithm for efficient area revelation

#### Win Detection & Board Revelation
- **Automatic Detection**: Game instantly detects when all safe cells are revealed
- **Complete Board Reveal**: Upon winning, all mines are automatically revealed
- **State Management**: Game state transitions cleanly between PLAYING, WON, and LOST

### Game Flow Examples

#### Standard Play
```
1. game.reveal(4, 4)     # Safe first click
2. game.flag(3, 3)       # Mark suspected mine
3. game.reveal(5, 5)     # Reveal another cell
4. game.chord_reveal(4, 4) # Quick reveal if flags match
```

#### Pattern-Based Setup
```python
game.setup_board_from_pattern("""
*...*
.1.1.
..2..
.1.1.
*...*
""")
# Numbers calculated automatically
# Adjacent mine counts computed
```

## BDD Test Coverage

The test suite covers:
- ✅ Game initialization and board setup
- ✅ Explicit board pattern setup  
- ✅ Cell revelation mechanics
- ✅ Mine placement and detection
- ✅ Flag/unflag operations
- ✅ **Chord reveal functionality** (8 comprehensive scenarios)
- ✅ Win/lose condition detection with complete board revelation
- ✅ Auto-reveal functionality and cascading
- ✅ Edge cases and error handling

### Chord Reveal Test Coverage
- ✅ Correct flags reveal adjacent cells
- ✅ Incorrect flag count prevents activation
- ✅ Works only on revealed cells
- ✅ Mine hits properly end game
- ✅ Mixed flagging scenarios
- ✅ Triggers auto-reveal cascades
- ✅ Can complete the game (win condition)

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
- `MinesweeperTUI(game)` - Text user interface
- `CellState` - Enum: HIDDEN, REVEALED, FLAGGED  
- `GameState` - Enum: PLAYING, WON, LOST

### Key Methods

#### Core Game Actions
- `game.reveal(row, col) -> bool` - Reveal cell, returns success
- `game.flag(row, col) -> bool` - Toggle flag, returns success
- `game.chord_reveal(row, col) -> bool` - Chord reveal (middle-click), returns success

#### Game Setup & State
- `game.setup_board_from_pattern(pattern)` - Set explicit board layout
- `game.get_game_state() -> GameState` - Current game status (PLAYING/WON/LOST)
- `game.reset()` - Start fresh game
- `game.reveal_all_mines()` - Reveal all mines (called automatically on win)

#### Game Information
- `game.get_remaining_mines() -> int` - Mines remaining (total - flags)
- `game.is_game_over() -> bool` - Check if game ended
- `game.get_cell_info(row, col) -> dict` - Get cell details

#### TUI Interface
- `tui.run()` - Start the text interface

## Dependencies

- **Runtime**: Python 3.7+ (uses standard library only)
- **Testing**: pytest and pytest-bdd, installed through the `test` extra
- **Linting**: Ruff and Pylint, installed through the `lint` extra
