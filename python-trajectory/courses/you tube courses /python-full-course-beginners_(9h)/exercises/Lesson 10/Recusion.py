# recursion_learning_block.py

"""
🧠 How to Create, Understand, and Manipulate Recursion in Python
This file is a learning guide + executable walkthrough for beginners.
It teaches how recursion works, how to write it, and how to manipulate it.
"""

# --- 🔁 What Is Recursion? ---
# Recursion is when a function calls itself to solve a smaller piece of the same problem.
# Think of it like zooming in until the problem is simple, then solving your way back out.


# --- 🔨 How to Build a Recursive Function (The Recipe) ---

# ✅ 1. Define the Problem
#    - Ask: Can this be broken down into a smaller version of the same task?
# ✅ 2. Set the Base Case (STOP condition)
#    - Without this, recursion never ends and crashes.
# ✅ 3. Write the Recursive Case (GO deeper)
#    - This is the part where the function calls itself.
# ✅ 4. Return the Result
#    - Let the result return back up once the base case is reached.


# --- 🧪 Example Template ---

"""
def my_function(input):
    if some_condition_is_true:      # ✅ Base case
        return base_result

    smaller_input = input - something  # Make input smaller
    return my_function(smaller_input)  # 🔁 Recursive call
"""

# --- 🎓 Build-and-Break Example: Count Up to 5 ---

def count_up(num):
    if num >= 5:                    # ✅ Base case: stop at 5
        print("Reached 5!")
        return
    print(num)                      # 👀 See current value
    count_up(num + 1)              # 🔁 Recursive call

# Run the count_up function
print("\n🧪 Running count_up(1)...\n")
count_up(1)


# --- 🔄 How to Manipulate Recursive Behavior ---

# ✅ Direction change: count down instead of up

def count_down(num):
    if num == 0:
        print("Blast off!")
        return
    print(num)
    count_down(num - 1)

print("\n🧪 Running count_down(5)...\n")
count_down(5)


# ✅ Returning values instead of printing

def sum_up_to(n):
    if n == 0:
        return 0
    return n + sum_up_to(n - 1)

print("\n🧪 Running sum_up_to(5):\n")
print("Total:", sum_up_to(5))  # 5 + 4 + 3 + 2 + 1 = 15


# ✅ Building a list using recursive return values

def list_numbers(n):
    if n == 0:
        return []
    return list_numbers(n - 1) + [n]

print("\n🧪 Running list_numbers(5):\n")
print("List:", list_numbers(5))  # [1, 2, 3, 4, 5]


# --- 🧠 Think of Recursion Like a Stack ---
# Every time a function calls itself:
# - It pauses and waits for the result of the next call
# - Once the base case is reached, results return in reverse order
# - Like stacking plates, and removing them one at a time


# --- 💪 Optional Practice Challenge ---

def count_to_five(num=1):
    if num > 5:
        print("Done!")
        return
    print(num)
    count_to_five(num + 1)

print("\n🧪 Practice: count_to_five()\n")
count_to_five()


# --- ✅ Summary of What You Learned ---

"""
🔁 RECURSION KEY CONCEPTS:

- Base case     → Stops the loop
- Recursive call→ Continues the loop
- Stack flow    → Each call waits for the next to finish
- Use cases     → Counting, math (factorials, Fibonacci), search, trees

"""

# Done!
print("\n✅ Finished Recursion Learning Block.\n")
