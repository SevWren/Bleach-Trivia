"""
User Interface components for the Bleach Trivia game.

This module provides functions for displaying game information,
menus, and handling user interactions in a consistent way.
"""
from typing import Dict, List, Optional, Any, Callable

from config.settings import DISPLAY, GAME_MODES
from utils.validators import (
    get_valid_menu_choice,
    get_valid_answer,
    get_valid_player_name
)


def clear_screen() -> None:
    """Clear the terminal screen."""
    print("\033[H\033[J", end="")  # ANSI escape code to clear screen


def display_header(title: str) -> None:
    """
    Display a formatted header.
    
    Args:
        title: The title to display in the header
    """
    print("\n" + "=" * 60)
    print(f"{title:^60}")
    print("=" * 60 + "\n")


def display_menu(title: str, options: Dict[str, str]) -> str:
    """
    Display a menu and get user's choice.
    
    Args:
        title: The menu title
        options: Dictionary of option_number: description
        
    Returns:
        str: The user's choice
    """
    display_header(title)
    
    # Sort options by key (menu number)
    sorted_options = sorted(options.items(), key=lambda x: x[0])
    
    # Display menu options
    for option_num, description in sorted_options:
        print(f"{option_num}. {description}")
    
    # Get and validate user choice
    min_choice = min(int(k) for k in options.keys())
    max_choice = max(int(k) for k in options.keys())
    
    choice = get_valid_menu_choice(
        f"\nEnter your choice ({min_choice}-{max_choice}): ",
        min_choice,
        max_choice
    )
    
    return str(choice)


def display_game_modes() -> str:
    """
    Display the game mode selection menu.
    
    Returns:
        str: The selected game mode key (e.g., 'short', 'medium', 'long')
    """
    display_header("Select Game Mode")
    
    # Create menu options from game modes
    options = {}
    for i, (mode_key, mode_info) in enumerate(GAME_MODES.items(), 1):
        options[str(i)] = f"{mode_info['name']} - {mode_info['description']}"
    
    # Add option to go back
    options[str(len(options) + 1)] = "Back to Main Menu"
    
    # Display menu and get choice
    choice = display_menu("Game Modes", options)
    
    # Convert numeric choice back to mode key
    if choice == str(len(options)):  # Last option is "Back"
        return "back"
    
    # Get the selected mode key
    mode_key = list(GAME_MODES.keys())[int(choice) - 1]
    return mode_key


def display_question(question_data: Dict[str, Any], question_num: int, total_questions: int) -> str:
    """
    Display a question and get the user's answer.
    
    Args:
        question_data: The question data containing 'question' and 'options'
        question_num: The current question number
        total_questions: Total number of questions in the game
        
    Returns:
        str: The user's answer (A, B, C, or D)
    """
    # Display question number and text
    print(f"\nQuestion {question_num} of {total_questions}")
    print("-" * 60)
    print(question_data["question"])
    print()
    
    # Display answer options
    for option, text in question_data["options"].items():
        print(f"{option}. {text}")
    
    # Get and validate user's answer
    return get_valid_answer("\nYour answer (A/B/C/D): ")


def display_results(score: int, total: int) -> None:
    """
    Display the game results.
    
    Args:
        score: Number of correct answers
        total: Total number of questions
    """
    percentage = (score / total) * 100 if total > 0 else 0
    
    print("\n" + "=" * 60)
    print("GAME OVER!")
    print("=" * 60)
    print(f"Your score: {score} out of {total} ({percentage:.1f}%)")
    
    # Add some fun messages based on performance
    if percentage >= 90:
        print("🏆 Amazing! You're a true Bleach expert!")
    elif percentage >= 70:
        print("👍 Great job! You know your Bleach!")
    elif percentage >= 50:
        print("Not bad! Keep practicing!")
    else:
        print("Keep watching Bleach and try again!")
    
    print("\nPress Enter to continue...", end="")
    input()


def display_leaderboard(leaderboard: Dict[str, Any], mode: str = None) -> None:
    """
    Display the leaderboard.
    
    Args:
        leaderboard: The leaderboard data
        mode: Optional game mode to filter by
    """
    display_header("Leaderboard")
    
    if mode:
        # Display specific mode leaderboard
        mode_name = GAME_MODES[mode]['name']
        print(f"🏆 {mode_name} Leaderboard 🏆\n")
        _display_leaderboard_table(leaderboard[mode], show_mode=False)
    else:
        # Display top scores across all modes
        print("🏆 Top Scores (All Modes) 🏆\n")
        _display_leaderboard_table(leaderboard['top_scores'], show_mode=True)
    
    print("\nPress Enter to continue...", end="")
    input()


def _display_leaderboard_table(scores: List[Dict[str, Any]], show_mode: bool = False) -> None:
    """
    Helper function to display a leaderboard table.
    
    Args:
        scores: List of score entries
        show_mode: Whether to show the game mode column
    """
    if not scores:
        print("No scores yet. Be the first to play!")
        return
    
    # Prepare table header
    header = ["Rank", "Name", "Score", "Total", "%", "Date"]
    if show_mode:
        header.insert(4, "Mode")
    
    # Print table header
    print(" | ".join(header))
    print("-" * 80)
    
    # Print each score
    for i, entry in enumerate(scores[:10], 1):
        name = entry.get('name', 'Unknown')[:20]
        score = entry.get('score', 0)
        total = entry.get('total', 1)
        percentage = (score / total) * 100 if total > 0 else 0
        date = entry.get('date', 'N/A')
        
        row = [
            str(i).rjust(3),
            name.ljust(20),
            str(score).rjust(5),
            str(total).rjust(5),
            f"{percentage:5.1f}%"
        ]
        
        if show_mode:
            mode = entry.get('mode', 'N/A')
            row.insert(4, mode.capitalize().ljust(6))
        
        row.append(date)
        print(" | ".join(row))
