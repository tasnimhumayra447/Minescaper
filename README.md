# Minescaper

A Minesweeper-inspired variant built in Python, with an interactive browser demo deployed via GitHub Pages.

🎮 **[Play it live here] (https://tasnimhumayra447.github.io/Minescaper/index.html)**

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

---

## Running Locally

```bash
python minescaper.py
```

Or open `index.html` directly in any browser — no server required.

---

## Tech Stack

- **Python** — core game logic
- **Vanilla JavaScript** — browser port of the Python logic
- **HTML/CSS** — UI and styling
- **GitHub Pages** — free static hosting
