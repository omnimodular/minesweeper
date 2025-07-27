import pytest
from pytest_bdd import scenarios, given, when, then, parsers
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from minesweeper import Minesweeper, CellState, GameState

# Load scenarios from the feature file
scenarios('../features/mine_placement.feature')

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

# When steps
@when('I set up the game with this board pattern')
def setup_game_with_pattern(game_context):
    """Set up the game using the board pattern from docstring."""
    pattern = game_context['board_pattern']
    game_context['game'] = Minesweeper()
    game_context['game'].setup_board_from_pattern(pattern)

# Then steps
@then(parsers.parse('exactly {count:d} mines should be placed on the board'))
@then(parsers.parse('exactly {count:d} mine should be placed on the board'))
def check_exact_mine_count(game_context, count):
    """Verify the exact number of mines placed on the board."""
    game = game_context['game']
    mine_count = sum(1 for row in range(game.rows) 
                     for col in range(game.cols) 
                     if game.grid[row][col].is_mine)
    assert mine_count == count, f"Expected {count} mines, found {mine_count}"

@then(parsers.parse('cell at row {row:d}, column {col:d} should have a mine'))
def check_cell_has_mine(game_context, row, col):
    """Verify that a specific cell contains a mine."""
    game = game_context['game']
    cell = game.grid[row][col]
    assert cell.is_mine, f"Cell at ({row}, {col}) should have a mine"

@then(parsers.parse('the board should be {rows:d}x{cols:d}'))
def check_board_dimensions(game_context, rows, cols):
    """Verify the board has the correct dimensions."""
    game = game_context['game']
    assert game.rows == rows
    assert game.cols == cols

@then('all non-mine cells should have correct adjacent mine counts')
def check_adjacent_mine_counts(game_context):
    """Verify that all non-mine cells have correct adjacent mine counts."""
    game = game_context['game']
    
    for row in range(game.rows):
        for col in range(game.cols):
            cell = game.grid[row][col]
            if not cell.is_mine:
                # Calculate expected adjacent mines
                expected_count = 0
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        new_row, new_col = row + dr, col + dc
                        if (0 <= new_row < game.rows and 
                            0 <= new_col < game.cols and 
                            game.grid[new_row][new_col].is_mine):
                            expected_count += 1
                
                assert cell.adjacent_mines == expected_count, \
                    f"Cell at ({row}, {col}) should have {expected_count} adjacent mines, got {cell.adjacent_mines}"

@then(parsers.parse('cell at row {row:d}, column {col:d} should show {count:d} adjacent mine'))
@then(parsers.parse('cell at row {row:d}, column {col:d} should show {count:d} adjacent mines'))
def check_specific_cell_adjacent_mines(game_context, row, col, count):
    """Verify that a specific cell shows the correct adjacent mine count."""
    game = game_context['game']
    cell = game.grid[row][col]
    assert cell.adjacent_mines == count, \
        f"Cell at ({row}, {col}) should show {count} adjacent mines, got {cell.adjacent_mines}"

@then('center cell should show 4 adjacent mines')
def check_center_cell_adjacent_mines(game_context):
    """Verify that the center cell shows 4 adjacent mines."""
    game = game_context['game']
    center_row = game.rows // 2
    center_col = game.cols // 2
    center_cell = game.grid[center_row][center_col]
    assert center_cell.adjacent_mines == 4, \
        f"Center cell should show 4 adjacent mines, got {center_cell.adjacent_mines}"

@then('all cells should show 0 adjacent mines')
def check_all_cells_zero_adjacent_mines(game_context):
    """Verify that all cells show 0 adjacent mines."""
    game = game_context['game']
    for row in range(game.rows):
        for col in range(game.cols):
            cell = game.grid[row][col]
            assert cell.adjacent_mines == 0, \
                f"Cell at ({row}, {col}) should show 0 adjacent mines, got {cell.adjacent_mines}"

@then('all adjacent cells to the mine should show 1 adjacent mine')
def check_adjacent_cells_to_mine(game_context):
    """Verify that all cells adjacent to the single mine show 1 adjacent mine."""
    game = game_context['game']
    
    # Find the mine
    mine_row, mine_col = None, None
    for row in range(game.rows):
        for col in range(game.cols):
            if game.grid[row][col].is_mine:
                mine_row, mine_col = row, col
                break
        if mine_row is not None:
            break
    
    assert mine_row is not None, "No mine found on the board"
    
    # Check all adjacent cells
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            adj_row, adj_col = mine_row + dr, mine_col + dc
            if (0 <= adj_row < game.rows and 0 <= adj_col < game.cols):
                adj_cell = game.grid[adj_row][adj_col]
                assert adj_cell.adjacent_mines == 1, \
                    f"Adjacent cell at ({adj_row}, {adj_col}) should show 1 adjacent mine, got {adj_cell.adjacent_mines}" 
