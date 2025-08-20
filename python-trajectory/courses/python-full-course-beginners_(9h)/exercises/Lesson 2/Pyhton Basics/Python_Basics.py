# === Python Type: Updated Message Display with Box Formatting and Color ===
# New message shows motivation and encouragement.

line001 = "******************************************"  # Decorative border
line002 = "*                                        *"  # Spacer line inside the box
line003 = "*   Keep going, you're doing amazing!    *"  # Positive message line
line004 = "*  Every step forward is progress.       *"  # Motivational message
line005 = "*   Trust the journey. You've got this!  *"  # Encouraging closer
line006 = "*   💪🔥 Code. Learn. Grow. Repeat. 🔥💪   *"  # Fun repeated message with emojis

print("")  # Spacer before the box

print(line001)  # Top border
print(line002)  # Empty line
print(line003)  # Line 1 of the message
print(line004)  # Line 2
print(line005)  # Line 3
print(line006)  # Line 4 (highlight line)

# Repeating the line multiple times to reinforce motivation
print(line006)
print(line006)
print(line006)
print(line006)
print(line006)
print(line006)
print(line006)
print(line006)
print(line006)
print(line006)
print(line006)
print(line006)

print(line002)  # Bottom spacing line
print(line001)  # Bottom border

# === Repeating the same with purple color for emphasis ===

line001 = "******************************************"
line002 = "*                                        *"
line003 = "*   Keep going, you're doing amazing!    *"
line004 = "*  Every step forward is progress.       *"
line005 = "*   Trust the journey. You've got this!  *"
line006 = "*   💪🔥 Code. Learn. Grow. Repeat. 🔥💪   *"

print("")  # Blank line

print(line001)
print(line002)
print(line003)
print(line004)
print(line005)

# Highlight lines in purple using ANSI escape codes
print("\033[35m" + line006 + "\033[0m")
print("\033[35m" + line006 + "\033[0m")
print("\033[35m" + line006 + "\033[0m")
print("\033[35m" + line006 + "\033[0m")
print("\033[35m" + line006 + "\033[0m")
print("\033[35m" + line006 + "\033[0m")

print(line002)
print(line001)
