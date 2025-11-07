"""
Input validation utilities for the Bleach Trivia game.

This module provides functions to validate various types of user input,
including player names, menu selections, and game answers.
"""
import re
from typing import Any, Optional, TypeVar, Type, Callable
from pathlib import Path

from config.settings import VALIDATION, DISPLAY

T = TypeVar('T')

def validate_input(
    prompt: str,
    input_type: Type[T],
    validation_func: Optional[Callable[[Any], bool]] = None,
    error_message: str = "Invalid input. Please try again.",
    allow_empty: bool = False
) -> T:
    """
    Generic input validation function.
    
    Args:
        prompt: The prompt to display to the user
        input_type: The expected type of the input
        validation_func: Optional function to validate the input
        error_message: Error message to display on validation failure
        allow_empty: Whether empty input is allowed
        
    Returns:
        The validated input of the specified type
        
    Raises:
        ValueError: If input cannot be converted to the specified type
        KeyboardInterrupt: If user presses Ctrl+C
    """
    while True:
        try:
            user_input = input(prompt).strip()
            
            if not user_input and not allow_empty:
                print("Input cannot be empty.")
                continue
                
            if not user_input and allow_empty:
                return None
                
            # Convert to the desired type
            converted = input_type(user_input)
            
            # Apply additional validation if provided
            if validation_func and not validation_func(converted):
                print(error_message)
                continue
                
            return converted
            
        except ValueError:
            print(f"Please enter a valid {input_type.__name__}.")
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            raise

def validate_player_name(name: str) -> bool:
    """
    Validate a player's name.
    
    Args:
        name: The name to validate
        
    Returns:
        bool: True if the name is valid, False otherwise
    """
    if not name:
        return False
        
    min_len = VALIDATION['MIN_PLAYER_NAME_LENGTH']
    max_len = VALIDATION['MAX_PLAYER_NAME_LENGTH']
    allowed_chars = VALIDATION['ALLOWED_SPECIAL_CHARS']
    
    # Check length
    if not (min_len <= len(name) <= max_len):
        print(f"Name must be between {min_len} and {max_len} characters long.")
        return False
    
    # Check for invalid characters
    pattern = f'^[\w{re.escape(allowed_chars)}]+$'
    if not re.match(pattern, name):
        print(f"Name can only contain letters, numbers, and these special characters: {allowed_chars}")
        return False
        
    return True

def validate_menu_choice(choice: str, min_val: int, max_val: int) -> bool:
    """
    Validate a menu choice.
    
    Args:
        choice: The user's input
        min_val: Minimum valid choice
        max_val: Maximum valid choice
        
    Returns:
        bool: True if the choice is valid, False otherwise
    """
    if not choice.isdigit():
        return False
    
    choice_num = int(choice)
    return min_val <= choice_num <= max_val

def validate_answer(answer: str) -> bool:
    """
    Validate a game answer.
    
    Args:
        answer: The answer to validate
        
    Returns:
        bool: True if the answer is valid, False otherwise
    """
    return answer.upper() in VALIDATION['VALID_ANSWERS']

def validate_file_exists(file_path: Path) -> bool:
    """
    Check if a file exists and is readable.
    
    Args:
        file_path: Path to the file
        
    Returns:
        bool: True if the file exists and is readable, False otherwise
    """
    if not file_path.exists():
        print(f"Error: File not found: {file_path}")
        return False
    if not file_path.is_file():
        print(f"Error: Not a file: {file_path}")
        return False
    if not os.access(file_path, os.R_OK):
        print(f"Error: Cannot read file (permission denied): {file_path}")
        return False
    return True

def get_valid_player_name() -> str:
    """
    Prompt the user for a valid player name.
    
    Returns:
        str: A valid player name
    """
    while True:
        name = input("\nEnter your name: ").strip()
        if validate_player_name(name):
            return name
        print(f"Please enter a name between {VALIDATION['MIN_PLAYER_NAME_LENGTH']} "
              f"and {VALIDATION['MAX_PLAYER_NAME_LENGTH']} characters.")

def get_valid_menu_choice(prompt: str, min_val: int, max_val: int) -> int:
    """
    Prompt the user for a valid menu choice.
    
    Args:
        prompt: The prompt to display
        min_val: Minimum valid choice
        max_val: Maximum valid choice
        
    Returns:
        int: The user's valid menu choice
    """
    while True:
        choice = input(prompt).strip()
        if validate_menu_choice(choice, min_val, max_val):
            return int(choice)
        print(f"Please enter a number between {min_val} and {max_val}.")

def get_valid_answer(prompt: str) -> str:
    """
    Prompt the user for a valid answer.
    
    Args:
        prompt: The prompt to display
        
    Returns:
        str: The user's valid answer (uppercase)
    """
    while True:
        answer = input(prompt).strip().upper()
        if validate_answer(answer):
            return answer
        print(f"Please enter a valid answer ({', '.join(sorted(VALIDATION['VALID_ANSWERS']))}).")
