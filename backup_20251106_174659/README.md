# Bleach Trivia Game

A command-line trivia game based on the popular anime/manga series Bleach. Test your knowledge of the series with various game modes and compete for the top scores on the leaderboard.

## Features

- Three game modes: Short (5 questions), Medium (20 questions), and Long (50 questions)
- Persistent leaderboard tracking across game sessions
- Smart question selection to prevent repeats until all questions have been seen
- Player-specific progress tracking
- Cross-platform compatibility

## Requirements

- Python 3.6 or higher
- No additional dependencies required

## Quick Start

1. Clone the repository or download the source code
2. Run the game:
   ```
   python bleach_trivia.py
   ```
3. Enter your name and select a game mode
4. Answer questions and try to get the highest score!

## Project Structure

- `bleach_trivia.py` - Main game logic and entry point
- `questions.json` - Contains all trivia questions and options
- `answers.json` - Contains the correct answers for each question
- `leaderboard.json` - Stores player scores and progress (automatically created)
- `docs/` - Additional documentation

## Documentation

- [User Guide](docs/USER_GUIDE.md) - How to play and game features
- [Developer Guide](docs/DEVELOPER_GUIDE.md) - Code structure and contribution guidelines
- [API Reference](docs/API_REFERENCE.md) - Detailed class and method documentation

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
