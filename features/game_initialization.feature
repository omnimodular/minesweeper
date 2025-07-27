Feature: Game Initialization
  As a player
  I want to initialize a Minesweeper game
  So that I can start playing with a proper game board

  Scenario: Initialize default game board
    Given I want to start a new game
    When I create a default Minesweeper game
    Then the board should be 9x9
    And there should be 10 mines
    And all cells should be hidden
    And the game state should be "playing"

  Scenario: Initialize game with explicit board pattern
    Given I want to start a new game
    And the board is:
      """
      *..
      .*.
      ..*
      """
    When I set up the game with this board pattern
    Then the board should be 3x3
    And there should be 3 mines
    And all cells should be hidden
    And the game state should be "playing"

  Scenario: Initialize simple board with single mine
    Given I want to start a new game
    And the board is:
      """
      ..
      .*
      """
    When I set up the game with this board pattern
    Then the board should be 2x2
    And there should be 1 mine
    And the remaining mines count should be 1
    And the flags placed count should be 0
    And the cells revealed count should be 0

  Scenario: Initialize empty board with no mines
    Given I want to start a new game
    And the board is:
      """
      ...
      ...
      ...
      """
    When I set up the game with this board pattern
    Then the board should be 3x3
    And there should be 0 mines
    And all cells should be hidden
    And the game state should be "playing" 
