import sys
import io
import sys
from unittest.mock import patch
from bleach_trivia import BleachTriviaGame

# Set up console output to handle Unicode
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def test_game():
    # Simulate user inputs for a complete game
    test_inputs = [
        'Test Player',  # Player name
        '1',           # Choose short game
        'A', 'B', 'C', 'D', 'A',  # Answers to 5 questions
        'n'            # Don't play again
    ]
    
    with patch('builtins.input', side_effect=test_inputs):
        game = BleachTriviaGame()
        game.play_game()
    
    print("\nTest completed successfully!")

if __name__ == "__main__":
    print("Starting automated test...")
    test_game()
