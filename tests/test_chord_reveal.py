import pytest
from pytest_bdd import scenarios, given, when, then, parsers
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from minesweeper import Minesweeper, CellState, GameState

# Load scenarios from the feature file
scenarios('../features/chord_reveal.feature')

@pytest.fixture
def game_context():
    """Context to store game state between steps."""
    return {}

# Given steps (reusing from existing tests)
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
def reveal_specific_cell(game_context, row, col):
    """Reveal a specific cell at the given coordinates."""
    game = game_context['game']
    result = game.reveal(row, col)
    game_context['last_reveal_result'] = result

@when(parsers.parse('I flag cell at row {row:d}, column {col:d}'))
def flag_specific_cell(game_context, row, col):
    """Flag a specific cell at the given coordinates."""
    game = game_context['game']
    result = game.flag(row, col)
    game_context['last_flag_result'] = result

@when(parsers.parse('I chord reveal cell at row {row:d}, column {col:d}'))
def chord_reveal_cell(game_context, row, col):
    """Chord reveal (middle-click reveal) a specific cell."""
    game = game_context['game']
    result = game.chord_reveal(row, col)
    game_context['last_chord_result'] = result

# Then steps
@then(parsers.parse('the cells at {coordinates} should be revealed'))
def check_multiple_cells_revealed(game_context, coordinates):
    """Verify multiple cells are revealed based on coordinate list."""
    game = game_context['game']
    
    # Parse coordinates like "(0,1), (0,2), (1,1), (1,2)"
    coord_pairs = []
    # Remove spaces and split by commas
    coords_str = coordinates.replace(' ', '')
    # Extract coordinate pairs
    import re
    matches = re.findall(r'\((\d+),(\d+)\)', coords_str)
    
    for match in matches:
        row, col = int(match[0]), int(match[1])
        cell = game.grid[row][col]
        assert cell.state == CellState.REVEALED, f"Cell at ({row}, {col}) should be revealed but is {cell.state.value}"

@then(parsers.parse('the cell at row {row:d}, column {col:d} should not be revealed'))
def check_cell_not_revealed(game_context, row, col):
    """Verify a specific cell is not revealed."""
    game = game_context['game']
    cell = game.grid[row][col]
    assert cell.state != CellState.REVEALED, f"Cell at ({row}, {col}) should not be revealed but is {cell.state.value}"

@then(parsers.parse('the cell at row {row:d}, column {col:d} should be revealed'))
def check_cell_revealed(game_context, row, col):
    """Verify a specific cell is revealed."""
    game = game_context['game']
    cell = game.grid[row][col]
    assert cell.state == CellState.REVEALED, f"Cell at ({row}, {col}) should be revealed but is {cell.state.value}"

@then(parsers.parse('the game state should be "{state}"'))
def check_game_state(game_context, state):
    """Verify the game state matches expected value."""
    game = game_context['game']
    expected_state = GameState(state)
    assert game.get_game_state() == expected_state

@then('the mine should be revealed')
def check_mine_revealed(game_context):
    """Verify that at least one mine is revealed."""
    game = game_context['game']
    mine_revealed = False
    for row in range(game.rows):
        for col in range(game.cols):
            cell = game.grid[row][col]
            if cell.is_mine and cell.state == CellState.REVEALED:
                mine_revealed = True
                break
        if mine_revealed:
            break
    assert mine_revealed, "No mine was revealed"

@then('multiple cells should be revealed by auto-reveal')
def check_multiple_cells_auto_revealed(game_context):
    """Verify that multiple cells were revealed (more than just the target)."""
    game = game_context['game']
    revealed_count = 0
    for row in range(game.rows):
        for col in range(game.cols):
            cell = game.grid[row][col]
            if cell.state == CellState.REVEALED:
                revealed_count += 1
    
    # Should have more than 2 cells revealed (the initial one plus chord targets)
    assert revealed_count > 2, f"Expected multiple cells to be auto-revealed, but only {revealed_count} are revealed"

@then('all cells should be revealed')
def check_all_cells_revealed(game_context):
    """Verify all cells on the board are revealed."""
    game = game_context['game']
    for row in range(game.rows):
        for col in range(game.cols):
            cell = game.grid[row][col]
            assert cell.state == CellState.REVEALED, f"Cell at ({row}, {col}) not revealed" 
