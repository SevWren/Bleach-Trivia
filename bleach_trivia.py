"""
Bleach Trivia Game

A command-line trivia game based on the Bleach anime/manga series.
Players can test their knowledge with different game modes and track their scores.
"""

import json
import random
import os
import sys
from pathlib import Path

class BleachTriviaGame:
    """
    A class representing the Bleach Trivia Game.
    
    This class handles the game logic, question management, and leaderboard functionality.
    """
    
    def __init__(self):
        """
        Initialize the BleachTriviaGame instance.
        
        Loads questions, answers, and leaderboard data from JSON files.
        Initializes player name and score.
        """
        self.questions = self.load_questions()
        self.answers = self.load_answers()
        self.leaderboard = self.load_leaderboard()
        self.player_name = ""
        self.current_score = 0

    def get_base_path(self):
        """Get the base path for file operations, works with PyInstaller"""
        if getattr(sys, 'frozen', False):
            # If the application is run as a bundle, the PyInstaller bootloader
            # extends the sys module by a flag frozen=True and sets the app 
            # path into variable _MEIPASS'.
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
        return base_path

    def get_data_path(self, filename):
        """Get the full path to a data file"""
        # First try the current working directory
        cwd_path = Path(filename)
        if cwd_path.exists():
            return str(cwd_path)
            
        # Then try the application directory
        base_path = self.get_base_path()
        app_path = Path(base_path) / filename
        if app_path.exists():
            return str(app_path)
            
        # If not found, return the original filename (will raise FileNotFoundError)
        return filename

    def load_questions(self):
        """
        Load questions from the questions.json file.
        
        Returns:
            list: A list of question dictionaries containing the question text and options.
            
        Raises:
            FileNotFoundError: If questions.json is not found.
            json.JSONDecodeError: If questions.json contains invalid JSON.
        """
        questions_path = self.get_data_path('questions.json')
        with open(questions_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def load_answers(self):
        """
        Load answers from the answers.json file.
        
        Returns:
            dict: A dictionary mapping question numbers to their correct answers.
            
        Raises:
            FileNotFoundError: If answers.json is not found.
            json.JSONDecodeError: If answers.json contains invalid JSON.
        """
        answers_path = self.get_data_path('answers.json')
        with open(answers_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def load_leaderboard(self):
        """
        Load the leaderboard from leaderboard.json or create a new one if it doesn't exist.
        
        Returns:
            dict: The leaderboard data with the following structure:
                {
                    'short': [],       # Short game mode scores
                    'medium': [],      # Medium game mode scores
                    'long': [],        # Long game mode scores
                    'top_scores': [],  # Top scores across all modes
                    'player_data': {}  # Player-specific data including answered questions
                }
                    
        Raises:
            IOError: If there's a problem reading the leaderboard file
            json.JSONDecodeError: If the file contains invalid JSON
        """
        if os.path.exists('leaderboard.json'):
            try:
                with open('leaderboard.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Ensure backward compatibility with old leaderboard format
                    if 'player_data' not in data:
                        data['player_data'] = {}
                    return data
            except json.JSONDecodeError as e:
                print("Warning: Leaderboard file is corrupted. Creating a new one.")
            except Exception as e:
                print(f"Error reading leaderboard: {e}")
                print("Starting with a fresh leaderboard.")
                
        return {
            "short": [],
            "medium": [],
            "long": [],
            "top_scores": [],
            "player_data": {}
        }

    def save_leaderboard(self):
        """Save the leaderboard to leaderboard.json"""
        try:
            # First try saving in the application directory
            leaderboard_path = self.get_data_path('leaderboard.json')
            with open(leaderboard_path, 'w', encoding='utf-8') as f:
                json.dump(self.leaderboard, f, indent=4)
        except (IOError, OSError):
            # If that fails, try saving in the current working directory
            with open('leaderboard.json', 'w', encoding='utf-8') as f:
                json.dump(self.leaderboard, f, indent=4)

    def get_question(self, index):
        """
        Retrieve a question by its index.
        
        Args:
            index (int or str): The 1-based index of the question to retrieve.
            
        Returns:
            dict: The question data containing 'question' and 'options'.
            
        Raises:
            ValueError: If the index is out of range or invalid.
            
        Note:
            The index is converted from 1-based to 0-based internally.
            Valid indices are from 1 to the number of questions.
        """
        try:
            idx = int(index) - 1
            if idx < 0 or idx >= len(self.questions):
                raise ValueError(
                    f"Question index must be between 1 and {len(self.questions)}, got {index}"
                )
            return self.questions[idx]
        except (ValueError, TypeError) as e:
            if "must be between" in str(e):
                raise
            raise ValueError(
                f"Invalid question index: {index}. "
                f"Please provide a valid number between 1 and {len(self.questions)}"
            ) from None

    def check_answer(self, question_num, answer):
        """
        Check if the provided answer is correct for the given question.
        
        Args:
            question_num (int or str): The question number to check.
            answer (str): The answer to check (A, B, C, or D).
            
        Returns:
            bool: True if the answer is correct, False otherwise.
            
        Note:
            The comparison is case-insensitive.
        """
        return self.answers.get(str(question_num), "").upper() == answer.upper()

    def update_leaderboard(self, game_mode):
        """
        Update the leaderboard with the current player's score.
        
        This method updates both the specific game mode leaderboard and the overall top scores.
        The leaderboard is then saved to disk.
        
        Args:
            game_mode (str): The game mode ('short', 'medium', or 'long').
            
        Note:
            The leaderboard is sorted by score (descending) and then by total questions (ascending).
            The top scores are sorted by percentage correct (score/total).
            Only the top 10 scores are kept in the top_scores list.
        """
        # Add to specific game mode leaderboard
        self.leaderboard[game_mode].append({
            "name": self.player_name,
            "score": self.current_score,
            "total": self.get_question_count(game_mode)
        })
        
        # Sort the specific leaderboard by score (descending) and total (ascending)
        self.leaderboard[game_mode].sort(key=lambda x: (-x["score"], x["total"]))
        
        # Add to top scores
        self.leaderboard["top_scores"].append({
            "name": self.player_name,
            "score": self.current_score,
            "total": self.get_question_count(game_mode),
            "mode": game_mode
        })
        
        # Sort top scores by percentage (descending) and keep top 10
        self.leaderboard["top_scores"].sort(
            key=lambda x: (x["score"]/x["total"], x["score"]), 
            reverse=True
        )
        self.leaderboard["top_scores"] = self.leaderboard["top_scores"][:10]
        
        self.save_leaderboard()
        
    def get_player_answered_questions(self, player_name):
        """
        Get the set of questions a player has already answered.
        
        Args:
            player_name (str): The name of the player
            
        Returns:
            set: A set of question numbers that the player has already answered
            
        Note:
            Initializes a new player entry in the leaderboard if they don't exist
        """
        if 'player_data' not in self.leaderboard:
            self.leaderboard['player_data'] = {}
        if player_name not in self.leaderboard['player_data']:
            self.leaderboard['player_data'][player_name] = {'answered_questions': []}
            self.save_leaderboard()  # Save after initializing new player
        return set(self.leaderboard['player_data'][player_name].get('answered_questions', []))
        
    def update_player_answered_questions(self, player_name, question_numbers):
        """Update the set of questions a player has answered."""
        if 'player_data' not in self.leaderboard:
            self.leaderboard['player_data'] = {}
        if player_name not in self.leaderboard['player_data']:
            self.leaderboard['player_data'][player_name] = {'answered_questions': []}
            
        # Convert to list of strings for JSON serialization
        current_questions = set(self.leaderboard['player_data'][player_name].get('answered_questions', []))
        current_questions.update(str(q) for q in question_numbers)
        
        # If all questions have been answered, reset for this player
        if len(current_questions) >= len(self.questions):
            self.leaderboard['player_data'][player_name]['answered_questions'] = []
        else:
            self.leaderboard['player_data'][player_name]['answered_questions'] = list(current_questions)

    def get_question_count(self, game_mode):
        """
        Get the number of questions for a specific game mode.
        
        Args:
            game_mode (str): The game mode ('short', 'medium', or 'long').
            
        Returns:
            int: Number of questions for the specified game mode.
                 - Short: 5 questions
                 - Medium: 20 questions
                 - Long: 50 questions
        """
        if game_mode == "short":
            return 5
        elif game_mode == "medium":
            return 20
        else:  # long
            return 50

    def play_game(self):
        """
        Main game loop that handles the main menu and game flow.
        
        This method displays the main menu and processes user input to start games,
        view leaderboards, or exit the application.
        
        The method runs in a loop until the user chooses to exit.
        """
        print("Welcome to Bleach Trivia!")
        while True:
            self.player_name = input("Enter your name (cannot be empty): ").strip()
            if self.player_name:  # Ensure name is not empty
                break
            print("Error: Name cannot be empty. Please enter a valid name.")
        
        while True:
            print("\nGame Modes:")
            print("1. Short (5 questions)")
            print("2. Medium (20 questions)")
            print("3. Long (50 questions)")
            print("4. View Leaderboards")
            print("5. Exit")
            
            choice = input("\nSelect an option (1-5): ").strip()
            
            if choice == "1":
                self.play_round("short")
            elif choice == "2":
                self.play_round("medium")
            elif choice == "3":
                self.play_round("long")
            elif choice == "4":
                self.show_leaderboards()
            elif choice == "5":
                print("Thanks for playing Bleach Trivia!")
                break
            else:
                print("Invalid choice. Please try again.")

    def play_round(self, game_mode):
        """
        Play a single round of the trivia game in the specified mode.
        
        This method handles the game logic for a single round, including:
        - Selecting appropriate questions
        - Presenting questions to the player
        - Accepting and validating answers
        - Updating the score
        - Updating the leaderboard
        
        Args:
            game_mode (str): The game mode ('short', 'medium', or 'long').
        """
        self.current_score = 0
        question_count = self.get_question_count(game_mode)
        
        # Get player's answered questions
        answered_questions = self.get_player_answered_questions(self.player_name)
        
        # Get random questions that haven't been answered yet by this player
        available_questions = [str(i+1) for i in range(len(self.questions)) 
                             if str(i+1) not in answered_questions]
        
        # If not enough unique questions left, reset for this player
        if len(available_questions) < question_count:
            print("\nYou've answered most questions! Resetting your question history for a fresh start.")
            self.leaderboard['player_data'][self.player_name]['answered_questions'] = []
            # Only include questions that haven't been selected in this game
            available_questions = [str(i+1) for i in range(len(self.questions)) 
                                 if str(i+1) not in selected_questions]
        
        # Select questions
        selected_questions = random.sample(available_questions, min(question_count, len(available_questions)))
        
        print(f"\nStarting {game_mode.capitalize()} game with {len(selected_questions)} questions!")
        
        # Ask each question
        for i, q_num in enumerate(selected_questions, 1):
            question_data = self.get_question(q_num)
            print(f"\nQuestion {i}:")
            print(question_data["question"])
            
            # Display answer options
            for option, text in question_data["options"].items():
                print(f"{option}. {text}")
            
            # Get and validate user input
            while True:
                answer = input("Your answer (A/B/C/D): ").strip().upper()
                if answer in ["A", "B", "C", "D"]:
                    break
                print("Invalid input. Please enter A, B, C, or D.")
            
            # Check answer and update score
            if self.check_answer(q_num, answer):
                print("Correct!")
                self.current_score += 1
            else:
                correct_answer = self.answers.get(q_num, "")
                print(f"Wrong! The correct answer was {correct_answer}.")
        
        # Update the player's answered questions
        self.update_player_answered_questions(self.player_name, selected_questions)
        
        # Show final results and update leaderboard
        print(f"\nGame Over! Your score: {self.current_score}/{len(selected_questions)}")
        self.update_leaderboard(game_mode)
        
        # Show final results and leaderboard
        print("\nFinal Results:")
        self.show_leaderboards(show_prompt=False)
        input("\nPress Enter to return to the main menu...")

    def show_leaderboards(self, show_prompt=True):
        """
        Display the leaderboards for all game modes and top scores.
        
        This method shows:
        1. Top scores across all game modes
        2. Individual leaderboards for each game mode (short, medium, long)
        
        Args:
            show_prompt (bool): If True, waits for user to press Enter before continuing.
        """
        print("\n--- Leaderboards ---")
        
        # Show top scores only if there are any
        if self.leaderboard["top_scores"]:
            print("\nTop Scores (All Modes):")
            print("Rank | Name           | Score | Total | Mode   | %")
            print("-" * 50)
            for i, entry in enumerate(self.leaderboard["top_scores"][:10], 1):
                percentage = (entry["score"] / entry["total"]) * 100
                print(f"{i:4d} | {entry['name'][:13]:<13} | {entry['score']:5d} | {entry['total']:5d} | {entry['mode']:6s} | {percentage:.1f}%")
        else:
            print("\nNo top scores yet. Be the first to play!")
        
        # Show mode-specific leaderboards
        for mode in ["short", "medium", "long"]:
            if self.leaderboard[mode]:
                print(f"\n{'-'*10} {mode.upper()} MODE {'-'*10}")
                print("Rank | Name           | Score | Total | %")
                print("-" * 40)
                for i, entry in enumerate(self.leaderboard[mode][:10], 1):
                    percentage = (entry["score"] / entry["total"]) * 100
                    print(f"{i:4d} | {entry['name'][:13]:<13} | {entry['score']:5d} | {entry['total']:5d} | {percentage:.1f}%")
        
        if show_prompt:
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    """
    Entry point for the Bleach Trivia Game.
    
    This block initializes the game and handles any unexpected errors,
    ensuring the leaderboard is always saved before exiting.
    """
    game = BleachTriviaGame()
    try:
        game.play_game()
    except KeyboardInterrupt:
        print("\nGame ended by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        game.save_leaderboard()
