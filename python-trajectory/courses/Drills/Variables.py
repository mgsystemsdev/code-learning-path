# Variable  Practice 

# Drills 1–5: Atomic Basics
# Focus: Create, assign, and print single variables

# Drill 1
color = "blue"         # Create a variable named 'color' and assign it the string value "blue"
print("\n",color,)           # Print the value stored in the variable 'color'

# Drill 2
age = 25               # Create a variable named 'age' and assign it the number 25
print(age)             # Output the value of 'age' to the screen

# Drill 3
greeting = "Hello!"    # Create a variable called 'greeting' with a string value
print(greeting)        # Display the content of 'greeting'

# Drill 4
is_sunny = True        # Declare a boolean variable named 'is_sunny' and assign it the value True
print(is_sunny)        # Print the boolean value held by 'is_sunny'

# Drill 5
height = 5.9           # Assign a floating point number (decimal) to the variable 'height'
print(height,'\n')          # Output the value of 'height'

# Drill Block 6–10: Value Swaps
# Focus: Reassign and overwrite variable values

# Drill 6
city = "Paris"         # Assign the string "Paris" to the variable 'city'
city = "Tokyo"         # Reassign 'city' to a new value: "Tokyo"
print(city)            # Print the current value of 'city' (should be "Tokyo")

# Drill 7
score = 100            # Create a variable 'score' with initial value 100
score = 85             # Change the value of 'score' to 85
print(score)           # Output the new value of 'score'

# Drill 8
language = "Python"    # Set 'language' to "Python"
language = "Java"      # Reassign 'language' to "Java"
print(language)        # Print the updated language

# Drill 9
is_open = False        # Declare a boolean variable 'is_open' and assign it False
is_open = True         # Change 'is_open' to True
print(is_open)         # Output the new boolean value

# Drill 10
temperature = 20       # Set 'temperature' to 20
temperature = 30       # Reassign 'temperature' to 30
print(temperature)     # Display the updated temperature

print("")

# Block 11–15: Variable Naming Rules
# Focus: Practice valid/invalid naming conventions.
# You'll apply Python’s variable naming rules:
# Valid names start with letters or underscores, use lowercase with underscores, and don’t clash with keywords.

# Drill 11
first_name = "Alice"          # Valid: uses lowercase letters and underscore
print(first_name)             # Print the variable 'first_name'

# Drill 12
_last_score = 98              # Valid: starts with an underscore
print(_last_score)            # Output the value of '_last_score'

# Drill 13
user2 = "Charlie"             # Valid: ends with a number, which is allowed
print(user2)                  # Display the value of 'user2'

# Drill 14
# 2nd_place = "Bob"           # Invalid: cannot start with a number (commented out to avoid error)
second_place = "Bob"          # Corrected version with valid name
print(second_place)           # Output the corrected variable

# Drill 15
# full name = "Eve"           # Invalid: variable names cannot have spaces (commented out)
full_name = "Eve"             # Correct version using underscore
print(full_name,'\n')              # Output the corrected variable

# Drill Block 16–20: Type Integrity
# Focus: Assign variables with different data types — and keep them clearly separated.
# The goal here is to not confuse types — e.g., don’t accidentally assign a number where a string was intended.

# Drill 16
age = 32                    # Integer type
print('\n',age)                  # Output the integer

# Drill 17
price = 19.99               # Float type (decimal)
print(price)                # Output the float

# Drill 18
name = "Jordan"             # String type
print(name)                 # Output the string

# Drill 19
is_member = True            # Boolean type
print(is_member)            # Output the boolean

# Drill 20
# Mixing types (illustrative only)
message = "Your total is"   # String type
total = 45.50               # Float type
print(message)              # Print string
print(total,'\n')                # Print float separately to keep type boundaries clear

#Drill Block 21–25: Sequential Assignment
# Focus:
# Assign multiple variables one after another, in a logical flow — usually across multiple lines.
# You’ll build clean chains of assignments, without overwriting or skipping steps.

# Drill Block 26–30: Shadowing Practice
# Focus: Practice reusing variable names to simulate “shadowing” — meaning the same name is reused with new meaning or value.
# This builds awareness of overwriting and why context matters.

# Drill 26
value = 100              # Assign 100 to 'value'
value = "one hundred"    # Reassign 'value' with a new string
print('\n',value)             # Output: now prints the string "one hundred"

# Drill 27
message = "Start"        # Assign initial string to 'message'
message = 404            # Reassign with an integer
print(message)           # Output: 404

# Drill 28
status = True            # Boolean assignment
status = "active"        # Now 'status' is a string
print(status)            # Output: "active"

# Drill 29
temperature = 75.0       # Start with a float
temperature = "warm"     # Then overwrite with a string
print(temperature)       # Output: "warm"

# Drill 30
data = "raw"             # Initial string
data = [1, 2, 3]         # Reassign as a list
print(data,'\n')              # Output: [1, 2, 3]

# Drill Block 31–35: Memory Anchoring
# Focus: Track how a variable’s value changes over time.
# We’re anchoring to memory by observing step-by-step mutations — no overwriting without observation.

# Drill 31
counter = 0             # Start at zero
print("\n",counter)          # Output: 0
counter = 1             # Change value
print(counter)          # Output: 1

# Drill 32
status = "loading"      # Initial state
print(status)           # Output: loading
status = "ready"        # Update state
print(status)           # Output: ready

# Drill 33
level = 1               # Start at level 1
print(level)            # Output: 1
level = level + 1       # Go to level 2
print(level)            # Output: 2

# Drill 34
speed = 10              # Initial speed
print(speed)            # Output: 10
speed = speed - 2       # Reduce speed
print(speed)            # Output: 8

# Drill 35
volume = 50             # Start volume at 50
print(volume)           # Output: 50
volume = volume + 10    # Increase volume
print(volume,"\n")           # Output: 60

# Drill Block 41–45: Parallel Declaration
# Focus: Declare multiple variables at once in a single line.
# Use clean, parallel syntax to assign efficiently.

# Drill 41
x, y = 5, 10            # Assign 5 to x, 10 to y in a single line
print("\n",x, y)             # Output: 5 10

# Drill 42
name, age = "Tina", 30  # Assign string and integer in one go
print(name, age)        # Output: Tina 30

# Drill 43
a, b, c = 1, 2, 3       # Assign 1 → a, 2 → b, 3 → c
print(a, b, c)          # Output: 1 2 3

# Drill 44
first, second = "one", "two"    # Two strings, two variables
print(first)                    # Output: one
print(second)                   # Output: two

# Drill 45
width, height = 1920, 1080      # Parallel screen dimensions
print(width, height,"\n")            # Output: 1920 1080

# Drill Block 46–50: Chain Assignment
# Focus: Assign the same value to multiple variables in a single line.

# Drill 46
a = b = 0              # Assign 0 to both a and b
print(a, b)            # Output: 0 0

# Drill 47
is_ready = is_active = True    # Both variables set to True
print(is_ready, is_active)     # Output: True True

# Drill 48
x = y = z = 100         # Assign 100 to three variables at once
print(x, y, z)          # Output: 100 100 100

# Drill 49
language1 = language2 = "Python"   # Assign "Python" to two variables
print(language1, language2)        # Output: Python Python

# Drill 50
width = height = depth = 1.5       # Same float assigned to all three
print(width, height, depth)        # Output: 1.5 1.5 1.5

# Drill Block 51–55: Internal Consistency
# Focus: Use variables together without breaking coherence — e.g., names, types, and roles should match their purpose.
# This block checks for clean logic across small clusters of variables.

# Drill 51
item = "Book"            # Item name as string
price = 12.99            # Item price as float
print(item, price)       # Output: Book 12.99

# Drill 52
username = "alex_92"     # Simulated username
logged_in = True         # Boolean login status
print(username, logged_in)  # Output: alex_92 True

# Drill 53
title = "Dr."            # Prefix/title
name = "Lee"             # Last name
full_name = title + " " + name   # Combine into one string
print(full_name)         # Output: Dr. Lee

# Drill 54
score = 85               # Score value
max_score = 100          # Maximum possible
percent = (score / max_score) * 100   # Calculate percentage
print(percent)           # Output: 85.0

# Drill 55
file_name = "report.pdf"     # File name string
file_type = "pdf"            # File extension/type
matches = file_name.endswith(file_type)   # Check if type matches
print(matches)               # Output: True


# Drill Block 56–60: Temporary Variables
# Focus: Use temporary (helper) variables to hold intermediate values during swaps or transformations.
# This prevents accidental loss of data.

# Drill 56
a = 5                   # Start with value 5
b = 10                  # Start with value 10
temp = a                # Save a's value into temp
a = b                   # Now assign b's value to a
b = temp                # Restore a's old value into b
print(a, b)             # Output: 10 5

# Drill 57
x = "left"              # Original value
y = "right"             # Original value
temp = x                # Save 'left' in temp
x = y                   # x becomes 'right'
y = temp                # y becomes 'left'
print(x, y)             # Output: right left

# Drill 58
first = 1               # Value 1
second = 2              # Value 2
temp = first + second   # Store sum in temp
print(temp)             # Output: 3

# Drill 59
value = 20              # Starting value
temp = value * 2        # Double it temporarily
value = temp - 5        # Adjust the result and store it back
print(value)            # Output: 35

# Drill 60
base = 4                # Base value
exponent = 2            # Exponent value
temp = base ** exponent  # Calculate power using temp
result = temp           # Assign to result
print(result)           # Output: 16

# Drill Block 61–65: Mutation Simulation
# Focus: Simulate how mutable-like updates work using plain variables (no lists or dicts — just variables).
# You’ll imitate change by reassigning variables to reflect shifting state.

# Drill 61
status = "waiting"       # Initial state
status = "processing"    # Simulated update
status = "done"          # Final state
print('\n',status)            # Output: done

# Drill 62
step = "begin"           # Starting phase
step = "middle"          # Simulated next phase
step = "end"             # Final stage
print(step)              # Output: end

# Drill 63
mode = "draft"           # Initial mode
mode = "review"          # Review stage
mode = "published"       # Final status
print(mode)              # Output: published

# Drill 64
value = 10               # Initial value
value = value + 5        # First mutation
value = value * 2        # Second mutation
print(value)             # Output: 30

# Drill 65
light = "off"            # Light off
light = "on"             # Light turned on
light = "dimmed"         # Light partially on
print(light)             # Output: dimmed

# Drill Block 66–70: Type Rotation
# Focus: Reassign the same variable name across multiple data types, on purpose.
# This builds flexibility in your mental model — x can be a string, number, or boolean... depending on context.

# Drill 66
item = "apple"           # Start as string
item = 3                 # Now item is an integer
print(item)              # Output: 3

# Drill 67
flag = True              # Boolean value
flag = "yes"             # String value
print(flag)              # Output: yes

# Drill 68
temperature = 98.6       # Float for precision
temperature = "normal"   # Reassign as descriptive string
print(temperature)       # Output: normal

# Drill 69
counter = 1              # Integer
counter = False          # Boolean now
print(counter)           # Output: False

# Drill 70
status = "active"        # String status
status = 1               # Integer status code
print(status)            # Output: 1

# Drill Block 71–75: Value Forecasting
# Focus: Mentally track variable changes over a sequence of steps.
# Predict what a variable holds at the end — it’s about state reasoning, not just writing code.

# Drill 71
x = 2                  # Start with 2
x = x + 3              # Now 5
x = x * 2              # Now 10
print(x)               # Output: 10

# Drill 72
y = 1
y = y + 1              # 2
y = y + y              # 4
print(y)               # Output: 4

# Drill 73
z = 10
z = z - 4              # 6
z = z / 2              # 3.0
print(z)               # Output: 3.0

# Drill 74
message = "Hi"
message = message + " there"     # "Hi there"
message = message + "!"          # "Hi there!"
print(message)                   # Output: Hi there!

# Drill 75
value = 5
value = value * 2                # 10
value = value - 3                # 7
value = value + 1                # 8
print(value)                     # Output: 8


# Drill Block 76–80: Composition Tracking
# Focus: Follow how a variable contributes to a full process — observe it through setup, transformation, and use.
# Think of each variable as part of a micro story.

# Drill 76
base_price = 100                  # Base value
tax = base_price * 0.1            # Tax is 10%
total = base_price + tax          # Final total
print(total)                      # Output: 110.0

# Drill 77
length = 5
width = 3
area = length * width             # Area of a rectangle
print(area)                       # Output: 15

# Drill 78
greeting = "Hello"
name = "Jordan"
message = greeting + ", " + name + "!"   # Compose greeting
print(message)                           # Output: Hello, Jordan!

# Drill 79
price = 25
discount = 5
final_price = price - discount           # Apply discount
print(final_price)                       # Output: 20

# Drill 80
num1 = 8
num2 = 4
average = (num1 + num2) / 2              # Find average
print(average)                           # Output: 6.0
