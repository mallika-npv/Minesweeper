# Minesweeper Game

## Overview
Minesweeper is a classic puzzle game that consists of a grid of cells. Some cells contain hidden "mines" and others are safe. The objective is to reveal all the safe cells without detonating any mines. When a player clicks on a safe cell, it reveals a number indicating how many neighboring cells contain mines. A neighbor is defined as any cell that is directly adjacent or diagonal to the given cell.

## Gameplay

- **Grid of Cells:** The game board is made up of a grid of cells.
- **Mines:** Some cells contain mines. Clicking on a mine cell results in a loss.
- **Safe Cells:** Clicking on a safe cell reveals a number that represents the count of mines in the adjacent cells.
- **Neighbors:** Neighbors include cells to the left, right, above, below, and diagonal to the current cell.

## Objective

- **Win Condition:** Reveal all safe cells without clicking on any mines.
- **Lose Condition:** Click on a cell that contains a mine.

## AI Implementation
In the Minesweeper game, an AI can assist in making decisions based on known information about the board. The AI uses logic to infer safe moves and identify potential mines.

### Sentence Class
The `Sentence` class manages the knowledge about the game board. It includes methods to identify known mines and safe cells, and to mark cells as either mines or safe.

- **known_mines:** Returns a set of cells that are known to be mines.
- **known_safes:** Returns a set of cells that are known to be safe.
- **mark_mine:** If a cell is in the sentence, it updates the sentence to reflect that the cell is a known mine.
- **mark_safe:** If a cell is in the sentence, it updates the sentence to reflect that the cell is a known safe cell.

### MinesweeperAI Class
The `MinesweeperAI` class uses the knowledge base to make decisions.

- **add_knowledge:** Accepts a cell and its corresponding mine count. It updates the AI's knowledge base with new information, marking cells as safe or as mines, and adds new logical sentences based on the revealed information.
- **make_safe_move:** Returns a known safe move that hasn't been made yet. If no safe move is known, it returns `None`.
- **make_random_move:** Returns a random move that hasn't been made and is not known to be a mine. If no such move is possible, it returns `None`.

## Summary
The AI continually updates its knowledge base with new information as the game progresses. It makes safe moves when possible and resorts to random moves when no safe move is known. This approach helps in systematically uncovering the board while minimizing the risk of hitting a mine.
