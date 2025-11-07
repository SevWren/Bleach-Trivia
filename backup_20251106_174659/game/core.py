"""
Core game logic for the Bleach Trivia game.

This module contains the main game class that orchestrates the game flow,
manages game state, and coordinates between different components.
"""
import random
from typing import Dict, List, Set, Optional, Tuple
from datetime import datetime

from config.settings import GAME_MODES
from utils.data_loader import GameData
from .ui import (
    display_question,
    display_results,
    display_leaderboard,
    display_menu,
    display_game_modes,
    clear_screen,
    display_header
)
from utils.validators import get_valid_player_name


class BleachTriviaGame:
    """
    Main game class for the Bleach Trivia game.
    
    This class manages the game state, handles user interactions,
    and coordinates between different game components.
    """
    
    def __init__(self):
        """Initialize the game with data and state."""
        self.data = GameData()
        self.player_name: str = ""
        self.current_score: int = 0
        self.current_mode: Optional[str] = None
        self.answered_questions: Set[str] = set()
    
    def start(self) -> None:
        """Start the main game loop."""
        try:
            self._show_welcome_screen()
            self._main_menu()
        except KeyboardInterrupt:
            print("\nThanks for playing Bleach Trivia!")
        except Exception as e:
            print(f"\nAn error occurred: {e}")
        finally:
            # Ensure leaderboard is saved before exiting
            self.data.save_leaderboard()
    
    def _show_welcome_screen(self) -> None:
        """Display the welcome screen and get player name."""
        clear_screen()
        display_header("BLEACH TRIVIA")
        print("Welcome to Bleach Trivia! Test your knowledge of the Bleach universe.\n")
        self.player_name = get_valid_player_name()
        self.answered_questions = self._get_player_answered_questions()
    
    def _main_menu(self) -> None:
        """Display the main menu and handle user choices."""
        while True:
            clear_screen()
            choice = display_menu("Main Menu", {
                "1": "Play Game",
                "2": "View Leaderboards",
                "3": "Exit"
            })
            
            if choice == "1":
                self._play_game_flow()
            elif choice == "2":
                self._show_leaderboards()
            elif choice == "3":
                print("\nThanks for playing Bleach Trivia!")
                break
    
    def _play_game_flow(self) -> None:
        """Handle the game play flow from mode selection to results."""
        # Select game mode
        mode = self._select_game_mode()
        if mode == "back":
            return
            
        self.current_mode = mode
        self.current_score = 0
        
        # Play the game
        self._play_round(mode)
        
        # Show results and update leaderboard
        self._handle_game_completion(mode)
    
    def _select_game_mode(self) -> str:
        """Let the player select a game mode."""
        while True:
            clear_screen()
            mode = display_game_modes()
            
            if mode == "back":
                return mode
                
            # Validate that we have enough questions
            required_questions = GAME_MODES[mode]["questions"]
            available_questions = self._get_available_questions()
            
            if len(available_questions) < required_questions:
                print(f"\nNot enough unique questions available for {GAME_MODES[mode]['name']}.")
                print("Please play a different mode or reset your progress.")
                input("\nPress Enter to continue...")
                continue
                
            return mode
    
    def _play_round(self, mode: str) -> None:
        """Play a single round of the game.
        
        Args:
            mode: The selected game mode (short, medium, long)
        """
        # Get questions for this round
        question_count = GAME_MODES[mode]["questions"]
        questions = self._select_questions(question_count)
        
        # Ask each question
        for i, q_id in enumerate(questions, 1):
            clear_screen()
            print(f"{GAME_MODES[mode]['name']} - Question {i} of {question_count}")
            
            # Get question data
            question_data = self.data.get_question(q_id)
            
            # Display question and get answer
            user_answer = display_question(question_data, i, question_count)
            
            # Check answer
            correct_answer = self.data.get_correct_answer(q_id)
            is_correct = user_answer.upper() == correct_answer.upper()
            
            # Provide feedback
            if is_correct:
                print("\n✅ Correct!")
                self.current_score += 1
            else:
                print(f"\n❌ Incorrect! The correct answer was {correct_answer}.")
            
            # Add to answered questions
            self.answered_questions.add(str(q_id))
            
            # Pause before next question
            if i < question_count:
                input("\nPress Enter to continue to the next question...")
    
    def _select_questions(self, count: int) -> List[str]:
        """Select random questions for the game.
        
        Args:
            count: Number of questions to select
            
        Returns:
            List of question IDs
        """
        available = self._get_available_questions()
        
        # If not enough questions, reset the answered questions
        if len(available) < count:
            print("\nNot enough questions available. Resetting your progress...")
            self._reset_answered_questions()
            available = self._get_available_questions()
        
        # Select random questions
        selected = random.sample(available, min(count, len(available)))
        
        return selected
    
    def _get_available_questions(self) -> List[str]:
        """Get a list of available question IDs that haven't been answered yet."""
        all_questions = set(str(i+1) for i in range(len(self.data.questions)))
        return list(all_questions - self.answered_questions)
    
    def _handle_game_completion(self, mode: str) -> None:
        """Handle game completion, update leaderboard, and show results.
        
        Args:
            mode: The game mode that was played
        """
        # Save answered questions
        self._update_player_answered_questions()
        
        # Update leaderboard
        self._update_leaderboard(mode)
        
        # Show results
        clear_screen()
        total_questions = GAME_MODES[mode]["questions"]
        display_results(self.current_score, total_questions)
        
        # Reset for next game
        self.current_score = 0
    
    def _update_leaderboard(self, mode: str) -> None:
        """Update the leaderboard with the current game's results.
        
        Args:
            mode: The game mode that was played
        """
        total_questions = GAME_MODES[mode]["questions"]
        
        # Create score entry
        score_entry = {
            'name': self.player_name,
            'score': self.current_score,
            'total': total_questions,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'mode': mode
        }
        
        # Add to mode-specific leaderboard
        self.data.leaderboard[mode].append(score_entry)
        
        # Sort mode-specific leaderboard (best scores first)
        self.data.leaderboard[mode].sort(
            key=lambda x: (x['score']/x['total'], x['score']),
            reverse=True
        )
        
        # Keep only top scores
        self.data.leaderboard[mode] = self.data.leaderboard[mode][:10]
        
        # Add to top scores
        self.data.leaderboard['top_scores'].append(score_entry)
        
        # Sort top scores
        self.data.leaderboard['top_scores'].sort(
            key=lambda x: (x['score']/x['total'], x['score']),
            reverse=True
        )
        
        # Keep only top scores
        self.data.leaderboard['top_scores'] = self.data.leaderboard['top_scores'][:10]
        
        # Save leaderboard
        self.data.save_leaderboard()
    
    def _show_leaderboards(self) -> None:
        """Show the leaderboards menu and display selected leaderboard."""
        while True:
            clear_screen()
            choice = display_menu("Leaderboards", {
                "1": "Top Scores (All Modes)",
                "2": "Short Game Leaderboard",
                "3": "Medium Game Leaderboard",
                "4": "Long Game Leaderboard",
                "5": "Back to Main Menu"
            })
            
            if choice == "1":
                display_leaderboard(self.data.leaderboard)
            elif choice == "2":
                display_leaderboard(self.data.leaderboard, "short")
            elif choice == "3":
                display_leaderboard(self.data.leaderboard, "medium")
            elif choice == "4":
                display_leaderboard(self.data.leaderboard, "long")
            elif choice == "5":
                break
    
    def _get_player_answered_questions(self) -> Set[str]:
        """Get the set of questions the player has already answered."""
        return set(
            self.data.leaderboard
            .get('player_data', {})
            .get(self.player_name, {})
            .get('answered_questions', [])
        )
    
    def _update_player_answered_questions(self) -> None:
        """Update the player's answered questions in the leaderboard."""
        if 'player_data' not in self.data.leaderboard:
            self.data.leaderboard['player_data'] = {}
        
        if self.player_name not in self.data.leaderboard['player_data']:
            self.data.leaderboard['player_data'][self.player_name] = {}
        
        self.data.leaderboard['player_data'][self.player_name]['answered_questions'] = \
            list(self.answered_questions)
        
        self.data.save_leaderboard()
    
    def _reset_answered_questions(self) -> None:
        """Reset the player's answered questions."""
        self.answered_questions = set()
        if 'player_data' in self.data.leaderboard and \
           self.player_name in self.data.leaderboard['player_data']:
            self.data.leaderboard['player_data'][self.player_name]['answered_questions'] = []
            self.data.save_leaderboard()


def main():
    """Entry point for the Bleach Trivia game."""
    game = BleachTriviaGame()
    game.start()


if __name__ == "__main__":
    main()
