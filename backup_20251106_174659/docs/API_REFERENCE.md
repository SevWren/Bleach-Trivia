# Bleach Trivia - API Reference

## Table of Contents
1. [BleachTriviaGame Class](#bleachtriviagame-class)
   - [Initialization](#__init__)
   - [File I/O Methods](#file-io-methods)
   - [Game Logic Methods](#game-logic-methods)
   - [Leaderboard Methods](#leaderboard-methods)
   - [Main Game Loop](#main-game-loop)

## BleachTriviaGame Class

The main class that implements the Bleach Trivia game logic.

### `__init__`

```python
def __init__(self):
    """
    Initialize the BleachTriviaGame instance.
    
    Loads questions, answers, and leaderboard data from JSON files.
    Initializes player name and score.
    """
```

### File I/O Methods

#### `load_questions`

```python
def load_questions(self):
    """
    Load questions from the questions.json file.
    
    Returns:
        list: A list of question dictionaries containing the question text and options.
        
    Raises:
        FileNotFoundError: If questions.json is not found.
        json.JSONDecodeError: If questions.json contains invalid JSON.
    """
```

#### `load_answers`

```python
def load_answers(self):
    """
    Load answers from the answers.json file.
    
    Returns:
        dict: A dictionary mapping question numbers to their correct answers.
        
    Raises:
        FileNotFoundError: If answers.json is not found.
        json.JSONDecodeError: If answers.json contains invalid JSON.
    """
```

#### `load_leaderboard`

```python
def load_leaderboard(self):
    """
    Load the leaderboard from leaderboard.json or create a new one.
    
    Returns:
        dict: The leaderboard data with game mode scores and player data.
        
    Raises:
        IOError: If there's a problem reading the file.
        json.JSONDecodeError: If the file contains invalid JSON.
    """
```

#### `save_leaderboard`

```python
def save_leaderboard(self):
    """
    Save the current leaderboard to leaderboard.json.
    
    The leaderboard is saved with proper indentation and UTF-8 encoding.
    Non-ASCII characters are preserved.
    """
```

### Game Logic Methods

#### `get_question`

```python
def get_question(self, index):
    """
    Retrieve a question by its index.
    
    Args:
        index (int or str): The 1-based index of the question to retrieve.
        
    Returns:
        dict: The question data containing 'question' and 'options'.
    """
```

#### `check_answer`

```python
def check_answer(self, question_num, answer):
    """
    Check if the provided answer is correct for the given question.
    
    Args:
        question_num (int or str): The question number to check.
        answer (str): The answer to check (A, B, C, or D).
        
    Returns:
        bool: True if the answer is correct, False otherwise.
    """
```

### Leaderboard Methods

#### `update_leaderboard`

```python
def update_leaderboard(self, game_mode):
    """
    Update the leaderboard with the current player's score.
    
    Args:
        game_mode (str): The game mode ('short', 'medium', or 'long').
    """
```

#### `get_player_answered_questions`

```python
def get_player_answered_questions(self, player_name):
    """
    Get the set of questions a player has already answered.
    
    Args:
        player_name (str): The name of the player.
        
    Returns:
        set: A set of question numbers that the player has already answered.
    """
```

#### `update_player_answered_questions`

```python
def update_player_answered_questions(self, player_name, question_numbers):
    """
    Update the set of questions a player has answered.
    
    Args:
        player_name (str): The name of the player.
        question_numbers (list): List of question numbers to add to the player's history.
    """
```

### Main Game Loop

#### `play_game`

```python
def play_game(self):
    """
    Main game loop that handles the main menu and game flow.
    
    This method runs in a loop until the user chooses to exit.
    """
```

#### `play_round`

```python
def play_round(self, game_mode):
    """
    Play a single round of the trivia game in the specified mode.
    
    Args:
        game_mode (str): The game mode ('short', 'medium', or 'long').
    """
```

#### `show_leaderboards`

```python
def show_leaderboards(self, show_prompt=True):
    """
    Display the leaderboards for all game modes and top scores.
    
    Args:
        show_prompt (bool): If True, waits for user to press Enter before continuing.
    """
```

## Data Structures

### Question Object
```python
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

### Score Entry
```python
{
    "name": "Player1",
    "score": 4,
    "total": 5,
    "mode": "short"  # Only in top_scores
}
```

## Error Handling

The game handles various error conditions including:
- Missing or corrupted data files
- Invalid user input
- File I/O errors

All errors are caught and appropriate messages are displayed to the user.
