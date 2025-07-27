import pytest
from pytest_bdd import scenarios, given, when, then, parsers
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from minesweeper import Minesweeper, CellState, GameState

# Load scenarios from the feature file
scenarios('../features/win_condition_bug.feature')

@pytest.fixture
def game_context():
    """Context to store game state between steps."""
    return {}

# Given steps
@given('I want to start a new game')
def want_new_game(game_context):
    """Initialize the game context."""
    game_context['ready'] = True

@given('the board is:', target_fixture='board_pattern')
def board_pattern(docstring, game_context):
    """Store the board pattern from docstring."""
    game_context['board_pattern'] = docstring
    return docstring

# When steps
@when('I set up the game with this board pattern')
def setup_game_with_pattern(game_context):
    """Set up the game using the board pattern from docstring."""
    pattern = game_context['board_pattern']
    game_context['game'] = Minesweeper()
    game_context['game'].setup_board_from_pattern(pattern)

@when(parsers.parse('I reveal cell ({row:d},{col:d})'))
def reveal_specific_cell(game_context, row, col):
    """Reveal a specific cell at the given coordinates."""
    game = game_context['game']
    result = game.reveal(row, col)
    game_context['last_reveal_result'] = result

@when('I reveal all cells except the mine')
def reveal_all_safe_cells(game_context):
    """Reveal all cells except the mines."""
    game = game_context['game']
    for row in range(game.rows):
        for col in range(game.cols):
            if not game.grid[row][col].is_mine:
                game.reveal(row, col)

@when('I reveal some but not all safe cells')
def reveal_some_safe_cells(game_context):
    """Reveal only some safe cells, not all."""
    game = game_context['game']
    
    # Strategy: reveal specific cells that have adjacent mines (so they won't auto-reveal neighbors)
    # For the 5x5 board pattern:
    # *.*.*
    # .....
    # *.*.*
    # .....
    # *.*.*
    # 
    # Let's reveal just a few cells that have adjacent mines
    cells_to_reveal = [
        (1, 1),  # Adjacent to mines at (0,0), (0,2), (2,0), (2,2)
        (1, 3),  # Adjacent to mines at (0,2), (0,4), (2,2), (2,4)  
        (3, 1),  # Adjacent to mines at (2,0), (2,2), (4,0), (4,2)
        # Deliberately leaving other safe cells unrevealed
    ]
    
    for row, col in cells_to_reveal:
        if row < game.rows and col < game.cols:
            if not game.grid[row][col].is_mine:
                game.reveal(row, col)

# Then steps
@then(parsers.parse('the game state should be "{state}"'))
def check_game_state(game_context, state):
    """Verify the game state matches expected value."""
    game = game_context['game']
    expected_state = GameState(state)
    actual_state = game.get_game_state()
    
    # Debug information
    print(f"\nDEBUG INFO:")
    print(f"Expected state: {expected_state}")
    print(f"Actual state: {actual_state}")
    print(f"Cells revealed: {game.cells_revealed}")
    print(f"Total safe cells: {game.total_safe_cells}")
    print(f"Total mines: {game.total_mines}")
    print(f"Board dimensions: {game.rows}x{game.cols}")
    
    # Get detailed cell counts
    counts = game._get_cell_counts()
    print(f"Detailed cell counts: {counts}")
    
    # Print board state for debugging
    print("Board state:")
    for row in range(game.rows):
        row_str = ""
        for col in range(game.cols):
            cell = game.grid[row][col]
            if cell.state == CellState.REVEALED:
                if cell.is_mine:
                    row_str += "*"
                else:
                    row_str += str(cell.adjacent_mines) if cell.adjacent_mines > 0 else " "
            elif cell.state == CellState.FLAGGED:
                row_str += "x"
            else:
                row_str += "■"
        print(f"  {row_str}")
    
    assert actual_state == expected_state, f"Expected {expected_state}, but got {actual_state}"

@then('the game should be over')
def check_game_over(game_context):
    """Verify the game is over."""
    game = game_context['game']
    assert game.is_game_over()

@then('the game should not be over')
def check_game_not_over(game_context):
    """Verify the game is not over."""
    game = game_context['game']
    assert not game.is_game_over()

@then('all safe cells should be revealed')
def check_all_safe_cells_revealed(game_context):
    """Verify all safe cells are revealed."""
    game = game_context['game']
    for row in range(game.rows):
        for col in range(game.cols):
            cell = game.grid[row][col]
            if not cell.is_mine:
                assert cell.state == CellState.REVEALED, f"Safe cell at ({row}, {col}) not revealed"
