

# 📝 Exercise A (Setup)

# Goal:
# Write a program that stores your name in a variable and prints a personalized greeting.

# Input:
# No user input — just store your name in code.

# Output:
# A message like:

name = "María"
print(f"Hello, {name}! Welcome to Python.")




# 📝 Exercise B (Setup)

# **Goal:**
# Write a program that stores your **favorite number** in a variable, then prints:

# ```
# My favorite number is 7.
# ```

# ---

# ### ⚡ Requirements:

# 1. Create a variable called `favorite_number`.
# 2. Store an **integer** in it (not a string).
# 3. Print the sentence using an f-string.
# 4. Add a comment explaining what the program does.

# ---

# ### ❌ Common Trap (to watch out for):

# If you try to directly join a number and a string without converting or using an f-string, Python will throw a **TypeError**. Example:

# ```python
# number = 7
# print("My favorite number is " + number)  # ERROR
# ```

# So we’ll avoid that by using **f-strings**.

# this program  shows my favorite number  # comment
number = 7                                # variable
print(f"My favorite number is {number}.") # output
# using f-string to avoid type error 




# # 📝 Exercise C (Setup)

# **Goal:**
# Practice **re-assigning variables** and using **string methods**.

# Your program should:

# 1. Create a variable called `city` and store the name of a city (e.g., `"paris"`).
# 2. Print the name with the **first letter capitalized**.
# 3. Re-assign the variable with a different city name (e.g., `"tokyo"`).
# 4. Print the new city name in **all uppercase letters**.
# 5. Add a comment describing what the program does.

# ---

# ### 💡 Example Output:

# ```
# Paris
# TOKYO
# ```

# this program shows how to reassign variables and use string methods  # comment
city = "paris"               # variable assignment
print(city.capitalize())  # output first letter capitalized
city = "tokyo"
print(city.upper())  # output all uppercase letters



# 📝 Exercise D (Setup)

# **Goal:**
# Combine **variables, numbers, and comments** to do a simple calculation.

# Your program should:

# 1. Create a variable called `age` and store your age (integer).
# 2. Create another variable called `future_age` that adds **10 years** to `age`.
# 3. Print a sentence using an f-string, like:

#    ```
#    In 10 years, I will be 35 years old.
#    ```
# 4. Add a comment explaining what the program does.

# ---

# ### ⚡ Example:

# If `age = 25`, the output should be:

# ```
# In 10 years, I will be 35 years old.
# ```

# This program add my age i will be in 10 year from now 
age = 35  # variable assignment
future_age = age + 10  # adding 10 years to age

print(f"In 10 years, i will be {future_age} years old.")  # output using f-string




# This program tell my actual  age my age next year 
name = "miguel"    # variable for name 
age = 35           # variable for age
future_age = age + 1 # variable for age next year

print(f"Hello,{name.title()}! you are {age} years old.") # output using f-string for age now
print(f"Next year you will be {future_age} years old.") # output using f-string for age next year





# 📝 Exercise F (Setup)

# **Goal:**
# Work with strings that contain **extra spaces** and clean them up using `.strip()`, `.rstrip()`, and `.lstrip()`.

# ---

# ### ⚡ Requirements:

# 1. Create a variable called `username` with leading and trailing spaces, e.g. `"   miguel   "`.
# 2. Print the raw value to show the spaces.
# 3. Print it again with:

#    * `.lstrip()` → removes spaces on the **left**
#    * `.rstrip()` → removes spaces on the **right**
#    * `.strip()`  → removes spaces on **both sides**
# 4. Add a comment describing what the program does.

# ---

# ### 💡 Example Output:

# ```
#    miguel   
# miguel   
#    miguel
# miguel
# ```

# This program shows how to use strip methods to remove leading and trailing spaces from a string  # comment
user_name = "   miguel   "  # variable with leading and trailing spaces

print(user_name)  # output raw value
print(user_name.lstrip())  # output with left spaces removed
print(user_name.rstrip())  # output with right spaces removed
print(user_name.strip())  # output with both sides spaces removed




# # 📝 Exercise G (Setup)

# **Goal:**
# Work with **underscores in numeric literals** to improve readability.

# ---

# ### ⚡ Requirements:

# 1. Create a variable called `universe_age` and store a large number with underscores, e.g. `14_000_000_000`.
# 2. Print the variable to show that Python ignores the underscores.
# 3. Do a simple calculation with it (e.g., divide by 2) to prove it behaves like a normal number.
# 4. Add a comment describing what the program does.

# ---

# ### 💡 Example Output:

# ```
# 14000000000
# 7000000000.0
# ```


# program to demonstrate the use of underscores in numeric literals
universe_age = 14_000_000_000 # variable with underscores for readability
print(universe_age) # output to show underscores are ignored 
print(universe_age / 2) # simple calculation to prove it behaves like a normal number



# this program shows how to assign multiple variables on one line and reassing value to them
x, y, z = 5, 10, 15 # variables on line 
a, b, c = 20, 30, 40 # variables on line reassing value

print(f"x = {x}, y = {y}, z = {z}") # output firts value
print(f"a = {a}, b = {b}, c = {c}")  # output reassing value







# # 📝 Exercise I (Setup)

# **Goal:**
# Learn how to represent **constants** in Python using **ALL\_CAPS** naming.
# (Remember: Python doesn’t *enforce* constants, but programmers use caps to show “this should not change.”)

# ---

# ### ⚡ Requirements:

# 1. Create a constant variable `MAX_USERS` with a value, e.g. `100`.
# 2. Print a sentence using it.
# 3. Try reassigning `MAX_USERS` to a new value and print again — to show Python *allows* it, but style says you shouldn’t.
# 4. Add a comment explaining what the program does.

# ---

# ### 💡 Example Output:

# ```
# The maximum number of users allowed is 100.
# The maximum number of users allowed is 200.  # Python lets you, but style says no!
# ```

# This program demonstrates the use of constant variables in Python 
MAX_USERS = 100  # constant variable
print(f"The maximum number of users allowed is {MAX_USERS}.")  # output using constant
MAX_USERS = 200  # reassigning constant variable (not recommended)
print(f"The maximum number of users allowed is {MAX_USERS}.")  # output after reass



# # 📝 Exercise J (Setup)

# **Goal:**
# Understand what happens when you try to mix **strings and integers** incorrectly, and how to fix it.

# ---

# ### ⚡ Requirements:

# 1. Create a variable `age` and store your age as an integer.
# 2. Try printing this sentence **without conversion**:

#    ```
#    I am 35 years old.
#    ```

#    using string concatenation (`+`).
#    👉 Expect a **TypeError**.
# 3. Fix it in two ways:

#    * Using `str(age)`
#    * Using an **f-string**
# 4. Add a comment explaining what the program does.

# ---

# ### 💡 Example Output:

# ```
# TypeError: can only concatenate str (not "int") to str
# I am 35 years old.      # fixed with str()
# I am 35 years old.      # fixed with f-string
# ```

# this code demonstrates how to fix TypeError when mixing strings and integers
age = 35  # variable assignment
print("I am " + str(age) + " years old.")  # fixed with str()
print(f"I am {age} years old.")  # fixed with f-string
