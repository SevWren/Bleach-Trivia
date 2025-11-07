"""
Data loading and saving utilities for the Bleach Trivia game.

This module handles reading and writing game data, including questions,
answers, and leaderboard information.
"""
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from config.settings import PATHS, DEFAULT_ENCODING, INDENT_LEVEL
from utils.validators import validate_file_exists


def load_json_file(file_path: Path) -> Union[Dict, List]:
    """
    Load data from a JSON file.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        The parsed JSON data (dict or list)
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file contains invalid JSON
        OSError: For other I/O related errors
    """
    try:
        with open(file_path, 'r', encoding=DEFAULT_ENCODING) as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        raise
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {file_path}: {e}")
        raise
    except OSError as e:
        print(f"Error reading {file_path}: {e}")
        raise


def save_json_file(data: Any, file_path: Path) -> None:
    """
    Save data to a JSON file.
    
    Args:
        data: The data to save (must be JSON serializable)
        file_path: Path where to save the file
        
    Raises:
        OSError: If there's an error writing the file
        TypeError: If the data is not JSON serializable
    """
    try:
        # Ensure directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding=DEFAULT_ENCODING) as f:
            json.dump(
                data,
                f,
                indent=INDENT_LEVEL,
                ensure_ascii=False,
                default=str
            )
    except OSError as e:
        print(f"Error writing to {file_path}: {e}")
        raise
    except TypeError as e:
        print(f"Error: Data is not JSON serializable: {e}")
        raise


class GameData:
    """Class to handle loading and accessing game data."""
    
    def __init__(self):
        """Initialize the GameData instance and load all game data."""
        self.questions = self._load_questions()
        self.answers = self._load_answers()
        self.leaderboard = self._load_leaderboard()
    
    def _load_questions(self) -> List[Dict[str, Any]]:
        """Load questions from the questions file."""
        if not validate_file_exists(PATHS['QUESTIONS']):
            raise FileNotFoundError(f"Questions file not found: {PATHS['QUESTIONS']}")
        return load_json_file(PATHS['QUESTIONS'])
    
    def _load_answers(self) -> Dict[str, str]:
        """Load answers from the answers file."""
        if not validate_file_exists(PATHS['ANSWERS']):
            raise FileNotFoundError(f"Answers file not found: {PATHS['ANSWERS']}")
        return load_json_file(PATHS['ANSWERS'])
    
    def _load_leaderboard(self) -> Dict[str, Any]:
        """
        Load the leaderboard from file or create a new one.
        
        Returns:
            dict: The leaderboard data with the following structure:
                {
                    'short': [],       # Short game mode scores
                    'medium': [],      # Medium game mode scores
                    'long': [],        # Long game mode scores
                    'top_scores': [],  # Top scores across all modes
                    'player_data': {}  # Player-specific data
                }
        """
        if PATHS['LEADERBOARD'].exists():
            try:
                leaderboard = load_json_file(PATHS['LEADERBOARD'])
                # Ensure all required keys exist
                for key in ['short', 'medium', 'long', 'top_scores', 'player_data']:
                    if key not in leaderboard:
                        leaderboard[key] = [] if key != 'player_data' else {}
                return leaderboard
            except (FileNotFoundError, json.JSONDecodeError):
                print("Warning: Could not load leaderboard. Creating a new one.")
        
        # Return default leaderboard structure
        return {
            'short': [],
            'medium': [],
            'long': [],
            'top_scores': [],
            'player_data': {}
        }
    
    def save_leaderboard(self) -> None:
        """Save the current leaderboard to file."""
        try:
            save_json_file(self.leaderboard, PATHS['LEADERBOARD'])
        except Exception as e:
            print(f"Error saving leaderboard: {e}")
            raise
    
    def get_question(self, question_id: Union[int, str]) -> Dict[str, Any]:
        """
        Get a question by its ID.
        
        Args:
            question_id: The 1-based question ID
            
        Returns:
            dict: The question data
            
        Raises:
            IndexError: If the question ID is out of range
        """
        try:
            return self.questions[int(question_id) - 1]
        except (IndexError, ValueError) as e:
            raise IndexError(f"Invalid question ID: {question_id}") from e
    
    def get_correct_answer(self, question_id: Union[int, str]) -> str:
        """
        Get the correct answer for a question.
        
        Args:
            question_id: The 1-based question ID
            
        Returns:
            str: The correct answer (A, B, C, or D)
            
        Raises:
            KeyError: If the question ID is not found
        """
        try:
            return self.answers[str(question_id)].upper()
        except KeyError as e:
            raise KeyError(f"No answer found for question {question_id}") from e
