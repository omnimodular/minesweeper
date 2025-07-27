"""
Main entry point for Minesweeper game.

This module demonstrates dependency injection by creating a game instance
and injecting it into the TUI.
"""

import sys
import curses
from minesweeper import Minesweeper
from tui import MinesweeperTUI


def create_game(difficulty: str = "easy") -> Minesweeper:
    """
    Factory function to create game instances with different difficulties.
    
    Args:
        difficulty: Game difficulty level ("easy", "medium", "hard", "custom")
    
    Returns:
        Configured Minesweeper game instance
    """
    difficulty_configs = {
        "easy": (9, 9, 10),      # 9x9 with 10 mines
        "medium": (16, 16, 40),  # 16x16 with 40 mines  
        "hard": (16, 30, 99),    # 16x30 with 99 mines
    }
    
    if difficulty in difficulty_configs:
        rows, cols, mines = difficulty_configs[difficulty]
        return Minesweeper(rows, cols, mines)
    else:
        # Default to easy
        return Minesweeper(9, 9, 10)


def select_difficulty() -> str:
    """Allow user to select game difficulty."""
    print("🎯 Select Difficulty:")
    print("  1. Easy (9x9, 10 mines)")
    print("  2. Medium (16x16, 40 mines)")
    print("  3. Hard (16x30, 99 mines)")
    print("  4. Custom")
    
    while True:
        try:
            choice = input("\nEnter choice (1-4): ").strip()
            
            if choice == "1":
                return "easy"
            elif choice == "2":
                return "medium"
            elif choice == "3":
                return "hard"
            elif choice == "4":
                return create_custom_game()
            else:
                print("Please enter 1, 2, 3, or 4")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            sys.exit(0)


def create_custom_game() -> Minesweeper:
    """Create a custom game with user-specified dimensions and mines."""
    print("\n🛠️  Custom Game Setup:")
    
    try:
        rows = int(input("Enter number of rows (3-30): "))
        cols = int(input("Enter number of columns (3-30): "))
        max_mines = (rows * cols) - 1
        mines = int(input(f"Enter number of mines (1-{max_mines}): "))
        
        # Validate inputs
        if not (3 <= rows <= 30):
            print("Rows must be between 3 and 30. Using default: 9")
            rows = 9
        if not (3 <= cols <= 30):
            print("Columns must be between 3 and 30. Using default: 9")
            cols = 9
        if not (1 <= mines <= max_mines):
            print(f"Mines must be between 1 and {max_mines}. Using default: 10")
            mines = 10
        
        return Minesweeper(rows, cols, mines)
        
    except (ValueError, KeyboardInterrupt):
        print("\nInvalid input. Using default easy game.")
        return Minesweeper(9, 9, 10)


def main():
    """
    Main entry point with dependency injection.
    
    This function demonstrates the dependency injection pattern:
    1. Create the game (dependency)
    2. Inject it into the TUI (dependent)
    3. Run the TUI
    """
    try:
        print("🚩 Welcome to Minesweeper! 💣\n")
        
        # Always show difficulty selection menu
        difficulty = select_difficulty()
        if isinstance(difficulty, str):
            game = create_game(difficulty)
        else:
            game = difficulty  # Custom game returned directly
        
        # Dependency Injection: Inject game into TUI
        tui = MinesweeperTUI(game)
        
        # Run the interface through curses wrapper
        def tui_wrapper(stdscr):
            tui.run(stdscr)
        
        curses.wrapper(tui_wrapper)
        
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Goodbye!")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        print("Please report this issue.")


if __name__ == "__main__":
    main() 
