import pytest
from pytest_bdd import scenarios, given, when, then, parsers
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from minesweeper import Minesweeper, CellState, GameState

# Load scenarios from the feature file
scenarios('../features/win_lose_conditions.feature')

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

@given(parsers.parse('I have a {rows:d}x{cols:d} Minesweeper game with {mines:d} mine'))
@given(parsers.parse('I have a {rows:d}x{cols:d} Minesweeper game with {mines:d} mines'))
def create_custom_game(game_context, rows, cols, mines):
    """Create a custom Minesweeper game with specified dimensions and mines."""
    game_context['game'] = Minesweeper(rows, cols, mines)

@given('I have revealed a safe cell first')
def reveal_safe_cell_first(game_context):
    """Reveal a safe cell to trigger mine placement."""
    game = game_context['game']
    # Find a safe spot to reveal (avoid corners which might have mines)
    for row in range(game.rows):
        for col in range(game.cols):
            result = game.reveal(row, col)
            if result and game.get_game_state() == GameState.PLAYING:
                break
        if game.cells_revealed > 0:
            break

@given('I have lost the game by revealing a mine')
def have_lost_game(game_context):
    """Pre-condition: game is already lost by revealing a mine."""
    game = game_context['game']
    # First reveal a safe cell
    game.reveal(1, 1)  # Assuming this is safe
    # Then reveal a mine (we know where it is from the pattern)
    for row in range(game.rows):
        for col in range(game.cols):
            if game.grid[row][col].is_mine:
                result = game.reveal(row, col)
                game_context['last_reveal_result'] = result
                break

@given('I have won the game by revealing all safe cells')
def have_won_game(game_context):
    """Pre-condition: game is already won by revealing all safe cells."""
    game = game_context['game']
    # Reveal all non-mine cells
    for row in range(game.rows):
        for col in range(game.cols):
            if not game.grid[row][col].is_mine:
                game.reveal(row, col)

# When steps
@when('I set up the game with this board pattern')
def setup_game_with_pattern(game_context):
    """Set up the game using the board pattern from docstring."""
    pattern = game_context['board_pattern']
    game_context['game'] = Minesweeper()
    game_context['game'].setup_board_from_pattern(pattern)

@when('I reveal a cell that contains a mine')
def reveal_mine_cell(game_context):
    """Reveal a cell that contains a mine."""
    game = game_context['game']
    # Find and reveal a mine
    for row in range(game.rows):
        for col in range(game.cols):
            if game.grid[row][col].is_mine:
                result = game.reveal(row, col)
                game_context['last_reveal_result'] = result
                break

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
    revealed_count = 0
    max_to_reveal = game.total_safe_cells - 2  # Leave at least 2 unrevealed
    
    for row in range(game.rows):
        for col in range(game.cols):
            if not game.grid[row][col].is_mine and revealed_count < max_to_reveal:
                game.reveal(row, col)
                revealed_count += 1
            if revealed_count >= max_to_reveal:
                break
        if revealed_count >= max_to_reveal:
            break

@when('I try to reveal another cell')
def try_reveal_another_cell(game_context):
    """Try to reveal another cell after game is over."""
    game = game_context['game']
    # Try to reveal any hidden cell
    game_context['last_reveal_result'] = False  # Default to False if no hidden cells found
    for row in range(game.rows):
        for col in range(game.cols):
            if game.grid[row][col].state == CellState.HIDDEN:
                result = game.reveal(row, col)
                game_context['last_reveal_result'] = result
                break
            elif game.grid[row][col].state == CellState.REVEALED:
                # Try to reveal an already revealed cell - should fail
                result = game.reveal(row, col)
                game_context['last_reveal_result'] = result
                break

@when('I flag some cells')
def flag_some_cells(game_context):
    """Flag some cells on the board."""
    game = game_context['game']
    # Flag a few cells
    cells_to_flag = [(0, 0), (0, 1)]
    for row, col in cells_to_flag:
        if row < game.rows and col < game.cols:
            game.flag(row, col)

@when('I reveal all safe cells')
def reveal_all_safe_cells_after_flagging(game_context):
    """Reveal all safe cells (after some may be flagged)."""
    game = game_context['game']
    for row in range(game.rows):
        for col in range(game.cols):
            cell = game.grid[row][col]
            if not cell.is_mine and cell.state != CellState.REVEALED:
                # Unflag if needed, then reveal
                if cell.state == CellState.FLAGGED:
                    game.flag(row, col)  # Unflag
                game.reveal(row, col)

@when('I reveal all cells')
def reveal_all_cells(game_context):
    """Reveal all cells on the board."""
    game = game_context['game']
    for row in range(game.rows):
        for col in range(game.cols):
            game.reveal(row, col)

@when(parsers.parse('I reveal cell ({row:d},{col:d})'))
def reveal_specific_cell(game_context, row, col):
    """Reveal a specific cell at the given coordinates."""
    game = game_context['game']
    result = game.reveal(row, col)
    game_context['last_reveal_result'] = result

# Then steps
@then(parsers.parse('the game state should be "{state}"'))
def check_game_state(game_context, state):
    """Verify the game state matches expected value."""
    game = game_context['game']
    expected_state = GameState(state)
    assert game.get_game_state() == expected_state

@then(parsers.parse('the game state should remain "{state}"'))
def check_game_state_remains(game_context, state):
    """Verify the game state remains as expected."""
    game = game_context['game']
    expected_state = GameState(state)
    assert game.get_game_state() == expected_state

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

@then('all safe cells should be revealed')
def check_all_safe_cells_revealed(game_context):
    """Verify all safe cells are revealed."""
    game = game_context['game']
    for row in range(game.rows):
        for col in range(game.cols):
            cell = game.grid[row][col]
            if not cell.is_mine:
                assert cell.state == CellState.REVEALED, f"Safe cell at ({row}, {col}) not revealed"

@then('the reveal operation should fail')
def check_reveal_operation_failed(game_context):
    """Verify that the last reveal operation failed."""
    assert game_context['last_reveal_result'] == False

@then('flagged cells should not prevent winning')
def check_flags_dont_prevent_winning(game_context):
    """Verify that having flagged cells doesn't prevent winning."""
    game = game_context['game']
    # If game is won, then flagged cells didn't prevent it
    assert game.get_game_state() == GameState.WON

@then('all cells should be revealed')
def check_all_cells_revealed(game_context):
    """Verify all cells on the board are revealed."""
    game = game_context['game']
    for row in range(game.rows):
        for col in range(game.cols):
            cell = game.grid[row][col]
            assert cell.state == CellState.REVEALED, f"Cell at ({row}, {col}) not revealed" 
