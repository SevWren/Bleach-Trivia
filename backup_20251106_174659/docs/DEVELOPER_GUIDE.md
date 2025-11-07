# Bleach Trivia - Developer Guide

## Table of Contents
1. [Project Structure](#project-structure)
2. [Setup and Installation](#setup-and-installation)
3. [Code Organization](#code-organization)
4. [Data Files](#data-files)
5. [Adding New Questions](#adding-new-questions)
6. [Extending the Game](#extending-the-game)
7. [Testing](#testing)
8. [Contributing](#contributing)
9. [License](#license)

## Project Structure

```
Bleach-Trivia/
├── bleach_trivia.py  # Main game logic
├── questions.json    # Trivia questions and options
├── answers.json      # Correct answers
├── leaderboard.json  # Player data and scores (auto-generated)
├── README.md         # Project overview
└── docs/             # Documentation files
    ├── USER_GUIDE.md
    ├── DEVELOPER_GUIDE.md
    └── API_REFERENCE.md
```

## Setup and Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/bleach-trivia.git
   cd bleach-trivia
   ```

2. Ensure you have Python 3.6+ installed

3. (Optional) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

## Code Organization

The game is built using object-oriented programming with a single main class:

- `BleachTriviaGame`: Main game class that handles all game logic
  - Initialization and file I/O
  - Game state management
  - Question selection and validation
  - Leaderboard management

## Data Files

### questions.json
Contains an array of question objects, each with:
```json
{
  "question": "What's the full name of the captain commander?",
  "options": {
    "A": "Yamamoto Genryuusai Shigekuni",
    "B": "Ukitake Jyuushiro",
    "C": "Kuchiki Byakuya",
    "D": "Hitsugaya Toshiro"
  }
}
```

### answers.json
Contains a mapping of question numbers to correct answers:
```json
{
  "1": "A",
  "2": "B",
  "3": "C",
  ...
}
```

### leaderboard.json
Automatically generated and managed by the game:
```json
{
  "short": [...],
  "medium": [],
  "long": [],
  "top_scores": [...],
  "player_data": {
    "Player1": {
      "answered_questions": ["1", "5", "7"]
    }
  }
}
```

## Adding New Questions

1. Edit `questions.json` to add a new question object to the array
2. Update `answers.json` with the correct answer for the new question
3. The question number corresponds to its position in the array (1-based index)

## Extending the Game

### Adding New Game Modes
1. Update `get_question_count()` to handle the new mode
2. Add the new mode to the main menu in `play_game()`
3. Update the leaderboard initialization in `load_leaderboard()`

### Modifying Scoring
- The scoring logic is in `play_round()` and `update_leaderboard()`
- Modify these methods to implement different scoring systems

## Testing

Run the game and test all features:
1. Different game modes
2. Answer validation
3. Leaderboard updates
4. Question history tracking
5. Error conditions (e.g., corrupted data files)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
