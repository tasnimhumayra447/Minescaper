# Minescaper

A Minesweeper-inspired variant built in Python, with an interactive browser demo deployed via GitHub Pages.

🎮 **[Play it live here](https://tasnimhumayra447.github.io/Minesweeper)**

---

## About

Minescaper is a grid-based puzzle game where the player navigates from the **top-left corner** to the **bottom-right exit** without stepping on a mine. 
Unlike classic Minesweeper where you click to reveal cells, here you actively move through the board using WASD controls — making every step count.

The project was built from scratch in Python, implementing the full game logic across four components: board generation, input processing, zero-cell cascading, and board rendering.

---

## How to Play

**Controls**

| Input | Action |
|-------|--------|
| `W` | Move up |
| `S` | Move down |
| `A` | Move left |
| `D` | Move right |
| `WA`, `WD`, `SA`, `SD` | Move diagonally |
| Append `F` | Flag the target cell (e.g. `WF`, `WDF`) |

- Each move can consist of **1 or 2 direction steps**, allowing diagonal movement
- Appending `F` to any move **flags that cell** instead of moving there — useful for marking suspected mines
- The **start (top-left)** and **exit (bottom-right)** can never contain mines and cannot be flagged
- Out-of-bounds moves are silently ignored

**Win condition:** Reach the bottom-right exit cell  
**Lose condition:** Step on a mine

---

## Features

- Configurable grid size (5×5, 7×7, 9×9) and mine count
- WASD keyboard controls + clickable d-pad
- Flag mode toggle for marking suspected mines
- Automatic cascading reveal of empty areas
- Reveal All button for testing or giving up
- Fully playable in the browser — no installation required

---

## Implementation

### Task 1 — Mine Board Generation (`create_mine_board`)

Creates the underlying game board as a `grid_size x grid_size` 2D list. Mines are placed at the given positions and represented as `-1`. 
Every safe cell is then filled with an integer from `0` to `8` indicating how many of its up-to-8 neighbouring cells contain mines.

Mine positions are stored in a **set** for O(1) membership checks, and a `ValueError` is raised if a mine is placed on the start or exit cell.

### Task 2 — Input Processing (`process_input`)

Parses a move string from the player and returns the new position and whether a flag was placed. The parsing follows these rules in order:

1. Case-insensitive — converted to uppercase
2. Only the first 3 characters are considered
3. Invalid characters (anything other than `W`, `A`, `S`, `D`, `F`) are stripped
4. `F` is only valid as the **final character** — if it appears mid-string (e.g. `WFW`) it is ignored and the move is treated as directional only
5. Direction steps are order-insensitive and capped at 2
6. Out-of-bounds moves are cancelled and the player stays in place
7. The start and exit cells cannot be flagged

### Task 3 — Zero Cell Cascading (`reveal_zeros`)

When the player steps on a cell with `0` adjacent mines, it triggers an **automatic cascade reveal** of all connected empty cells and their neighbours. 
This is the same mechanic as classic Minesweeper's flood-fill behaviour.

**How the cascade works:**

> Imagine the board as a landscape. A `0` cell means there are no mines anywhere nearby — so it's completely safe to automatically reveal all 8 of its neighbours.
> If any of those neighbours are also `0`, the same logic applies to them, and so on, spreading outward until it hits cells with non-zero counts
> (which act as the boundary, showing the player how close the mines are).

```
Start at current cell
→ Add to visited
→ If value is 0, push all unvisited neighbours onto the stack
→ Repeat until stack is empty
```

The result is that a single step into an open area can reveal a large connected region instantly, rather than requiring the player to manually visit every cell.

### Task 4 — Game Board Rendering (`create_game_board`)

Constructs the visual game board as a 2D list of strings based on the current game state. Each cell is rendered according to this priority order:

| Symbol | Meaning |
|--------|---------|
| `[x]` | Player's current position (e.g. `[2]`, `[0]`) |
| `x` | Revealed safe cell showing adjacent mine count |
| `F` | Flagged cell |
| `E` | Exit cell |
| `.` | Hidden unrevealed cell |
| `*` | Mine (only shown when `show_all=True` at game end) |

When `show_all=True` (game over), the full board is revealed including all mine locations.

---

## Running Locally

```bash
python minesweeper.py
```

Or open `index.html` directly in any browser — no server required.

---

## Tech Stack

- **Python** — core game logic
- **Vanilla JavaScript** — browser port of the Python logic
- **HTML/CSS** — UI and styling
- **GitHub Pages** — free static hosting
