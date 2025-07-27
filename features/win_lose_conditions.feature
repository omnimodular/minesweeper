Feature: Win and Lose Conditions
  As a player
  I want clear win and lose conditions
  So that I know when the game ends

  Scenario: Lose by revealing a mine
    Given I want to start a new game
    And the board is:
      """
      *..
      ...
      ...
      """
    When I set up the game with this board pattern
    And I reveal cell (1,1)
    And I reveal cell (0,0)
    Then the game state should be "lost"
    And the game should be over
    And the mine should be revealed

  Scenario: Win by revealing all safe cells
    Given I have a 3x3 Minesweeper game with 1 mine
    When I reveal all cells except the mine
    Then the game state should be "won"
    And the game should be over
    And all safe cells should be revealed

  Scenario: Game continues while safe cells remain
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
    And I reveal cell (1,1)
    And I reveal cell (1,3)
    Then the game state should be "playing"
    And the game should not be over

  Scenario: Cannot make moves after game is lost
    Given I want to start a new game
    And the board is:
      """
      *..
      ...
      ...
      """
    When I set up the game with this board pattern
    And I reveal cell (1,1)
    And I reveal cell (0,0)
    And I try to reveal another cell
    Then the reveal operation should fail
    And the game state should remain "lost"

  Scenario: Cannot make moves after game is won
    Given I have a 3x3 Minesweeper game with 1 mine
    And I have won the game by revealing all safe cells
    When I try to reveal another cell
    Then the reveal operation should fail
    And the game state should remain "won"

  Scenario: Flagging doesn't affect win condition
    Given I have a 3x3 Minesweeper game with 1 mine
    When I flag some cells
    And I reveal all safe cells
    Then the game state should be "won"
    And flagged cells should not prevent winning

  Scenario: Win condition with zero mines
    Given I have a 3x3 Minesweeper game with 0 mines
    When I reveal all cells
    Then the game state should be "won"
    And all cells should be revealed

  Scenario: All cells are revealed when game is won
    Given I want to start a new game
    And the board is:
      """
      *..
      ...
      ...*
      """
    When I set up the game with this board pattern
    And I reveal all cells except the mine
    Then the game state should be "won"
    And the game should be over
    And all cells should be revealed
