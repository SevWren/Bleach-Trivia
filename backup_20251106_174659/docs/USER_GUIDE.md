# Bleach Trivia - User Guide

## Table of Contents
1. [Getting Started](#getting-started)
2. [Game Modes](#game-modes)
3. [How to Play](#how-to-play)
4. [Scoring System](#scoring-system)
5. [Leaderboards](#leaderboards)
6. [Frequently Asked Questions](#frequently-asked-questions)

## Getting Started

1. Ensure you have Python 3.6 or higher installed on your system
2. Download or clone the Bleach Trivia game files
3. Open a terminal/command prompt in the game directory
4. Run the game: `python bleach_trivia.py`

## Game Modes

Bleach Trivia offers three different game modes:

- **Short Game**: 5 questions, perfect for a quick break
- **Medium Game**: 20 questions, a balanced challenge
- **Long Game**: 50 questions, for true Bleach experts

## How to Play

1. **Starting the Game**:
   - Launch the game and enter your name when prompted
   - Select a game mode from the main menu

2. **Answering Questions**:
   - Read each question carefully
   - Type the letter (A, B, C, or D) corresponding to your answer
   - Press Enter to submit your answer

3. **Game Progress**:
   - Your score is displayed after each question
   - The game tracks which questions you've already seen
   - After completing all questions, your final score will be shown

## Scoring System

- Each correct answer awards 1 point
- No points are deducted for incorrect answers
- Your score is shown as a fraction (e.g., 4/5 means 4 correct out of 5 questions)
- The leaderboard tracks both your raw score and percentage correct

## Leaderboards

The game maintains several leaderboards:

1. **Top Scores**: Shows the highest percentage scores across all game modes
2. **Mode-Specific Leaderboards**: Separate rankings for each game mode

Your score is automatically saved when you complete a game. The leaderboard shows:
- Player name
- Score (correct answers)
- Total questions
- Percentage correct

## Frequently Asked Questions

**Q: Can I play the same questions again?**
A: The game will cycle through all available questions before repeating any. After you've seen all questions, your history will reset.

**Q: How are ties handled on the leaderboard?**
A: Ties are first broken by percentage correct, then by the raw score.

**Q: Can I change my name between games?**
A: Yes, simply exit and restart the game to enter a different name.

**Q: Where is my progress saved?**
A: All game data is saved in `leaderboard.json` in the game directory.

**Q: How many questions are in the game?**
A: The game includes 100 unique Bleach trivia questions.

For any other questions or issues, please refer to the [Developer Guide](DEVELOPER_GUIDE.md) or open an issue in the project repository.
