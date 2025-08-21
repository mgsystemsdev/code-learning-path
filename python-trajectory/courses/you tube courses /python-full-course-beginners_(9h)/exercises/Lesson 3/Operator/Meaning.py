# === Python Type: Ternary Operator (One-line If-Else) ===
# This shows how to use the ternary operator for simple decision-making.

# Example 1 — basic usage
meaning = 45  # Assigning a number to the variable 'meaning'
print("Right On!") if meaning > 10 else print("Not Today")  
# If 'meaning' is greater than 10, print "Right On!", otherwise print "Not Today"

# Example 2 — test for equality
score = 100
print("Perfect Score!") if score == 100 else print("Keep Trying!")
# If score equals 100, print a special message

# Example 3 — check if number is even
number = 4
print("Even Number") if number % 2 == 0 else print("Odd Number")
# Using the modulus operator to check if number is even

# Example 4 — checking string content
status = "online"
print("User is active") if status == "online" else print("User is away")
# Compares a string to decide what message to show

# Example 5 — checking a list’s length
tasks = ["code", "review", "test"]
print("Tasks to do!") if len(tasks) > 0 else print("No tasks left")
# Checks if the list has any items in it

