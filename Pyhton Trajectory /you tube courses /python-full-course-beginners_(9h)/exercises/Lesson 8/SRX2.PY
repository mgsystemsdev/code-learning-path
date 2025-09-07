# rock_paper_scissors_safe.py

"""
🎮 Rock-Paper-Scissors Game (Safe Version with Explanations)

This beginner-friendly script allows a player to play Rock-Paper-Scissors
against the computer using Enums and while loops. It includes input validation
to prevent crashes and comments to explain every step.
"""

# --- 📦 IMPORTS ---
# These modules give us extra functionality for system exit, randomness, and better game structure
import sys          # Lets us exit the program cleanly with a message
import random       # Allows the computer to make a random choice
from enum import Enum  # Helps us name the game choices using enums for readability

# --- 🎲 ENUM CLASS FOR GAME CHOICES ---
# Instead of using plain numbers, we assign names to them for clarity.
# This improves both display and comparison logic later.
class RPS(Enum):
    rock = 1
    paper = 2
    scissors = 3

# --- 🔁 GAME LOOP CONTROL VARIABLE ---
# This boolean controls whether the game repeats or not
playagain = True

# --- 🔄 MAIN GAME LOOP ---
# This loop keeps running until the player chooses to quit
while playagain:
    
    # --- 🎮 USER INPUT ---
    # Prompt the user to pick a move by entering a number
    playerchoices = input(
        "\nEnter...\n\n1 for Rock,\n2 for Paper,\n3 for Scissors:\n\n"
    )

    # --- ✅ INPUT VALIDATION ---
    # Make sure the user entered digits only (e.g., no letters or symbols)
    if not playerchoices.isdigit():
        sys.exit("⚠️ Invalid input. You must enter a number (1, 2, or 3).")

    # Convert the valid input into an integer
    player = int(playerchoices)

    # Ensure the number is one of the allowed choices
    if player < 1 or player > 3:
        sys.exit("⚠️ Invalid number. You must enter 1, 2, or 3.")

    # --- 🤖 COMPUTER CHOICE ---
    # The computer randomly selects one of the valid moves
    computer = random.choice([1, 2, 3])

    # --- 🧾 DISPLAY CHOICES ---
    # Show what both the player and the computer picked using enum names
    print("\nYou chose: " + str(RPS(player)).replace('RPS.', '') + "\n")
    print("Python chose: " + str(RPS(computer)).replace('RPS.', '') + "\n")

    # --- ⚔️ GAME LOGIC ---
    # Determine the outcome based on classic Rock-Paper-Scissors rules
    if (player == 1 and computer == 3) or \
       (player == 2 and computer == 1) or \
       (player == 3 and computer == 2):
        print("🎉 You WIN!")
    elif player == computer:
        print("🤝 It's a TIE!")
    else:
        print("🐍 Python WINS!")

    # --- 🔁 ASK TO PLAY AGAIN ---
    # Prompt the user to see if they want to play another round
    again = input("\nPlay again? (Y to continue, any other key to quit): ").lower()
    
    # If they type 'y', the loop restarts; otherwise it ends
    if again == "y":
        continue
    else:
        print("\n🎉 Thanks for playing! 🎉")
        playagain = False

# --- 🛑 CLEAN EXIT ---
# Final goodbye message after the loop ends
sys.exit("Goodbye 👋")
