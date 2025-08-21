# === Rock Paper Scissors Game with Scoreboard ===
# This program lets you play against the computer and keeps track of wins, losses, and ties.

# --- Step 1: Import required modules ---
import sys      # For exiting the program if needed
import random   # To let the computer make random choices
import time     # To pause between outputs for dramatic effect

# --- Step 2: Define choices as a dictionary ---
choices = {1: "rock", 2: "paper", 3: "scissors"}  
# Maps each number to a string so we can refer to moves by number in logic, and by name in display

# --- Step 3: Define a function to play a single round ---
def play_round():
    print("\nEnter...")
    print("1 for Rock")
    print("2 for Paper")
    print("3 for Scissors")

    # Get user input and ensure it's a valid number
    try:
        player = int(input("\nYour choice: "))
    except ValueError:
        print("\n⚠️ Please enter a number (1, 2, or 3)!")
        return None

    # Make sure the input is within the valid range
    if player < 1 or player > 3:
        print("\n⚠️ Invalid choice. Pick 1, 2, or 3!")
        return None

    # Randomly generate computer's move
    computer = random.choice([1, 2, 3])

    # Show both choices
    print("\nYou chose " + choices[player] + "...")
    time.sleep(1)
    print("Python chose " + choices[computer] + "...")
    time.sleep(1)

    # Determine the outcome and return who won
    if (player == 1 and computer == 3) or \
       (player == 2 and computer == 1) or \
       (player == 3 and computer == 2):
        print("\n🎉 You WIN this round!")
        return "player"
    elif player == computer:
        print("\n🤝 It's a TIE!")
        return "tie"
    else:
        print("\n💻 Python WINS this round!")
        return "python"

# --- Step 4: Main function to control the game loop and scoreboard ---
def main():
    print("\n🪨📄✂️ Welcome to Rock Paper Scissors with a Scoreboard!")

    # Initialize scores
    player_score = 0
    python_score = 0
    ties = 0

    # Loop to keep playing rounds until user quits
    while True:
        result = play_round()

        # Update scores based on result
        if result == "player":
            player_score += 1
        elif result == "python":
            python_score += 1
        elif result == "tie":
            ties += 1

        # Print updated scoreboard
        print(f"\n--- Scoreboard ---")
        print(f"You: {player_score}")
        print(f"Python: {python_score}")
        print(f"Ties: {ties}")

        # Ask if the player wants to continue
        again = input("\nPlay another round? (y/n): ").lower()
        if again != 'y':
            print("\nThanks for playing! Final Score:")
            print(f"You: {player_score} | Python: {python_score} | Ties: {ties}")
            print("Goodbye 👋")
            break

# --- Step 5: Only run the game if this file is executed directly ---
if __name__ == "__main__":
    main()

