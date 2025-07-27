Feature: Cell Flagging
  As a player
  I want to flag and unflag cells
  So that I can mark suspected mine locations

  Scenario: Flag a hidden cell
    Given I have a 5x5 Minesweeper game with 3 mines
    When I flag cell at row 0, column 0
    Then the cell at row 0, column 0 should be flagged
    And the flags placed count should be 1
    And the remaining mines count should be 2

  Scenario: Unflag a flagged cell
    Given I have a 5x5 Minesweeper game with 3 mines
    And I have flagged cell at row 0, column 0
    When I flag cell at row 0, column 0 again
    Then the cell at row 0, column 0 should be hidden
    And the flags placed count should be 0
    And the remaining mines count should be 3

  Scenario: Cannot flag revealed cell
    Given I have a 5x5 Minesweeper game with 3 mines
    When I reveal cell at row 2, column 2
    And I try to flag cell at row 2, column 2
    Then the flag operation should fail
    And the cell at row 2, column 2 should remain revealed
    And the flags placed count should be 0

  Scenario: Flag multiple cells
    Given I have a 5x5 Minesweeper game with 5 mines
    When I flag cell at row 0, column 0
    And I flag cell at row 0, column 1
    And I flag cell at row 1, column 0
    Then the flags placed count should be 3
    And the remaining mines count should be 2
    And all three cells should be flagged

  Scenario: Flag cell outside board boundaries
    Given I have a 5x5 Minesweeper game with 3 mines
    When I try to flag cell at row 10, column 10
    Then the flag operation should fail
    And the flags placed count should be 0

  Scenario: Flag more cells than mines
    Given I have a 3x3 Minesweeper game with 2 mines
    When I flag 5 different cells
    Then all 5 cells should be flagged
    And the flags placed count should be 5
    And the remaining mines count should be -3 
