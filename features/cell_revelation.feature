Feature: Cell Revelation
  As a player
  I want to reveal cells on the board
  So that I can progress through the game

  Scenario: Reveal safe cell shows adjacent mine count
    Given I want to start a new game
    And the board is:
      """
      *....
      .....
      .....
      .....
      ....*
      """
    When I set up the game with this board pattern
    And I reveal cell at row 1, column 1
    Then the cell at row 1, column 1 should be revealed
    And the cell should show 1 adjacent mine
    And the game state should be "playing"

  Scenario: Reveal cell with multiple adjacent mines
    Given I want to start a new game
    And the board is:
      """
      .*...
      *.*..
      .*...
      .....
      .....
      """
    When I set up the game with this board pattern
    And I reveal cell at row 1, column 1
    Then the cell at row 1, column 1 should be revealed
    And the cell should show 4 adjacent mines
    And the game state should be "playing"

  Scenario: Reveal empty cell triggers auto-reveal
    Given I want to start a new game
    And the board is:
      """
      ......
      ......
      ......
      .*....
      ......
      .....*
      """
    When I set up the game with this board pattern
    And I reveal cell at row 0, column 0
    Then the cell at row 0, column 0 should be revealed
    And multiple connected empty cells should be revealed
    And the game state should be "playing"

  Scenario: Cannot reveal flagged cell
    Given I want to start a new game
    And the board is:
      """
      *..
      ...
      """
    When I set up the game with this board pattern
    And I flag cell at row 0, column 0
    And I try to reveal cell at row 0, column 0
    Then the cell at row 0, column 0 should remain flagged
    And the reveal operation should fail

  Scenario: Cannot reveal already revealed cell
    Given I want to start a new game
    And the board is:
      """
      *..
      ...
      """
    When I set up the game with this board pattern
    And I reveal cell at row 1, column 1
    And I try to reveal cell at row 1, column 1 again
    Then the second reveal operation should fail
    And the cell should remain revealed

  Scenario: Reveal cell outside board boundaries
    Given I want to start a new game
    And the board is:
      """
      *..
      ...
      """
    When I set up the game with this board pattern
    And I try to reveal cell at row 10, column 10
    Then the reveal operation should fail
    And the game state should remain "playing" 
