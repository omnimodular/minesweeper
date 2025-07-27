import pytest
from pytest_bdd import scenarios, given, when, then, parsers
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from minesweeper import Minesweeper, CellState, GameState

# Load scenarios from the feature file
scenarios('../features/flagging.feature')

@pytest.fixture
def game_context():
    """Context to store game state between steps."""
    return {}

# Given steps (reuse from other tests)
@given('I want to start a new game')
def want_new_game(game_context):
    """Initialize the game context."""
    game_context['ready'] = True

@given('the board is:', target_fixture='board_pattern')
def board_pattern(docstring, game_context):
    """Store the board pattern from docstring."""
    game_context['board_pattern'] = docstring
    return docstring

@given(parsers.parse('I have a {rows:d}x{cols:d} Minesweeper game with {mines:d} mines'))
def create_custom_game(game_context, rows, cols, mines):
    """Create a custom Minesweeper game with specified dimensions and mines."""
    game_context['game'] = Minesweeper(rows, cols, mines)

@given(parsers.parse('I have flagged cell at row {row:d}, column {col:d}'))
def have_flagged_cell(game_context, row, col):
    """Pre-condition: a cell is already flagged."""
    game = game_context['game']
    game.flag(row, col)

# When steps
@when('I set up the game with this board pattern')
def setup_game_with_pattern(game_context):
    """Set up the game using the board pattern from docstring."""
    pattern = game_context['board_pattern']
    game_context['game'] = Minesweeper()
    game_context['game'].setup_board_from_pattern(pattern)

@when(parsers.parse('I flag cell at row {row:d}, column {col:d}'))
def flag_cell(game_context, row, col):
    """Flag a cell at the specified coordinates."""
    game = game_context['game']
    result = game.flag(row, col)
    game_context['last_flag_result'] = result

@when(parsers.parse('I flag cell at row {row:d}, column {col:d} again'))
def flag_cell_again(game_context, row, col):
    """Flag a cell again (to unflag it)."""
    game = game_context['game']
    result = game.flag(row, col)
    game_context['last_flag_result'] = result

@when(parsers.parse('I try to flag cell at row {row:d}, column {col:d}'))
def try_flag_cell(game_context, row, col):
    """Try to flag a cell and store the result."""
    game = game_context['game']
    result = game.flag(row, col)
    game_context['last_flag_result'] = result

@when(parsers.parse('I reveal cell at row {row:d}, column {col:d}'))
def reveal_cell(game_context, row, col):
    """Reveal a cell at the specified coordinates."""
    game = game_context['game']
    result = game.reveal(row, col)
    game_context['last_reveal_result'] = result

@when('I flag 5 different cells')
def flag_five_cells(game_context):
    """Flag 5 different cells on the board."""
    game = game_context['game']
    cells_to_flag = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1)]
    for row, col in cells_to_flag:
        if row < game.rows and col < game.cols:
            game.flag(row, col)

# Then steps
@then(parsers.parse('the cell at row {row:d}, column {col:d} should be flagged'))
def check_cell_flagged(game_context, row, col):
    """Verify that a cell is flagged."""
    game = game_context['game']
    cell = game.grid[row][col]
    assert cell.state == CellState.FLAGGED

@then(parsers.parse('the cell at row {row:d}, column {col:d} should be hidden'))
def check_cell_hidden(game_context, row, col):
    """Verify that a cell is hidden."""
    game = game_context['game']
    cell = game.grid[row][col]
    assert cell.state == CellState.HIDDEN

@then(parsers.parse('the cell at row {row:d}, column {col:d} should remain revealed'))
def check_cell_remains_revealed(game_context, row, col):
    """Verify that a cell remains revealed."""
    game = game_context['game']
    cell = game.grid[row][col]
    assert cell.state == CellState.REVEALED

@then(parsers.parse('the flags placed count should be {count:d}'))
def check_flags_placed_count(game_context, count):
    """Verify the number of flags placed."""
    game = game_context['game']
    assert game.flags_placed == count

@then(parsers.parse('the remaining mines count should be {count:d}'))
def check_remaining_mines_count(game_context, count):
    """Verify the remaining mines count."""
    game = game_context['game']
    assert game.get_remaining_mines() == count

@then('the flag operation should fail')
def check_flag_operation_failed(game_context):
    """Verify that the last flag operation failed."""
    assert game_context['last_flag_result'] == False

@then('all three cells should be flagged')
def check_three_cells_flagged(game_context):
    """Verify that three specific cells are flagged."""
    game = game_context['game']
    flagged_count = sum(1 for row in range(game.rows) 
                       for col in range(game.cols) 
                       if game.grid[row][col].state == CellState.FLAGGED)
    assert flagged_count == 3, f"Expected 3 flagged cells, found {flagged_count}"

@then('all 5 cells should be flagged')
def check_five_cells_flagged(game_context):
    """Verify that 5 cells are flagged."""
    game = game_context['game']
    flagged_count = sum(1 for row in range(game.rows) 
                       for col in range(game.cols) 
                       if game.grid[row][col].state == CellState.FLAGGED)
    assert flagged_count == 5, f"Expected 5 flagged cells, found {flagged_count}" 
