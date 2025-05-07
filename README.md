# Chess vs AI

A interactive chess application built with Python, Tkinter, and the `python-chess` library. Play against a Minimax-based AI with configurable difficulty, view move history, and customize settings.

## Table of Contents

* [Features](#features)
* [Demo](#demo)
* [Installation](#installation)
* [Usage](#usage)
* [Configuration](#configuration)
* [Key Bindings & Controls](#key-bindings--controls)
* [Project Structure](#project-structure)
* [Dependencies](#dependencies)
* [Contributing](#contributing)
* [License](#license)

## Features

* **Minimax AI**: Configurable search depth (Levels 1–5) with Alpha-Beta pruning.
* **GUI**: Graphical board and side panel built with Tkinter.
* **Move History**: Tracks and displays moves in algebraic notation.
* **Visual Aids**:

  * Highlight legal moves for selected pieces.
  * Highlight last move made.
  * Indicate when the king is in check.
* **Settings Menu**:

  * Choose AI difficulty level.
  * Select player color (White or Black).
  * Toggle display of legal moves.
* **Game Controls**:

  * Start a new game.
  * Resign mid-game.
  * Exit application.

## Demo

*To be added: Screenshots or GIF of gameplay*

## Installation

1. **Clone this repository:**

   ```bash
   git clone https://github.com/yourusername/chess-vs-ai.git
   cd chess-vs-ai
   ```
2. **Install dependencies:**

   ```bash
   pip install python-chess
   ```

   Tkinter is included in most Python distributions. If not, install via your OS package manager.

## Usage

Run the main script:

```bash
python "CHESS GAME2.py"
```

* By default, you play White against the AI.
* Use the **Settings** menu to change difficulty or play as Black.
* Click on a piece to view its legal moves, then click on a target square to move.
* The AI will move automatically after your turn.

## Configuration

Open the **Settings** menu in the application to adjust:

* **AI Difficulty**: Level 1 (shallow) to Level 5 (deep).
* **Player Color**: Choose to play as White or Black.
* **Show Legal Moves**: Enable or disable legal move hints.

## Key Bindings & Controls

* **Mouse Left-Click**: Select piece / target square.
* **`File → New Game`**: Start a fresh game.
* **`File → Exit`**: Quit the application.
* **`Resign`**: Concede the current game.

## Project Structure

```
├── "CHESS GAME2.py"    # Main application script
├── README.md            # This file
└── assets/              # (Optional) Icons, screenshots
```

## Dependencies

* [python-chess](https://pypi.org/project/python-chess/)
* Tkinter (standard GUI library)

## Contributing

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/YourFeature`.
3. Commit your changes and push: `git push origin feature/YourFeature`.
4. Open a Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
