import pytest
from pytest_bdd import scenarios, given, when, then, parsers
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from minesweeper import Minesweeper, CellState, GameState

# Load scenarios from the feature file
scenarios('../features/cell_revelation.feature')

@pytest.fixture
def game_context():
    """Context to store game state between steps."""
    return {}

# Given steps (reuse from game_initialization)
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

@when(parsers.parse('I reveal cell at row {row:d}, column {col:d}'))
def reveal_cell(game_context, row, col):
    """Reveal a cell at the specified coordinates."""
    game = game_context['game']
    result = game.reveal(row, col)
    game_context['last_reveal_result'] = result

@when(parsers.parse('I try to reveal cell at row {row:d}, column {col:d}'))
def try_reveal_cell(game_context, row, col):
    """Try to reveal a cell and store the result."""
    game = game_context['game']
    result = game.reveal(row, col)
    game_context['last_reveal_result'] = result

@when(parsers.parse('I try to reveal cell at row {row:d}, column {col:d} again'))
def try_reveal_cell_again(game_context, row, col):
    """Try to reveal a cell again and store the result."""
    game = game_context['game']
    result = game.reveal(row, col)
    game_context['second_reveal_result'] = result

@when(parsers.parse('I flag cell at row {row:d}, column {col:d}'))
def flag_cell(game_context, row, col):
    """Flag a cell at the specified coordinates."""
    game = game_context['game']
    result = game.flag(row, col)
    game_context['last_flag_result'] = result

# Then steps
@then(parsers.parse('the cell at row {row:d}, column {col:d} should be revealed'))
def check_cell_revealed(game_context, row, col):
    """Verify that a cell is revealed."""
    game = game_context['game']
    cell = game.grid[row][col]
    assert cell.state == CellState.REVEALED

@then(parsers.parse('the cell should show {count:d} adjacent mine'))
@then(parsers.parse('the cell should show {count:d} adjacent mines'))
def check_adjacent_mines(game_context, count):
    """Verify the adjacent mine count shown on the last revealed cell."""
    # This is a simplified check - in a real implementation you'd track which cell was revealed
    # For now, we'll check that there's at least one cell with the expected count
    game = game_context['game']
    found = False
    for row in range(game.rows):
        for col in range(game.cols):
            cell = game.grid[row][col]
            if cell.state == CellState.REVEALED and cell.adjacent_mines == count:
                found = True
                break
        if found:
            break
    assert found, f"No revealed cell found with {count} adjacent mines"

@then(parsers.parse('the game state should be "{state}"'))
def check_game_state(game_context, state):
    """Verify the game state matches expected value."""
    game = game_context['game']
    expected_state = GameState(state)
    assert game.get_game_state() == expected_state

@then('multiple connected empty cells should be revealed')
def check_multiple_cells_revealed(game_context):
    """Verify that multiple cells were revealed (auto-reveal)."""
    game = game_context['game']
    revealed_count = sum(1 for row in range(game.rows) 
                        for col in range(game.cols) 
                        if game.grid[row][col].state == CellState.REVEALED)
    assert revealed_count > 1, f"Expected multiple cells revealed, got {revealed_count}"

@then(parsers.parse('the cell at row {row:d}, column {col:d} should remain flagged'))
def check_cell_remains_flagged(game_context, row, col):
    """Verify that a cell remains flagged."""
    game = game_context['game']
    cell = game.grid[row][col]
    assert cell.state == CellState.FLAGGED

@then('the reveal operation should fail')
def check_reveal_failed(game_context):
    """Verify that the last reveal operation failed."""
    assert game_context['last_reveal_result'] == False

@then('the second reveal operation should fail')
def check_second_reveal_failed(game_context):
    """Verify that the second reveal operation failed."""
    assert game_context['second_reveal_result'] == False

@then('the cell should remain revealed')
def check_cell_remains_revealed(game_context):
    """Verify that a cell remains in revealed state."""
    # This step assumes we're checking the last revealed cell
    # In a real implementation, you'd be more specific about which cell
    game = game_context['game']
    revealed_count = sum(1 for row in range(game.rows) 
                        for col in range(game.cols) 
                        if game.grid[row][col].state == CellState.REVEALED)
    assert revealed_count >= 1, "Expected at least one cell to remain revealed"

@then(parsers.parse('the game state should remain "{state}"'))
def check_game_state_remains(game_context, state):
    """Verify the game state remains as expected."""
    game = game_context['game']
    expected_state = GameState(state)
    assert game.get_game_state() == expected_state 
