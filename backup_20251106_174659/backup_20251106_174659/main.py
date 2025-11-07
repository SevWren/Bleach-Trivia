#!/usr/bin/env python3
"""
Bleach Trivia Game

A command-line trivia game based on the Bleach anime/manga series.
Players can test their knowledge with different game modes and track their scores.
"""

def main():
    """Main entry point for the Bleach Trivia game."""
    try:
        from game.core import BleachTriviaGame
        
        print("Starting Bleach Trivia...")
        game = BleachTriviaGame()
        game.start()
        
    except ImportError as e:
        print(f"Error: Failed to import required modules: {e}")
        print("Please make sure you have all the required dependencies installed.")
        print("You can install them by running: pip install -r requirements.txt")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise


if __name__ == "__main__":
    main()
