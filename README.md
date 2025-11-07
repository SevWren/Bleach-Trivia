# Bleach Trivia Game

A command-line trivia game based on the popular anime/manga series Bleach. Test your knowledge of the series with various game modes and compete for the top scores on the leaderboard.

## ✨ Features

- **Multiple Game Modes**:
  - Short: 5 questions
  - Medium: 20 questions
  - Long: 50 questions
- **Comprehensive Leaderboard**:
  - Tracks scores across all game modes
  - Shows percentage correct
  - Maintains separate rankings for each game mode
  - Tracks player progress and question history
- **Smart Question Selection**:
  - Prevents question repetition
  - Tracks answered questions per player
  - Resets after all questions are used
- **Player Progress**:
  - Saves individual player statistics
  - Tracks questions answered correctly/incorrectly
  - Maintains history across game sessions
- **User Experience**:
  - Clean, intuitive interface
  - Full Unicode character support
  - Clear feedback on answers

## 🚀 Requirements

- Python 3.8 or higher
- No external dependencies required
- Compatible with Windows, macOS, and Linux

## ⚡ Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/bleach-trivia.git
   cd bleach-trivia
   ```

2. **Run the game**:
   ```bash
   python main.py
   ```

3. **Follow the on-screen instructions to play!**

## 🏗️ Project Structure

```
bleach-trivia/
├── README.md           # Project documentation
├── main.py            # Main entry point
├── bleach_trivia.py   # Core game logic and classes
├── questions.json     # Trivia questions database
├── answers.json       # Correct answers
├── leaderboard.json   # Player scores and progress (auto-generated)
└── test_game.py       # Automated test script
```

## 🎮 How to Play

1. **Start the game**:
   ```bash
   python main.py
   ```

2. **Enter your name** when prompted (cannot be empty)

3. **Choose a game mode**:
   - `1` - Short (5 questions)
   - `2` - Medium (20 questions)
   - `3` - Long (50 questions)
   - `4` - View Leaderboards
   - `5` - Exit

4. **Answer questions**:
   - Read each question carefully
   - Enter A, B, C, or D to select your answer
   - Get immediate feedback on your answer

5. **View your results**:
   - See your final score
   - Compare with the leaderboard
   - View detailed statistics

## 🧪 Testing

Run the automated test script to verify all game functionality:

```bash
python test_game.py
```

This will simulate a complete game session with predefined inputs.

## 🐛 Troubleshooting

### Common Issues:
- **Unicode Characters Not Displaying**:
  - Ensure your terminal supports UTF-8 encoding
  - On Windows, try running in Windows Terminal or PowerShell

- **File Permission Errors**:
  - Make sure the application has write permissions for `leaderboard.json`

- **Corrupted Data**:
  - If you encounter issues, you can safely delete `leaderboard.json` to reset all scores

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Report Bugs**:
   - Open an issue with detailed reproduction steps
   - Include your Python version and operating system

2. **Suggest Improvements**:
   - Open an issue with your ideas
   - Explain the proposed changes

3. **Submit Pull Requests**:
   - Fork the repository
   - Create a feature branch
   - Submit a pull request with a clear description

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📚 Resources

- [Bleach Wiki](https://bleach.fandom.com/)
- [Python Documentation](https://docs.python.org/3/)

---

<div align="center">
  Made with ❤️ by Bleach Fans | 2025
</div>
