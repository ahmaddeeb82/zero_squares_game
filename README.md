
# Zero Squares Game - State Management

This repository contains the state management code for the "Zero Squares" game, a grid-based puzzle game where players navigate cells to reach specific goal cells on a game board.


## Overview




The `State` class is responsible for managing the game grid, tracking player movements, and validating potential moves. Players move through cells of various types (like empty cells, goal cells, and other player cells) to solve the puzzle.

## State Class
The `State` class represents the current game state, tracking the grid layout, player positions, and possible moves. It enables moving player cells within the grid and transitioning to new game states based on player actions.



### Attributes

- **grid**: A 2D list representing the game board with various cell types.
- **status**: Boolean indicating if a goal has been achieved.
- **prev_states**: Stores previous game states for tracking move history.
- **next_states**: Lists potential future states based on available moves.

## Core Methods

### getDirectionalCell

**Purpose**: Calculates a new cell position based on a starting position and a given direction.

- **Parameters**:
   - `row`, `column`: Starting cell coordinates.
   - `direction`: Direction to move (`UP`, `DOWN`, `LEFT`, `RIGHT`).
   - `count`: Optional, how many cells to move in the given direction.

### getPlayerCells
**Purpose**: Finds all cells on the grid containing player pieces.
- **Returns**: A list of dictionaries, each with the player cell's object, row, and column.

### checkMove
**Purpose**: Checks if a move in a specific direction is valid.
- **Parameters**:
    - `row`, `column`: Starting position.
    - `grid`: The current grid layout.
    - `direction`: Direction of the move.
    - `count`: Optional, distance to check for validity.
- **Returns**: `True` if the move is valid; otherwise, `False`.

### checkAvailableMoves
**Purpose**: Lists all valid moves for the player based on their current position.
- **Returns**: A list of valid directions.

### move
**Purpose**: Executes a move in a specified direction, updating cell types and managing interactions with goal cells or other player cells.

- **Parameters**:
    - `grid`: The grid layout.
    - `direction`: Direction to move.
    - `count`: Optional, specifies the move distance.
- **Returns**: A new `State` instance representing the updated game state.

### getNextStates
**Purpose**: Generates all potential future states based on available moves.
