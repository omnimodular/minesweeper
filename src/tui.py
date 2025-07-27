"""
Text User Interface for Minesweeper.

This TUI depends on the Minesweeper game logic via dependency injection.
"""

import curses
import sys
from minesweeper import Minesweeper, GameState, CellState


class MinesweeperTUI:
    """Text User Interface for Minesweeper using ncurses."""
    
    def __init__(self, game: Minesweeper):
        """
        Initialize the TUI with dependency injection.
        
        Args:
            game: Minesweeper instance to use for the game
        """
        self.game = game
        self.cursor_row = 0
        self.cursor_col = 0
        # Store initial settings for restart functionality
        self.initial_rows = game.rows
        self.initial_cols = game.cols
        self.initial_mines = game.total_mines
    
    def setup_colors(self):
        """Set up color pairs for the display."""
        if curses.has_colors():
            curses.start_color()
            # Define color pairs
            curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)    # Normal text
            curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)      # Mines
            curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)      # Flagged
            curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)   # Cursor
            curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_BLACK)     # Numbers
            curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)     # Hidden
            curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_RED)      # Game over
    
    def get_cell_display_char(self, row: int, col: int) -> tuple:
        """
        Get the display character and color for a cell.
        
        Args:
            row: Row of the cell
            col: Column of the cell
            
        Returns:
            Tuple of (character, color_pair)
        """
        cell = self.game.grid[row][col]
        
        if cell.state == CellState.FLAGGED:
            return ('x', curses.color_pair(3))
        elif cell.state == CellState.HIDDEN:
            return ('■', curses.color_pair(6))
        elif cell.is_mine:
            return ('*', curses.color_pair(2))
        elif cell.adjacent_mines > 0:
            return (str(cell.adjacent_mines), curses.color_pair(5))
        else:
            return (' ', curses.color_pair(1))
    
    def draw_board(self, stdscr):
        """Draw the minesweeper board."""
        # Clear screen
        stdscr.clear()
        
        # Draw column headers
        header = "   " + " ".join(f"{i:2}" for i in range(self.game.cols))
        stdscr.addstr(0, 0, header, curses.color_pair(1))
        stdscr.addstr(1, 0, "  " + "---" * self.game.cols, curses.color_pair(1))
        
        # Draw board
        for row in range(self.game.rows):
            # Row header
            stdscr.addstr(row + 2, 0, f"{row:2}|", curses.color_pair(1))
            
            for col in range(self.game.cols):
                char, color = self.get_cell_display_char(row, col)
                
                # Highlight cursor position
                if row == self.cursor_row and col == self.cursor_col:
                    if self.game.game_state == GameState.PLAYING:
                        color = curses.color_pair(4) | curses.A_REVERSE
                    else:
                        color = curses.color_pair(7) | curses.A_REVERSE
                
                stdscr.addstr(row + 2, 3 + col * 3, f" {char}", color)
        
        # Draw status information
        status_row = self.game.rows + 4
        stdscr.addstr(status_row, 0, f"Mines remaining: {self.game.get_remaining_mines()}", curses.color_pair(1))
        stdscr.addstr(status_row + 1, 0, f"Game state: {self.game.game_state.value.upper()}", curses.color_pair(1))
        
        if self.game.game_state == GameState.WON:
            stdscr.addstr(status_row + 2, 0, "🎉 CONGRATULATIONS! YOU WON! 🎉", curses.color_pair(3) | curses.A_BOLD)
        elif self.game.game_state == GameState.LOST:
            stdscr.addstr(status_row + 2, 0, "💥 GAME OVER! YOU HIT A MINE! 💥", curses.color_pair(2) | curses.A_BOLD)
        
        # Draw controls
        controls_row = status_row + 4
        stdscr.addstr(controls_row, 0, "Controls:", curses.color_pair(1) | curses.A_BOLD)
        stdscr.addstr(controls_row + 1, 0, "  Arrow keys / hjkl: Move cursor", curses.color_pair(1))
        stdscr.addstr(controls_row + 2, 0, "  'r': Reveal cell", curses.color_pair(1))
        stdscr.addstr(controls_row + 3, 0, "  'm': Mark/unmark cell", curses.color_pair(1))
        stdscr.addstr(controls_row + 4, 0, "  'F2': Restart game", curses.color_pair(1))
        stdscr.addstr(controls_row + 5, 0, "  'ESC': Quit", curses.color_pair(1))
        
        stdscr.refresh()
    
    def handle_input(self, key):
        """
        Handle keyboard input.
        
        Args:
            key: The key pressed
            
        Returns:
            True to continue, False to quit
        """
        # ESC key to quit
        if key == 27:  # ESC
            return False
        
        # F2 key to restart
        if key == curses.KEY_F2:
            self.game = Minesweeper(self.initial_rows, self.initial_cols, self.initial_mines)
            self.cursor_row = 0
            self.cursor_col = 0
            return True
        
        # Arrow key navigation and Vi bindings
        if (key == curses.KEY_UP or key == ord('k') or key == ord('K')) and self.cursor_row > 0:
            self.cursor_row -= 1
        elif (key == curses.KEY_DOWN or key == ord('j') or key == ord('J')) and self.cursor_row < self.game.rows - 1:
            self.cursor_row += 1
        elif (key == curses.KEY_LEFT or key == ord('h') or key == ord('H')) and self.cursor_col > 0:
            self.cursor_col -= 1
        elif (key == curses.KEY_RIGHT or key == ord('l') or key == ord('L')) and self.cursor_col < self.game.cols - 1:
            self.cursor_col += 1
        
        # Game actions (only if game is still playing)
        elif self.game.game_state == GameState.PLAYING:
            if key == ord('r') or key == ord('R'):
                # Reveal cell
                success = self.game.reveal(self.cursor_row, self.cursor_col)
                if not success and self.game.game_state == GameState.LOST:
                    # Reveal all mines when game is lost
                    self.game.reveal_all_mines()
            elif key == ord('m') or key == ord('M'):
                # Mark/unmark cell
                self.game.flag(self.cursor_row, self.cursor_col)
        
        return True
    
    def run(self, stdscr):
        """Main game loop."""
        # Setup
        curses.curs_set(0)  # Hide cursor
        stdscr.keypad(True)  # Enable special keys
        stdscr.nodelay(False)  # Blocking input
        self.setup_colors()
        
        while True:
            self.draw_board(stdscr)
            key = stdscr.getch()
            
            if not self.handle_input(key):
                break


def main():
    """Main entry point for the TUI."""
    def wrapper(stdscr):
        # Default game settings - can be customized
        rows, cols, mines = 9, 9, 10
        
        # Check for command line arguments
        if len(sys.argv) >= 4:
            try:
                rows = int(sys.argv[1])
                cols = int(sys.argv[2])
                mines = int(sys.argv[3])
            except ValueError:
                print("Usage: python tui.py [rows] [cols] [mines]")
                return
        
        # Create a Minesweeper instance for the TUI
        game = Minesweeper(rows, cols, mines)
        tui = MinesweeperTUI(game)
        tui.run(stdscr)
    
    try:
        curses.wrapper(wrapper)
    except KeyboardInterrupt:
        print("\nGame interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main() 
