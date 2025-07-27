# Minesweeper

This repository contains a simple BDD specification for a Minesweeper clone written in Python. The UI will use Ncurses while the game logic remains independent so it can be tested without the interface.

See `features/minesweeper_game.feature` for BDD scenarios that describe how the board behaves. Boards can be explicitly defined in the feature file using the `Given the board is:` step.
