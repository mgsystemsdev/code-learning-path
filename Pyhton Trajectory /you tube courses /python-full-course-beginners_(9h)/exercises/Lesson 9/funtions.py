# functions_explained.py

"""
🧠 Python Function Basics - Learning File

This script teaches core concepts of how functions work in Python.
Each section includes comments to explain:
- How functions are defined
- How they accept parameters
- How to work with *args and **kwargs
"""

# --- 1️⃣ BASIC FUNCTION WITHOUT PARAMETERS ---

def hello():
    # This function doesn't need any input. It just prints a message.
    print('\n', "Hello World !", '\n')

# Calling the function
hello()

# 🔍 What You Learned:
# This is the simplest form of a function: no input, no return.
# It introduces the syntax: `def name():`, indentation, and calling a function.
# Even though it returns nothing, it shows how we can encapsulate a task and reuse it.


# --- 2️⃣ FUNCTION WITH PARAMETERS AND TYPE CHECKING ---

def sum(num1=0, num2=0):
    # This condition ensures both values are integers.
    if (type(num1) is not int or type(num2) is not int):
        return 0  # Return zero if invalid types
    return num1 + num2  # Return their sum

# Call with valid integers
total = sum(7, 9)
print('\n', total, '\n')

# 🔍 What You Learned:
# - You can give parameters default values (`num1=0`)
# - You can guard your logic with `type()` checks
# - You return a value using `return`
# - You store the result in a variable and print it
# This builds the foundation for defensive programming and validation.


# --- 3️⃣ VARIABLE-LENGTH POSITIONAL ARGUMENTS (*args) ---

def multiple_items(*args):
    # Just printing all arguments together as a tuple
    print('\n')
    print(args)              # The whole collection
    print('\n')
    print(type(args))        # Confirm it's a tuple
    print('\n')

# Call with multiple string arguments
multiple_items("dave", "john", 'sara')

# 🔍 What You Learned:
# - `*args` collects any number of positional arguments into a tuple
# - You can pass in 0, 1, or many values
# - Python groups them into one structure (`args`)
# This pattern is useful when writing flexible functions that can accept unlimited inputs.


# --- 4️⃣ LOOPING THROUGH *args ---

def multiple_items(*args):
    print("\n")  
    for item in args:
        print(item)          # Each argument on a new line
        print(type(args))    # Still a tuple every time
    print("\n")  

# Call again with multiple values
multiple_items("dave", "john", "sara")

# 🔍 What You Learned:
# - You can iterate through `args` just like any other iterable
# - Each loop gives you one item from the original inputs
# - This pattern is useful when you want to *do something* with each item
# This helps bridge the concept of unpacking and iteration.


# --- 5️⃣ VARIABLE-LENGTH KEYWORD ARGUMENTS (**kwargs) ---

def mult_name_items(**kwargs):
    print("\n")  
    print(kwargs)           # Shows the dictionary of named arguments
    print(type(kwargs))     # Confirms it's a dictionary
    print("\n")  

# Call with named parameters
mult_name_items(first="dave", last="john")

# 🔍 What You Learned:
# - `**kwargs` captures multiple keyword (named) arguments
# - It stores them as a dictionary where keys are names and values are values
# - Useful for flexible configuration, API input, user settings
# This is a powerful tool when writing functions that need optional, named, or structured input.
