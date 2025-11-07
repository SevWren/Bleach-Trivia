# Bleach Trivia Game

A command-line trivia game based on the popular anime/manga series Bleach. Test your knowledge of the series with various game modes and compete for the top scores on the leaderboard.

## Features

- Three game modes: Short (5 questions), Medium (20 questions), and Long (50 questions)
- Persistent leaderboard tracking across game sessions
- Smart question selection to prevent repeats until all questions have been seen
- Player-specific progress tracking
- Simple, dependency-free implementation

## Requirements

- Python 3.8 or higher
- No additional dependencies required

## Quick Start

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/bleach-trivia.git
   cd bleach-trivia
   ```

2. Run the game:
   ```
   python main.py
   ```

3. Follow the on-screen instructions to play!

## Project Structure

```
bleach-trivia/
├── README.md           # This file
├── main.py            # Main entry point
├── bleach_trivia.py   # Core game logic
├── questions.json     # Trivia questions
├── answers.json       # Question answers
└── leaderboard.json   # Player scores and progress (auto-generated)
```

## How to Play

1. Enter your name when prompted
2. Choose a game mode:
   - Short: 5 questions
   - Medium: 20 questions
   - Long: 50 questions
3. Answer each question by entering A, B, C, or D
4. View your score and the leaderboard at the end of the game

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
