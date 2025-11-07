#!/usr/bin/env python3
"""
Bleach Trivia Game

A command-line trivia game based on the Bleach anime/manga series.
Players can test their knowledge with different game modes and track their scores.
"""

from bleach_trivia import BleachTriviaGame

def main():
    """Main entry point for the Bleach Trivia game."""
    try:
        print("Starting Bleach Trivia...")
        game = BleachTriviaGame()
        game.play_game()
    except KeyboardInterrupt:
        print("\nGame ended by user.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        raise
    finally:
        # Ensure leaderboard is saved before exiting
        if 'game' in locals():
            game.save_leaderboard()

if __name__ == "__main__":
    main()
