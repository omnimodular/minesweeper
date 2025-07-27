import pytest
from pytest_bdd import scenarios, given, when, then, parsers
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from minesweeper import Minesweeper, CellState, GameState

# Load scenarios from the feature file
scenarios('../features/game_initialization.feature')

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
@when('I create a default Minesweeper game')
def create_default_game(game_context):
    """Create a default 9x9 Minesweeper game with 10 mines."""
    game_context['game'] = Minesweeper()

@when('I set up the game with this board pattern')
def setup_game_with_pattern(game_context):
    """Set up the game using the board pattern from docstring."""
    pattern = game_context['board_pattern']
    game_context['game'] = Minesweeper()
    game_context['game'].setup_board_from_pattern(pattern)

@when(parsers.parse('I create a Minesweeper game with {rows:d} rows, {cols:d} columns, and {mines:d} mines'))
def create_custom_game(game_context, rows, cols, mines):
    """Create a custom Minesweeper game with specified dimensions and mines."""
    game_context['game'] = Minesweeper(rows, cols, mines)

# Then steps
@then(parsers.parse('the board should be {rows:d}x{cols:d}'))
def check_board_dimensions(game_context, rows, cols):
    """Verify the board has the correct dimensions."""
    game = game_context['game']
    assert game.rows == rows
    assert game.cols == cols

@then(parsers.parse('there should be {mines:d} mines'))
def check_mine_count(game_context, mines):
    """Verify the game has the correct number of mines."""
    game = game_context['game']
    assert game.total_mines == mines

@then(parsers.parse('there should be {mines:d} mine'))
def check_mine_count_singular(game_context, mines):
    """Verify the game has the correct number of mines (singular form)."""
    game = game_context['game']
    assert game.total_mines == mines

@then('all cells should be hidden')
def check_all_cells_hidden(game_context):
    """Verify all cells are initially hidden."""
    game = game_context['game']
    for row in range(game.rows):
        for col in range(game.cols):
            assert game.grid[row][col].state == CellState.HIDDEN

@then(parsers.parse('the game state should be "{state}"'))
def check_game_state(game_context, state):
    """Verify the game state matches expected value."""
    game = game_context['game']
    expected_state = GameState(state)
    assert game.get_game_state() == expected_state

@then(parsers.parse('the remaining mines count should be {count:d}'))
def check_remaining_mines(game_context, count):
    """Verify the remaining mines count."""
    game = game_context['game']
    assert game.get_remaining_mines() == count

@then(parsers.parse('the flags placed count should be {count:d}'))
def check_flags_placed(game_context, count):
    """Verify the flags placed count."""
    game = game_context['game']
    assert game.flags_placed == count

@then(parsers.parse('the cells revealed count should be {count:d}'))
def check_cells_revealed(game_context, count):
    """Verify the cells revealed count."""
    game = game_context['game']
    assert game.cells_revealed == count

@then('no mines should be placed yet')
def check_no_mines_placed(game_context):
    """Verify no mines are placed before first move."""
    game = game_context['game']
    mine_count = 0
    for row in range(game.rows):
        for col in range(game.cols):
            if game.grid[row][col].is_mine:
                mine_count += 1
    assert mine_count == 0
    assert game.first_move == True 
