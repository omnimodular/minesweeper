Feature: Win Condition Bug Reproduction
  As a player
  I want the game to only declare victory when ALL safe cells are revealed
  So that the win condition is accurate and fair

  Scenario: Game should not win with unrevealed safe cells
    Given I want to start a new game
    And the board is:
      """
      ...
      .*.
      ...
      """
    When I set up the game with this board pattern
    And I reveal cell (0,0)
    And I reveal cell (0,1)
    And I reveal cell (0,2)
    And I reveal cell (1,0)
    # Skipping cell (1,1) which is a mine
    And I reveal cell (1,2)
    And I reveal cell (2,0)
    # Leaving cells (2,1) and (2,2) unrevealed
    Then the game state should be "playing"
    And the game should not be over

  Scenario: Game should only win when all safe cells are revealed
    Given I want to start a new game
    And the board is:
      """
      ...
      .*.
      ...
      """
    When I set up the game with this board pattern
    And I reveal all cells except the mine
    Then the game state should be "won"
    And the game should be over
    And all safe cells should be revealed

  Scenario: Complex board pattern win condition
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
    And I reveal some but not all safe cells
    Then the game state should be "playing"
    And the game should not be over

  Scenario: Complex board should win only when all safe cells revealed
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
    And I reveal all cells except the mine
    Then the game state should be "won"
    And the game should be over
    And all safe cells should be revealed 
