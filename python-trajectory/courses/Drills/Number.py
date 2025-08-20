


#          Drills 1–5 — Basic Assignment

# Focus: Assign and print numeric values.

# Why this matters:
# Every program starts with data. This block teaches you how to store numbers in variables — 
# like putting values in labeled boxes. Until this is second 
# nature, nothing else can build on top of it.

# You’ll learn:
# The = operator is not math — it means store this value here.
#Numbers can be positive, negative, whole (int), or decimal (float).
#print() is your first tool for visibility — it’s how you “see” your code’s behavior.




# Drill 1
# Assign the number 10 to a variable and print it
x = 10
print(x)

# Drill 2
# Assign the number 42 to a variable called num and print it
num = 42
print(num)

# Drill 3
# Assign a negative number to a variable and print it
score = -5
print(score)

# Drill 4
# Assign a float number to a variable and print it
pi = 3.14
print(pi)

# Drill 5
# Assign zero to a variable and print it
zero = 0
print(zero)




#          Drills 6–10 — Reassignment

# Focus: Overwrite values in number variables.

# Why this matters:
# Variables are not locked — you can update them. This simulates changing values in real 
# life: a score increasing, a price adjusting, a timer updating.

# You’ll learn:
# Reassignment is just using = again — it replaces the old value.
# Variables act like containers that always show their latest value.
# Understanding reassignment sets you up for loops, logic, and math flows later.




# Drill 6
# Assign 5 to a variable, then reassign it to 10 and print
a = 5
a = 10
print(a)

# Drill 7
# Create a variable with a number, reassign a different number, print both steps
b = 100
print(b)
b = 200
print(b)

# Drill 8
# Assign and change a float value
rate = 2.5
rate = 3.75
print(rate)

# Drill 9
# Reassign a negative number to a positive value
change = -8
change = 8
print(change)

# Drill 10
# Reassign a variable from 0 to any other number
counter = 0
counter = 7
print(counter)




#          Drills 11–15 — Integer Operations

# Focus: Do math with whole numbers.

# Why this matters:
# These are the building blocks of any logic that counts, adds, or balances values — 
# from inventory systems to simple games.

# You’ll learn:
# How to use +, -, * on integers.
# That order matters: math follows a set priority (PEMDAS).
# Arithmetic is about flow: data moves through operations into results.




# Drill 11
# Add two integers and print the result
sum_result = 4 + 5
print(sum_result)

# Drill 12
# Subtract one integer from another
difference = 10 - 3
print(difference)

# Drill 13
# Multiply two integers
product = 6 * 7
print(product)

# Drill 14
# Combine addition and subtraction
result = 8 + 2 - 5
print(result)

# Drill 15
# Multiply first, then subtract
outcome = 3 * 4 - 2
print(outcome)




#          Drills 16–20 — Float Operations

# Focus: Work with decimal numbers.

# Why this matters:
# Many systems require precision — money, measurements, percentages. Floats allow for 
# finer granularity than integers.

# You’ll learn:
# Floats behave like ints — but with decimals.
# Float math introduces real-world precision (but also rounding errors later).
# Mixing float and int? Python upgrades the result to float automatically.




# Drill 16
# Add two floats
total = 1.5 + 2.5
print(total)

# Drill 17
# Subtract two floats
result = 4.75 - 1.25
print(result)

# Drill 18
# Multiply two floats
product = 2.0 * 3.5
print(product)

# Drill 19
# Add float and integer
mix = 1.2 + 3
print(mix)

# Drill 20
# Multiply float and integer
value = 2.5 * 4
print(value)




#          Drills 21–25 — Mixed Type Arithmetic
# Focus: Mix integers and floats in calculations.

# Why this matters:
# Real programs don’t separate types — you’ll often combine whole and decimal values.
# You need to understand how Python handles the mix.

# You’ll learn:
# Python defaults to float if either operand is a float.
# You don’t need to convert manually in most arithmetic cases.
# # Mixed type math trains flexibility and trust in Python’s arithmetic engine.




# Drill 21
# Add integer and float, store in result
result = 10 + 2.5
print(result)

# Drill 22
# Subtract float from integer
difference = 5 - 1.1
print(difference)

# Drill 23
# Multiply float and integer
product = 3 * 1.5
print(product)

# Drill 24
# Combine float and integer with multiple operations
calculation = 2 + 3.5 - 1
print(calculation)

# Drill 25
# Use float, integer, and multiplication in one line
combo = 2 * 1.1 + 3
print(combo)




#           Drills 26–30 — Order of Operations
# Focus: Use parentheses to control math flow.

# Why this matters:
# Misplaced parentheses = wrong logic. This teaches you how to control math flow — a key debugging skill.

# You’ll learn:
# Without parentheses, math follows operator precedence.
# Parentheses override that order.
# Nesting teaches you how to break logic into layers, like puzzle pieces.




# Drill 26
# Without parentheses — test order of operations
result = 2 + 3 * 4
print(result)

# Drill 27
# With parentheses to change order
result = (2 + 3) * 4
print(result)

# Drill 28
# Multiple parentheses levels
value = (5 + 3) * (2 + 1)
print(value)

# Drill 29
# Mix subtraction, multiplication, parentheses
total = (10 - 2) * 3
print(total)

# Drill 30
# Nested parentheses with all operators
final = ((2 + 3) * (4 - 1)) + 5
print(final)




#          Drills 31–35 — Division Variants
# Focus: Explore /, //, and %.

# Why this matters:
# Python gives you three kinds of division for different tasks — 
# floats, whole counts, and remainders. These show up constantly in puzzles, UI design, 
# and rounding logic.

# You’ll learn:
# / gives float division
# // gives floor division (cuts off decimals)
# % gives the remainder (like “what’s left over?”)




# Drill 31
# Use standard division with /
result = 10 / 4
print(result)

# Drill 32
# Use floor division //
floor = 10 // 4
print(floor)

# Drill 33
# Use modulo %
mod = 10 % 4
print(mod)

# Drill 34
# Combine floor and modulo
floor = 17 // 3
mod = 17 % 3
print(floor, mod)

# Drill 35
# Combine /, //, and % on same values
print(17 / 4)
print(17 // 4)
print(17 % 4)




# Drills 36–40 — Compound Assignment
# Focus: Use +=, -=, etc. to update numbers.

# Why this matters:
# These shortcuts are everywhere — they compress math and update into one command.
#  You’ll use them in loops, counters, and responsive systems.

# You’ll learn:
# x += 1 is shorthand for x = x + 1
# All math operators have a compound version
# They make your code cleaner, faster, easier to read




# Drill 36
# Use += on a number
x = 5
x += 3
print(x)

# Drill 37
# Use -= to decrease a number
y = 10
y -= 4
print(y)

# Drill 38
# Use *= to scale a number
z = 2
z *= 6
print(z)

# Drill 39
# Use /= to divide a float
a = 9.0
a /= 3
print(a)

# Drill 40
# Combine multiple compound operations
b = 8
b += 2
b *= 3
print(b)




# Drills 41–45 — Absolute Values
# Focus: Use abs() to get positive magnitudes.

# Why this matters:
# Sometimes you only care about how big a number is, not its sign. abs() is essential 
# for distance, change, and difference calculations.

# You’ll learn:

# abs(-7) returns 7

# It works on int or float

# It removes negative signs, not decimals




# Drill 41
# Use abs() on a positive number
val = abs(5)
print(val)

# Drill 42
# Use abs() on a negative number
val = abs(-10)
print(val)

# Drill 43
# Use abs() on the result of subtraction
diff = abs(3 - 7)
print(diff)

# Drill 44
# Assign abs() result to variable and print
x = abs(-4.5)
print(x)

# Drill 45
# Combine abs() with arithmetic
result = abs(-3) + 5
print(result)





#  Drills 46–50 — Rounding & Precision
# Focus: Use round() to control decimals.

#  Why this matters:
# Precision is everything in display, math, and finance. This teaches you how to clean up messy decimal results or control the number of digits shown.

# You’ll learn:
# round(x) rounds to the nearest whole number
# Round(x, 2) rounds to 2 decimal places
# It helps avoid floating point clutter

# Drill 46
# Round a float to nearest whole number
val = round(3.6)
print(val)

# Drill 47
# Round down value
print(round(2.3))

# Drill 48
# Round to 1 decimal place
print(round(5.678, 1))

# Drill 49
# Round to 2 decimal places
print(round(9.8765, 2))

# Drill 50
# Combine arithmetic and round
x = round(2.5 * 3.1, 1)
print(x)


# Drills 51–55 — Type Conversion Basics
# Focus: Convert numbers between float and int.

# Why this matters:
# Sometimes you must force Python to switch types — especially before printing, formatting, or storing.

# You’ll learn:

# int(4.8) removes the decimal (no rounding)

# float(4) adds .0

# Type conversion lets you cleanly shift values across contexts




# Drill 51
# Convert integer to float
x = float(4)
print(x)

# Drill 52
# Convert float to integer
y = int(3.9)
print(y)

# Drill 53
# Store float as int and print
num = int(7.8)
print(num)

# Drill 54
# Store int as float and print
val = float(2)
print(val)

# Drill 55
# Convert result of arithmetic
z = float(5 + 2)
print(z)




#  Drills 56–60 — Negative Numbers
# Focus: Use and manipulate negatives confidently.

# Why this matters:
# Negatives show up in math, coordinates, and logic. You need to be fluent in how they behave — including tricky double-negatives.

# You’ll learn:

# Subtracting a negative adds

# Multiplying by a negative flips sign

# Division follows sign rules too




# Drill 56
# Assign and print a negative integer
x = -15
print(x)

# Drill 57
# Add negative number to positive
result = 10 + (-3)
print(result)

# Drill 58
# Subtract negative number (double negative)
total = 4 - (-2)
print(total)

# Drill 59
# Multiply with negative
outcome = -3 * 4
print(outcome)

# Drill 60
# Divide negative float
value = -9.0 / 3
print(value)




# 🧠 Drills 61–65 — Basic Math Functions
# Focus: Use built-in math helpers: min(), max(), pow().

# Why this matters:
# Python gives you tools to compare and compute — no need to reinvent them. These helpers reduce your code and boost readability.

# You’ll learn:

# min() and max() return the smallest/largest

# pow(x, y) means “x to the power of y”

# These work with pure numbers — no imports needed




# Drill 61
# Use min() with two numbers
result = min(4, 7)
print(result)

# Drill 62
# Use max() with three numbers
result = max(3, 9, 1)
print(result)

# Drill 63
# Use pow() to calculate power
value = pow(2, 3)
print(value)

# Drill 64
# Combine min() and max()
low = min(5, 2)
high = max(10, 8)
print(low, high)

# Drill 65
# Use pow() on float base
output = pow(2.5, 2)
print(output)





# 🧩 Drills 66–70 — Expressions & Grouping
# Focus: Combine all previous skills into full expressions.

# Why this matters:
# Real code doesn’t do one step at a time. This trains your ability to read, write, and debug full expressions that use multiple operations and parentheses.

# You’ll learn:

# Expressions = math sentences

# Parentheses control complexity

# Combining operations increases fluency and confidence




# Drill 66
# Combine +, -, *, /
result = 2 + 3 * 4 - 6 / 2
print(result)

# Drill 67
# Group operations with ()
value = (2 + 3) * (4 - 1)
print(value)

# Drill 68
# Use nested parentheses in expression
calc = ((1 + 2) * 3) - (4 / 2)
print(calc)

# Drill 69
# Use parentheses and float division
x = (5.5 + 2.5) / 2
print(x)

# Drill 70
# Complex mixed grouping
answer = (2 + (3 * (4 - 1))) + 6
print(answer)





# ✅ Drills 71–75 — Number Identity Checks
# Focus: Compare numbers using == and !=.

# Why this matters:
# Even though we’re avoiding full logic (e.g., if-statements), comparison is core to any reasoning process. This lets you verify values with simple tests.

# You’ll learn:

# == checks equality

# != checks inequality

# Comparing float vs int is valid (5.0 == 5 is True)




# Drill 71
# Compare two equal numbers with ==
print(5 == 5)

# Drill 72
# Compare two unequal numbers with ==
print(3 == 4)

# Drill 73
# Use != to check inequality
print(10 != 7)

# Drill 74
# Compare result of expression
print((2 + 2) == 4)

# Drill 75
# Check float and int equality
print(5.0 == 5)




# 🧠 Drills 76–80 — Final Fluency Drills
# Focus: Mix everything — assign, calculate, convert, and print.

# Why this matters:
# This is your final practice block before the mini-project. These drills check that all atomic actions are automatic — no hesitation, no second-guessing.

# You’ll learn:

# You can read and write multi-step expressions

# You can trust your instinct on types, grouping, and results

# You’re fluent — ready to build small number-based tools

# Drill 76
# Full expression with all operators
x = (3 + 2) * 4 / 2 - 1
print(x)

# Drill 77
# Convert, round, and print
y = round(float(8) / 3, 2)
print(y)

# Drill 78
# Combine abs, pow, and arithmetic
z = abs(-3) + pow(2, 2)
print(z)

# Drill 79
# Min/max combo with arithmetic
a = min(3 + 2, max(1, 4))
print(a)

# Drill 80
# Final test: assignment, arithmetic, rounding
final = round((2.5 + 1.5) * 2)
print(final)
