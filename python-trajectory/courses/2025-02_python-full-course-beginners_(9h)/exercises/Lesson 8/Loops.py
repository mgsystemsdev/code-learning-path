# loops_explained.py

"""
🔁 Python Loops: while, for, break, continue, else — Full Walkthrough

This script explores all the major loop types in Python.
Each example is grouped and explained to help you:
- Understand when to use each loop
- Avoid common errors like infinite loops
- Practice break/continue control flows
"""

# --- 🌀 1. WHILE LOOP BASICS ---

value = 1

# A `while` loop repeats as long as the condition is True.
# Here, it prints numbers from 1 to 9.
# If you forget `value += 1`, the loop would never end (infinite loop!).
while value < 10:
    print(value)
    value += 1


# --- 🔁 WHILE LOOP TO 10 ---

value = 1  # reset value

# Similar logic, but now includes the number 10 using <=
while value <= 10:
    print('\n', value, '\n')
    value += 1


# --- ❌ 2. WHILE LOOP WITH BREAK ---

value = 1

# `break` exits the loop immediately when triggered.
# This loop will stop as soon as value == 2.
while value <= 10:
    print('\n', value, '\n')
    if value == 2:
        break
    value += 1


# --- ⏩ 3. WHILE LOOP WITH CONTINUE ---

# `continue` skips the rest of the loop **only for that iteration**.
# Here, when value == 5, it will skip the print.
while value <= 10:
    value += 1
    if value == 5:
        continue
    print("\n", str(value), "\n")


# --- ✅ 4. WHILE + ELSE ---

# The `else` clause in a while loop runs **only if the loop wasn't broken.**
# In this case, it will always run once value > 10.
while value <= 10:
    value += 1
    if value == 5:
        continue
    print("\n", str(value), "\n")
else:
    print("value is now equal to " + str(value))


# --- 🔁 5. FOR LOOP OVER A LIST ---

names = ['Dave', 'Sara', 'John']

# `for` loops go through each item in a sequence (like a list).
# Here, we print each name.
for x in names:
    print('\n', x, '\n')


# --- 🔠 6. FOR LOOP OVER A STRING ---

# A string is also a sequence. This will print each character of the word "mississippi".
for x in "mississippi":
    print('\n', x, '\n')


# --- ❌ 7. FOR LOOP WITH BREAK ---

# `break` stops the loop entirely as soon as a condition is met.
# Here, the loop stops when it finds "Sara".
for x in names:
    if x == "Sara":
        break
    print("\n", x, '\n')


# --- ⏭️ 8. FOR LOOP WITH CONTINUE ---

# `continue` skips just the matching case and moves on.
# Here, "Sara" is skipped, but the loop still runs for other names.
for x in names:
    if x == "Sara":
        continue
    print("\n", x, '\n')


# --- 🔢 9. FOR LOOP WITH RANGE ---

# `range()` lets you generate sequences of numbers.

# Basic range: 0 to 3
for x in range(4):
    print(x)

# Custom start and end: 2 to 3
for x in range(2, 4):
    print(x)

# Range with step: from 5 to 95, in steps of 5
for x in range(5, 100, 5):
    print(x)
else:
    print("glad that's over")  # This runs after the loop finishes normally


# --- 🔁 10. NESTED FOR LOOPS ---

actions = ["codes", "eat", "sleeps"]

# Nested loops: the outer loop runs once per name, the inner once per action.
# This results in each name doing each action once.
for name in names:
    for action in actions:
        print(name + "       " + action + ".")

# You can reverse the order too:
for action in actions:
    for name in names:
        print(name + "       " + action + ".")

"""
✅ What You Learned:
- `while` loops: run based on condition
- `for` loops: run through a sequence (like list or string)
- `break`: exit a loop early
- `continue`: skip one round of the loop
- `else`: runs if loop ends normally
- `range()`: generate numeric sequences for looping
- Nested loops: loops inside loops for multi-level logic

Use `while` for flexible or unknown-length loops.
Use `for` for known items or ranges.
"""

print("\n✅ Finished Loop Learning Block.\n")
