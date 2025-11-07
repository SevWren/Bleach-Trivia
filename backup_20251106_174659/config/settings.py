"""
Configuration settings for Bleach Trivia Game.

This module provides a centralized configuration system for the Bleach Trivia game,
including file paths, game settings, display options, and validation rules.
"""
from pathlib import Path
from typing import Dict, Any, TypedDict, Final

# Base directory paths
class Paths(TypedDict):
    """File path configuration."""
    BASE: Path
    DATA: Path
    QUESTIONS: Path
    ANSWERS: Path
    LEADERBOARD: Path

# Initialize paths
PATHS: Paths = {
    'BASE': Path(__file__).parent.parent,
    'DATA': Path(__file__).parent.parent / 'data'
}
PATHS.update({
    'QUESTIONS': PATHS['DATA'] / 'questions.json',
    'ANSWERS': PATHS['DATA'] / 'answers.json',
    'LEADERBOARD': PATHS['DATA'] / 'leaderboard.json'
})

# Game mode configuration
class GameModeConfig(TypedDict):
    """Configuration for a game mode."""
    name: str
    questions: int
    description: str

GAME_MODES: Dict[str, GameModeConfig] = {
    'short': {
        'name': 'Short Game',
        'questions': 5,
        'description': 'A quick 5-question challenge (5-10 minutes)'
    },
    'medium': {
        'name': 'Medium Game',
        'questions': 20,
        'description': 'A standard 20-question challenge (15-30 minutes)'
    },
    'long': {
        'name': 'Long Game',
        'questions': 50,
        'description': 'An epic 50-question challenge (30-60 minutes)'
    }
}

# Display settings
class DisplayConfig(TypedDict):
    """Display and UI configuration."""
    MAX_NAME_LENGTH: int
    LEADERBOARD_TOP_N: int
    PROMPT: str
    SEPARATOR: str

DISPLAY: DisplayConfig = {
    'MAX_NAME_LENGTH': 20,
    'LEADERBOARD_TOP_N': 10,
    'PROMPT': '> ',
    'SEPARATOR': '-' * 50
}

# Input validation rules
class ValidationRules(TypedDict):
    """Input validation rules and constraints."""
    VALID_ANSWERS: set[str]
    MIN_PLAYER_NAME_LENGTH: int
    MAX_PLAYER_NAME_LENGTH: int
    ALLOWED_SPECIAL_CHARS: str

VALIDATION: ValidationRules = {
    'VALID_ANSWERS': {'A', 'B', 'C', 'D'},
    'MIN_PLAYER_NAME_LENGTH': 1,
    'MAX_PLAYER_NAME_LENGTH': 20,
    'ALLOWED_SPECIAL_CHARS': ' _-.'
}

# Constants
DEFAULT_ENCODING: Final[str] = 'utf-8'
INDENT_LEVEL: Final[int] = 2


def ensure_data_directory() -> None:
    """Ensure the data directory exists."""
    PATHS['DATA'].mkdir(exist_ok=True, parents=True)


def validate_settings() -> None:
    """
    Validate that all required configuration is correct.
    
    Raises:
        FileNotFoundError: If required files are missing
        ValueError: If configuration values are invalid
    """
    # Check if required files exist
    required_files = [PATHS['QUESTIONS'], PATHS['ANSWERS']]
    for file_path in required_files:
        if not file_path.exists():
            raise FileNotFoundError(f"Required file not found: {file_path}")
    
    # Validate game modes
    if not GAME_MODES:
        raise ValueError("At least one game mode must be configured")
    
    for mode_id, mode in GAME_MODES.items():
        if not isinstance(mode['questions'], int) or mode['questions'] <= 0:
            raise ValueError(f"Invalid question count for mode {mode_id}")


# Initialize and validate settings
ensure_data_directory()
validate_settings()
