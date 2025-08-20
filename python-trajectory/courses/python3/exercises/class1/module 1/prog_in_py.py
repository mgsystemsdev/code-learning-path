# ============================================================
#  File:        module1.py
#  Author:      Miguel Gonzalez Almonte
#  Created:     2025-06-01
#  Description: Introduction to values, variables, and basic data types in Python.
# ------------------------------------------------------------
#  Course:      Python 3 Programming Specialization (Coursera)
#  Module:      Module 1 of Class 1
#  Purpose:     Establish foundational knowledge of how Python handles data —
#               including assignment, type categorization, and value manipulation.
# ------------------------------------------------------------
#  Notes:
#  - Value and Data
#  - Values and Data Types
#  - Integers, Floats, Strings, Booleans
#  - Type Checking with `type()`
#  - Variable Assignment and Naming Rules
#  - Type Conversion: `int()`, `float()`, `str()`
#  - Basic print() usage
#  - Avoiding Syntax Errors
#  - Introduction to Expressions
# ============================================================

# ============================================================
#      - Values and Data Types
# ============================================================

print("Hello, World!")

#--------

# What appears in the output window when the following statement executes?

print("Hello World!")

# C. Hello World!

# ============================================================
#      Operators and Operands¶
# ============================================================

print(20 + 32)
print(5 ** 2) 
print((5 + 9) * (15 - 7))
print(7 + 5)

#---------

print(9 / 5)
print(5 / 9)
print(9 // 5)

#---------

print(7.0 / 3.0)
print(7.0 // 3.0)

#---------

print(7 // 3)    # This is the integer division operator
print(7 % 3)     # This is the remainder or modulus operator

# ============================================================
#      Order of Operations¶
# ============================================================

print(2 ** 3 ** 2)     # the right-most ** operator gets done first!
print((2 ** 3) ** 2)   # use parentheses to force the order you want!

#---------

# What is the value of the following expression:

16 - 2 * 5 // 3 + 1

# A. 14

#---------

16 - 2 * 5 // 3 + 1

# ============================================================
#      Function Calls
# ============================================================

def square(x):
    return x * x

def sub(x, y):
    return x - y
print(square(4))

#----------

print(square(3))
square(5)
print(sub(6, 4))
print(sub(5, 9))

#----------

print(square(3) + 2)
print(sub(square(3), square(1+1)))

#----------

print(square)
print(square(3))

# ============================================================
#   Data Types¶
# ============================================================

print(type("Hello, World!"))
print(type(17))
print("Hello, World")
print(type(3.2))

#----------

print(type("17"))
print(type("3.2"))

#----------

print(type('This is a string.'))
print(type("And so is this."))
print(type("""and this."""))
print(type('''and even this...'''))

#----------

print('''"Oh no", she exclaimed, "Ben's bike is broken!"''')

#----------

print("""This message will span
several lines
of the text.""")

#----------

print('This is a string.')
print("""And so is this.""")


#----------

print(42500)
print(42,500)


#----------

print(42, 17, 56, 34, 11, 4.35, 32)
print(3.4, "hello", 45)

#----------

# How can you determine the type of a variable?

# B. Use the type function.

#----------

#    What is the data type of ‘this is what kind of data’?

# D. String

# ============================================================
#       Type conversion functions¶
# ============================================================

print(3.14, int(3.14))
# Output: 3.14 3       → int() removes decimal (does NOT round)

print(3.9999, int(3.9999))
# Output: 3.9999 3     → Still just drops the decimal

print(3.0, int(3.0))
# Output: 3.0 3        → Clean conversion from float

print(-3.999, int(-3.999))
# Output: -3.999 -3    → Truncates toward zero

print("2345", int("2345"))
# Output: 2345 2345    → Valid string-to-int

print(17, int(17))
# Output: 17 17        → Already an integer

print(int("23bottles"))
# ❌ ValueError: invalid literal for int() with base 10: '23bottles'

#----------

print(float("123.45"))
print(type(float("123.45")))

#----------

print(str(17))
print(str(123.45))
print(type(str(123.45)))

#----------

# What value is printed when the following statement executes?

print(int(53.785))

# B. 53

# ============================================================
#  Reassingment
# ============================================================

bruce = 5
print(bruce)
bruce = 7
print(bruce)

#----------

a = 5
b = a    # after executing this line, a and b are now equal
print(a,b)
a = 3    # after executing this line, a and b are no longer equal
print(a,b)

#----------

# After the following statements, what are the values of x and y?

x = 15
y = x
x = 22

# D. x is 22 and y is 15

# ============================================================
# Statements and Expressions
# ============================================================

print(1 + 1 + (2 * 3))
print(len("hello"))

#----------

y = 3.14
x = len("hello")
print(x)
print(y)

#----------

print(2 * len("hello") + len("goodbye"))

#----------

def square(x):
   return x * x

def sub(x, y):
   return x - y

#----------

x = 2
y = 1
print(square(y + 3))
print(square(y + square(x)))
print(sub(square(y), square(x)))

#----------

x = 5
y = 7
#add(square(y), square(x))

# ============================================================
#    Updating Variables¶
# ============================================================

x = 6        # initialize x
print(x)
x = x + 1    # update x
print(x)

#----------

x = 6        # initialize x
print(x)
x += 3       # increment x by 3; same as x = x + 3
print(x)
x -= 1       # decrement x by 1
print(x)

#----------

s = 1
print(s)
s = s + 2
print(s)
s = s + 3
print(s)
s = s + 4
print(s)
s = s + 5
print(s)
s = s + 6
print(s)
s = s + 7
print(s)
s = s + 8
print(s)
s = s + 9
print(s)
s = s + 10
print(s)

#----------

# What is printed when the following statements execute?

x = 12
x = x - 1
print(x)

11

#----------

# What is printed when the following statements execute?

x = 12
x = x - 3
x = x + 5
x = x + 1
print(x)

15

#----------

# Which of the following statements are equivalent?

#   x = x + y
#   x += y

# ============================================================
#    Input
# ============================================================

n = input("Please enter your name: ")
print("Hello", n)

#----------

str_seconds = input("Please enter the number of seconds you wish to convert")
total_secs = int(str_seconds)

hours = total_secs // 3600
secs_still_remaining = total_secs % 3600
minutes =  secs_still_remaining // 60
secs_finally_remaining = secs_still_remaining  % 60

print("Hrs=", hours, "mins=", minutes, "secs=", secs_finally_remaining)


#----------

# What is printed when the following statements execute?

n = input("Please enter your age: ")
# user types in 18
print(type(n))
# <class 'str'>

# ============================================================
#    Assigmment 
# ============================================================

#There is a function we are providing in for you in this problem called square. It takes one integer and returns the square of that integer value. Write code to assign
#a variable called xyz the value 5*5 (five squared). Use the square function, rather than just multiplying with *.

xyz = square(5)


#----------

# Write code to assign the number of characters in the string rv to a variable num_chars.

rv = """Once upon a midnight dreary, while I pondered, weak and weary,
    Over many a quaint and curious volume of forgotten lore,
    While I nodded, nearly napping, suddenly there came a tapping,
    As of some one gently rapping, rapping at my chamber door.
    'Tis some visitor, I muttered, tapping at my chamber door;
    Only this and nothing more."""

# Write your code here!

num_chars = len(rv)

#----------

def square(num):
    return num**2

#----------
#----------

### 🧠 Python Keywords (as of Python 3.5)

# Python keywords are **reserved words** that define the core **syntax and structure** of the language.  
# They **cannot be used as variable names**.  
# Here is a table of all keywords current as of **Python 3.5**, along with what each one does:

# | **Keyword**   | **What It Does**                                                                  |
# |---------------|-----------------------------------------------------------------------------------|
# | `and`         | Logical AND operator                                                              |
# | `as`          | Used to create aliases (e.g., `import x as y`)                                    |
# | `assert`      | Debugging aid that tests a condition                                              |
# | `async`       | Declares asynchronous functions (coroutines)                                      |
# | `await`       | Awaits the result of an async operation                                           |
# | `break`       | Exits the current loop prematurely                                                |
# | `class`       | Declares a new class                                                              |
# | `continue`    | Skips the rest of the current loop iteration                                      |
# | `def`         | Declares a new function                                                           |
# | `del`         | Deletes an object or variable                                                     |
# | `elif`        | Else-if condition in control flow                                                 |
# | `else`        | Final fallback block in conditionals or loops                                     |
# | `except`      | Defines a block to handle exceptions                                              |
# | `finally`     | Block that always runs after `try`/`except`, whether or not an error occurred     |
# | `for`         | Begins a `for` loop                                                               |
# | `from`        | Used to import specific parts of a module                                         |
# | `global`      | Declares a global variable from within a function                                 |
# | `if`          | Starts a conditional statement                                                    |
# | `import`      | Imports a module                                                                  |
# | `in`          | Tests for membership (e.g., `x in list`)                                          |
# | `is`          | Tests for identity (e.g., `x is y`)                                               |
# | `lambda`      | Declares an anonymous function (lambda function)                                  |
# | `nonlocal`    | Refers to a variable in an outer (non-global) scope                               |
# | `not`         | Logical NOT operator                                                              |
# | `or`          | Logical OR operator                                                               |
# | `pass`        | Placeholder that does nothing (used to fill empty blocks)                         |
# | `raise`       | Triggers an exception                                                             |
# | `return`      | Exits a function and optionally returns a value                                   |
# | `try`         | Starts a block of code to catch exceptions                                        |
# | `while`       | Starts a `while` loop                                                             |
# | `with`        | Wraps execution in a context manager (e.g., file handling)                        |
# | `yield`       | Pauses a generator function and yields a value                                    |
# | `True`        | Boolean true value                                                                |
# | `False`       | Boolean false value                                                               |
# | `None`        | Represents the absence of a value                                                 |











