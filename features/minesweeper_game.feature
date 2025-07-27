Feature: Minesweeper game logic
  As a player
  I want the board to behave like classic Minesweeper
  So that I can reveal cells, flag mines and win when all safe cells are revealed

  Background:
    Given a new game engine
    And the board is:
      """
      *...*
      .....
      ....*
      .....
      *...*
      """

  Scenario: Reveal a safe cell
    When I reveal cell (1,1)
    Then the cell should display the number of adjacent mines
    And the game should continue

  Scenario: Reveal a mine
    When I reveal a cell containing a mine
    Then the game should end with a loss

  Scenario: Auto reveal empty neighbours
    Given cell (2,2) has no adjacent mines
    When I reveal cell (2,2)
    Then all adjacent cells without mines should be revealed

  Scenario: Flagging a cell
    When I flag cell (0,0)
    Then the cell should be marked as flagged
    And the number of remaining flags should decrease

  Scenario: Winning the game
    Given all non-mine cells are revealed
    When the last safe cell is revealed
    Then the game should end with a win
