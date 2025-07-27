import random
from enum import Enum
from typing import List, Tuple, Set


class CellState(Enum):
    """Represents the state of a cell in the minesweeper grid."""
    HIDDEN = "hidden"
    REVEALED = "revealed"
    FLAGGED = "flagged"


class GameState(Enum):
    """Represents the current state of the game."""
    PLAYING = "playing"
    WON = "won"
    LOST = "lost"


class Cell:
    """Represents a single cell in the minesweeper grid."""
    
    def __init__(self):
        self.is_mine = False
        self.state = CellState.HIDDEN
        self.adjacent_mines = 0
    
    def __str__(self):
        if self.state == CellState.FLAGGED:
            return "F"
        elif self.state == CellState.HIDDEN:
            return "?"
        elif self.is_mine:
            return "*"
        else:
            return str(self.adjacent_mines) if self.adjacent_mines > 0 else " "


class Minesweeper:
    """A complete Minesweeper game implementation."""
    
    def __init__(self, rows: int = 9, cols: int = 9, mines: int = 10):
        """
        Initialize a new Minesweeper game.
        
        Args:
            rows: Number of rows in the grid
            cols: Number of columns in the grid
            mines: Number of mines to place
        """
        self.rows = rows
        self.cols = cols
        self.total_mines = mines
        self.game_state = GameState.PLAYING
        self.first_move = True
        
        # Initialize the grid
        self.grid: List[List[Cell]] = []
        for _ in range(rows):
            row = [Cell() for _ in range(cols)]
            self.grid.append(row)
        
        # Track game statistics
        self.flags_placed = 0
        self.cells_revealed = 0
        self.total_safe_cells = rows * cols - mines
    
    def setup_board_from_pattern(self, pattern: str):
        """
        Set up the board from a string pattern.
        
        Args:
            pattern: Multi-line string where '*' represents mines and '.' represents empty cells
        """
        lines = [line.strip() for line in pattern.strip().split('\n') if line.strip()]
        if not lines:
            return
        
        self.rows = len(lines)
        self.cols = max(len(line) for line in lines)  # Use max length to handle varying line lengths
        
        # Reinitialize grid with new dimensions
        self.grid = []
        for _ in range(self.rows):
            row = [Cell() for _ in range(self.cols)]
            self.grid.append(row)
        
        # Count actual mines in pattern
        mine_count = 0
        for row_idx, line in enumerate(lines):
            for col_idx, char in enumerate(line):
                if col_idx < self.cols:  # Safety check
                    if char == '*':
                        self.grid[row_idx][col_idx].is_mine = True
                        mine_count += 1
        
        self.total_mines = mine_count
        self.total_safe_cells = self.rows * self.cols - mine_count
        self.first_move = False  # Pattern is explicit, no need for first move protection
        
        # Reset game statistics
        self.flags_placed = 0
        self.cells_revealed = 0
        self.game_state = GameState.PLAYING
        
        # Calculate adjacent mine counts
        self._calculate_adjacent_mines()
    
    def _get_neighbors(self, row: int, col: int) -> List[Tuple[int, int]]:
        """Get all valid neighbor coordinates for a given cell."""
        neighbors = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
                    neighbors.append((new_row, new_col))
        return neighbors
    
    def _place_mines(self, exclude_row: int, exclude_col: int):
        """
        Place mines randomly on the board, avoiding the first clicked cell.
        
        Args:
            exclude_row: Row to exclude from mine placement (first click)
            exclude_col: Column to exclude from mine placement (first click)
        """
        # Get all possible positions except the first clicked cell and its neighbors
        exclude_positions = {(exclude_row, exclude_col)}
        exclude_positions.update(self._get_neighbors(exclude_row, exclude_col))
        
        available_positions = []
        for r in range(self.rows):
            for c in range(self.cols):
                if (r, c) not in exclude_positions:
                    available_positions.append((r, c))
        
        # Randomly select mine positions
        mine_positions = random.sample(available_positions, min(self.total_mines, len(available_positions)))
        
        # Place mines
        for row, col in mine_positions:
            self.grid[row][col].is_mine = True
        
        # Calculate adjacent mine counts for all cells
        self._calculate_adjacent_mines()
    
    def _calculate_adjacent_mines(self):
        """Calculate the number of adjacent mines for each cell."""
        for row in range(self.rows):
            for col in range(self.cols):
                if not self.grid[row][col].is_mine:
                    count = 0
                    for neighbor_row, neighbor_col in self._get_neighbors(row, col):
                        if self.grid[neighbor_row][neighbor_col].is_mine:
                            count += 1
                    self.grid[row][col].adjacent_mines = count
    
    def _reveal_cell(self, row: int, col: int) -> bool:
        """
        Reveal a single cell.
        
        Args:
            row: Row of the cell to reveal
            col: Column of the cell to reveal
            
        Returns:
            True if the game should continue, False if a mine was hit
        """
        cell = self.grid[row][col]
        
        if cell.state != CellState.HIDDEN:
            return True
        
        cell.state = CellState.REVEALED
        self.cells_revealed += 1
        
        if cell.is_mine:
            self.game_state = GameState.LOST
            return False
        
        # If cell has no adjacent mines, reveal all neighbors
        if cell.adjacent_mines == 0:
            for neighbor_row, neighbor_col in self._get_neighbors(row, col):
                if self.grid[neighbor_row][neighbor_col].state == CellState.HIDDEN:
                    self._reveal_cell(neighbor_row, neighbor_col)
        
        return True
    
    def reveal(self, row: int, col: int) -> bool:
        """
        Reveal a cell at the given coordinates.
        
        Args:
            row: Row of the cell to reveal
            col: Column of the cell to reveal
            
        Returns:
            True if the move was successful, False if invalid or game over
        """
        if self.game_state != GameState.PLAYING:
            return False
        
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return False
        
        cell = self.grid[row][col]
        
        if cell.state == CellState.FLAGGED:
            return False
        
        if cell.state == CellState.REVEALED:
            return False
        
        # Place mines on first move
        if self.first_move:
            self._place_mines(row, col)
            self.first_move = False
        
        # Reveal the cell
        success = self._reveal_cell(row, col)
        
        # Check win condition only if the reveal was successful (no mine hit)
        if success and self._are_all_safe_cells_revealed():
            self.game_state = GameState.WON
            self.reveal_all_mines()  # Reveal all mines when the game is won
        
        return success
    
    def flag(self, row: int, col: int) -> bool:
        """
        Toggle flag on a cell.
        
        Args:
            row: Row of the cell to flag
            col: Column of the cell to flag
            
        Returns:
            True if the flag operation was successful, False otherwise
        """
        if self.game_state != GameState.PLAYING:
            return False
        
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return False
        
        cell = self.grid[row][col]
        
        if cell.state == CellState.REVEALED:
            return False
        
        if cell.state == CellState.FLAGGED:
            cell.state = CellState.HIDDEN
            self.flags_placed -= 1
        else:
            cell.state = CellState.FLAGGED
            self.flags_placed += 1
        
        return True
    
    def chord_reveal(self, row: int, col: int) -> bool:
        """
        Chord reveal (middle-click reveal) - reveals all non-flagged adjacent cells
        if the number of flagged adjacent cells matches the cell's number.
        
        Args:
            row: Row of the cell to chord reveal
            col: Column of the cell to chord reveal
            
        Returns:
            True if the chord reveal was successful, False otherwise
        """
        if self.game_state != GameState.PLAYING:
            return False
        
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return False
        
        cell = self.grid[row][col]
        
        # Can only chord reveal on already revealed cells
        if cell.state != CellState.REVEALED:
            return False
        
        # Can't chord reveal on mines (shouldn't happen since mines end the game)
        if cell.is_mine:
            return False
        
        # Get all neighbors
        neighbors = self._get_neighbors(row, col)
        
        # Count flagged neighbors
        flagged_count = 0
        for neighbor_row, neighbor_col in neighbors:
            neighbor_cell = self.grid[neighbor_row][neighbor_col]
            if neighbor_cell.state == CellState.FLAGGED:
                flagged_count += 1
        
        # Only proceed if the number of flags matches the cell's number
        if flagged_count != cell.adjacent_mines:
            return False
        
        # Reveal all non-flagged, non-revealed neighbors
        success = True
        for neighbor_row, neighbor_col in neighbors:
            neighbor_cell = self.grid[neighbor_row][neighbor_col]
            if neighbor_cell.state == CellState.HIDDEN:
                # Reveal this cell
                result = self._reveal_cell(neighbor_row, neighbor_col)
                if not result:
                    success = False
                    break  # Hit a mine, game over
        
        # Check win condition only if all reveals were successful
        if success and self._are_all_safe_cells_revealed():
            self.game_state = GameState.WON
            self.reveal_all_mines()  # Reveal all mines when the game is won
        
        return success
    
    def get_remaining_mines(self) -> int:
        """Get the number of remaining mines (total mines - flags placed)."""
        return self.total_mines - self.flags_placed
    
    def is_game_over(self) -> bool:
        """Check if the game is over (won or lost)."""
        return self.game_state in [GameState.WON, GameState.LOST]
    
    def get_game_state(self) -> GameState:
        """Get the current game state."""
        return self.game_state
    
    def reset(self):
        """Reset the game to initial state."""
        self.game_state = GameState.PLAYING
        self.first_move = True
        self.flags_placed = 0
        self.cells_revealed = 0
        
        # Reset all cells
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.grid[row][col]
                cell.is_mine = False
                cell.state = CellState.HIDDEN
                cell.adjacent_mines = 0
    
    def reveal_all_mines(self):
        """Reveal all mines (useful for game over display)."""
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col].is_mine:
                    self.grid[row][col].state = CellState.REVEALED
    
    def _are_all_safe_cells_revealed(self) -> bool:
        """
        Check if all safe (non-mine) cells are revealed by actually counting them.
        
        Returns:
            True if all safe cells are revealed, False otherwise
        """
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.grid[row][col]
                # If we find a safe cell that is not revealed, return False
                if not cell.is_mine and cell.state != CellState.REVEALED:
                    return False
        return True

    def _get_cell_counts(self) -> dict:
        """
        Debug method to get counts of different cell types.
        
        Returns:
            Dictionary with counts of different cell states
        """
        counts = {
            'total_cells': self.rows * self.cols,
            'mines': 0,
            'safe_cells': 0,
            'revealed_safe_cells': 0,
            'hidden_safe_cells': 0,
            'flagged_safe_cells': 0,
            'revealed_mines': 0,
            'hidden_mines': 0,
            'flagged_mines': 0
        }
        
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.grid[row][col]
                if cell.is_mine:
                    counts['mines'] += 1
                    if cell.state == CellState.REVEALED:
                        counts['revealed_mines'] += 1
                    elif cell.state == CellState.HIDDEN:
                        counts['hidden_mines'] += 1
                    elif cell.state == CellState.FLAGGED:
                        counts['flagged_mines'] += 1
                else:
                    counts['safe_cells'] += 1
                    if cell.state == CellState.REVEALED:
                        counts['revealed_safe_cells'] += 1
                    elif cell.state == CellState.HIDDEN:
                        counts['hidden_safe_cells'] += 1
                    elif cell.state == CellState.FLAGGED:
                        counts['flagged_safe_cells'] += 1
        
        return counts

    def get_cell_info(self, row: int, col: int) -> dict:
        """
        Get information about a specific cell.
        
        Args:
            row: Row of the cell
            col: Column of the cell
            
        Returns:
            Dictionary with cell information
        """
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return {}
        
        cell = self.grid[row][col]
        return {
            "is_mine": cell.is_mine,
            "state": cell.state.value,
            "adjacent_mines": cell.adjacent_mines
        }


