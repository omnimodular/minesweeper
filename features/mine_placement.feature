Feature: Explicit Board Setup
  As a player
  I want explicit board patterns to be set up correctly
  So that I have predictable and testable game scenarios

  Scenario: Board pattern is set up correctly
    Given I want to start a new game
    And the board is:
      """
      *..
      .*.
      ..*
      """
    When I set up the game with this board pattern
    Then exactly 3 mines should be placed on the board
    And cell at row 0, column 0 should have a mine
    And cell at row 1, column 1 should have a mine
    And cell at row 2, column 2 should have a mine

  Scenario: Adjacent mine counts are calculated correctly
    Given I want to start a new game
    And the board is:
      """
      *..
      ...
      ..*
      """
    When I set up the game with this board pattern
    Then all non-mine cells should have correct adjacent mine counts
    And cell at row 0, column 1 should show 1 adjacent mine
    And cell at row 1, column 1 should show 2 adjacent mines
    And cell at row 2, column 1 should show 1 adjacent mine

  Scenario: Complex board pattern verification
    Given I want to start a new game
    And the board is:
      """
      *.*.*
      .....
      *.*.*
      .....
      *.*.*
      """
    When I set up the game with this board pattern
    Then exactly 9 mines should be placed on the board
    And the board should be 5x5
    And cell at row 1, column 1 should show 4 adjacent mines

  Scenario: Empty board with no mines
    Given I want to start a new game
    And the board is:
      """
      ....
      ....
      ....
      ....
      """
    When I set up the game with this board pattern
    Then exactly 0 mines should be placed on the board
    And all cells should show 0 adjacent mines

  Scenario: Single mine board
    Given I want to start a new game
    And the board is:
      """
      ...
      .*.
      ...
      """
    When I set up the game with this board pattern
    Then exactly 1 mine should be placed on the board
    And all adjacent cells to the mine should show 1 adjacent mine 
