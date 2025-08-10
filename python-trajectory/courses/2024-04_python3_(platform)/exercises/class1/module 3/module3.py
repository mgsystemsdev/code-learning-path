# ============================================================
#  File:        module3.py
#  Author:      Miguel Gonzalez Almonte
#  Created:     2025-06-01
#  Description: 
# ------------------------------------------------------------
#  Course:      Python 3 Programming Specialization (Coursera)
#  Module:      Module 3 of Class 1
#  Purpose:     
# ------------------------------------------------------------
#  Notes:
#  - 
#  - 
#  - 
# ============================================================
# ============================================================
#   8.1. Intro: What we can do with Turtles and Conditionals   
# ============================================================

import turtle
wn = turtle.Screen()

amy = turtle.Turtle()
amy.pencolor("Pink")
amy.forward(50)
if amy.pencolor() == "Pink":
    amy.right(60)
    amy.forward(100)
else:
    amy.left(60)
    amy.forward(100)

kenji = turtle.Turtle()
kenji.forward(60)
if kenji.pencolor() == "Pink":
    kenji.right(60)
    kenji.forward(100)
else:
    kenji.left(60)
    kenji.forward(100)


#--------

import turtle
wn = turtle.Screen()

amy = turtle.Turtle()
amy.pencolor("Pink")
amy.right(170)

colors = ["Purple", "Yellow", "Orange", "Pink", "Orange", "Yellow", "Purple", "Orange", "Pink", "Pink", "Orange", "Yellow", "Purple", "Orange", "Purple", "Yellow", "Orange", "Pink", "Orange", "Purple", "Purple", "Yellow", "Orange", "Pink", "Orange", "Yellow", "Purple", "Yellow"]


for color in colors:
    if amy.pencolor() == "Purple":
        amy.forward(50)
        amy.right(59)
    elif amy.pencolor() == "Yellow":
        amy.forward(65)
        amy.left(98)
    elif amy.pencolor() == "Orange":
        amy.forward(30)
        amy.left(60)
    elif amy.pencolor() == "Pink":
        amy.forward(50)
        amy.right(57)

    amy.pencolor(color)

# ============================================================
#     8.2. Boolean Values and Boolean Expressions
# ============================================================

print(True)
print(type(True))
print(type(False))

#--------
print(type(True))
print(type("True"))


#--------

print(5 == 5)
print(5 == 6)

# ============================================================
#      8.3. Logical operators
# ============================================================

x = True
y = False
print(x or y)
print(x and y)
print(not x)

#--------

x = 5
print(x > 0 and x < 10)

n = 25
print(n % 2 == 0 or n % 3 == 0)

#--------

total_weight = int(input('Enter total weight of luggage:'))
num_pieces = int(input('Number of pieces of luggage?'))

if total_weight / num_pieces > 50:
   print('Average weight is greater than 50 pounds -> $100 surcharge.')

print('Luggage check complete.')

#--------

total_weight = int(input('Enter total weight of luggage:'))
num_pieces = int(input('Number of pieces of luggage?'))

if num_pieces != 0 and total_weight / num_pieces > 50:
   print('Average weight is greater than 50 pounds -> $100 surcharge.')

print('Luggage check complete.')


# ============================================================
#      8.4. The in and not in operators
# ============================================================

print('p' in 'apple')
print('i' in 'apple')
print('ap' in 'apple')
print('pa' in 'apple')


#--------

print('a' in 'a')
print('apple' in 'apple')
print('' in 'a')
print('' in 'apple')

#--------

print('x' not in 'apple')


#--------

print("a" in ["a", "b", "c", "d"])
print(9 in [3, 2, 9, 10, 9.0])
print('wow' not in ['gee wiz', 'gosh golly', 'wow', 'amazing'])

#--------

print("a" in ["apple", "absolutely", "application", "nope"])


# ============================================================
#      8.5. Precedence of Operators
# ============================================================


# | **Level** | **Category**       | **Operators**                     |
# |-----------|--------------------|-----------------------------------|
# | 7 (high)  | Exponentiation      | `**`                             |
# | 6         | Multiplication/Divi | `*`, `/`, `//`, `%`              |
# | 5         | Addition/Sub.       | `+`, `-`                         |
# | 4         | Relational          | `==`, `!=`, `<=`, `>=`, `>`, `<` |
# | 3         | Logical NOT         | `not`                            |
# | 2         | Logical AND         | `and`                            |
# | 1 (low)   | Logical OR          | `or`                             |



# ============================================================
#      18.2. Checking Assumptions About Data Types¶
# ============================================================

assert type(9//5) == int
assert type(9.0//5) == int

#--------

lst = ['a', 'b', 'c']

first_type = type(lst[0])
for item in lst:
    assert type(item) == first_type

lst2 = ['a', 'b', 'c', 17]
first_type = type(lst2[0])
for item in lst2:
    assert type(item) == first_type

# ============================================================
#      18.2. Checking Other Assumptions
# ============================================================

# Define a list with 3 elements
lst = ['a', 'b', 'c']

# Assert that the list has fewer than 10 elements
assert len(lst) < 10

# If the assertion passes, continue running the rest of the code
print("Assertion passed. The list has fewer than 10 items.")

# ============================================================
#      8.6. Conditional Execution: Binary Selection¶
# ============================================================

x = 15

if x % 2 == 0:
    print(x, "is even")
else:
    print(x, "is odd")

#--------

# Write code to assign the string "You can apply to SI!" to output if the string "SI 106" is in the list courses. 
# If it is not in courses, assign the value "Take SI 106!" to the variable output.

courses = ["ENGR 101", "SI 110", "ENG 125", "SI 106", "CHEM 130"]


if "SI 106" in courses:
    output = "You can apply to SI!"
else:
    output = "Take SI 106!"

#--------

# Create a variable, b, and assign it the value of 15. Then, write code to see if the value b is greater than that of a. If it is, a’s value should be multiplied by 2. 
# If the value of b is less than or equal to a, nothing should happen. Finally, create variable c and assign it the value of the sum of a and b.

a = 20
b = 15

if b > a:
    a = a * 2

c = a + b


# ============================================================
#      8.7. Omitting the else Clause: Unary Selection
# ============================================================

x = 10
if x < 0:
    print("The negative number ",  x, " is not valid here.")
print("This is always printed")


# ============================================================
#      8.8. Nested conditionals
# ============================================================

x = 10
y = 10

if x < y:
    print("x is less than y")
else:
    if x > y:
        print("x is greater than y")
    else:
        print("x and y must be equal")

# ============================================================
#      8.9. Chained conditionals
# ============================================================

if x < y:
    print("x is less than y")
elif x > y:
    print("x is greater than y")
else:
    print("x and y must be equal")

#--------

x = 10
y = 10

if x < y:
    print("x is less than y")
elif x > y:
    print("x is greater than y")
else:
    print("x and y must be equal")

#--------

# Create one conditional to find whether “false” is in string str1. If so, assign variable output the string “False. You aren’t you?”. 
# Check to see if “true” is in string str1 and if it is then assign “True! You are you!” to the variable output. 
# If neither are in str1, assign “Neither true nor false!” to output.

str1 = "Today you are you! That is truer than true! There is no one alive who is you-er than you!"

if "false" in str1:
    output = "False. You aren’t you?"
elif "true" in str1:
    output = "True! You are you!"
else:
    output = "Neither true nor false!"

print(output)

#--------
# Create an empty list called resps. Using the list percent_rain, for each percent, if it is above 90, add the string ‘Bring an umbrella.’ to resps, 
# otherwise if it is above 80, add the string ‘Good for the flowers?’ to resps, otherwise if it is above 50, add the string ‘Watch out for clouds!’ to resps, 
# otherwise, add the string ‘Nice day!’ to resps. Note: if you’re sure you’ve got the problem right but it doesn’t pass, then check that you’ve matched up the strings exactly.

percent_rain = [94.3, 45, 100, 78, 16, 5.3, 79, 86]
resps = []

for percent in percent_rain:
    if percent > 90:
        resps.append('Bring an umbrella.')
    elif percent > 80:
        resps.append('Good for the flowers?')
    elif percent > 50:
        resps.append('Watch out for clouds!')
    else:
        resps.append('Nice day!')

print(resps)


#--------

# We have created conditionals for you to use. Do not change the provided conditional statements. Find an integer value for x that will cause output to hold the values True and None. 
# (Drawing diagrams or flow charts for yourself may help!)

x = 64
output = []

if x > 63:
    output.append(True)
elif x > 55:
    output.append(False)
else:
    output.append("Neither")

if x > 67:
    output.append(True)
else:
    output.append(None)

print(output)  # ➜ [True, None]



# ============================================================
#      18.3. Testing Conditionals
# ============================================================

if x < y:
    z = x
else:
    if x > y:
        z = y
    else:
        ## x must be equal to y
        z = 0


#--------

x = 3
y = 4

if x < y:
    z = x
else:
    if x > y:
        z = y
    else:
        # x must be equal to y
        assert x == y
        z = 0

print(z)

# ============================================================
#      8.10. The Accumulator Pattern with Conditionals
# ============================================================


phrase = "What a wonderful day to program"
tot = 0
for char in phrase:
    if char != " ":
        tot = tot + 1
print(tot)

#--------

s = "what if we went to the zoo"
x = 0
for i in s:
    if i in ['a', 'e', 'i', 'o', 'u']:
        x += 1
print(x)


#--------

nums = [9, 3, 8, 11, 5, 29, 2]
best_num = 0
for n in nums:
    if n > best_num:
        best_num = n
print(best_num)


#--------

nums = [9, 3, 8, 11, 5, 29, 2]
best_num = nums[0]
for n in nums:
    if n > best_num:
        best_num = n
print(best_num)

#--------

# For each string in the list words, find the number of characters in the string. If the number of characters in the string is greater than 3, add 1 to the variable num_words 
# so that num_words should end up with the total number of words with more than 3 characters.

words = ["water", "chair", "pen", "basket", "hi", "car"]
num_words = 0

for word in words:
    if len(word) > 3:
        num_words += 1

print(num_words)

#--------


# Challenge For each word in words, add ‘d’ to the end of the word if the word ends in “e” to make it past tense. Otherwise, add ‘ed’ to make it past tense. 
# Save these past tense words to a list called past_tense.

words = ["adopt", "bake", "beam", "confide", "grill", "plant", "time", "wave", "wish"]
past_tense = []

for word in words:
    if word.endswith("e"):
        past_tense.append(word + "d")
    else:
        past_tense.append(word + "ed")

print(past_tense)



# ============================================================
#  course_1_assessment_7
# ============================================================

# rainfall_mi is a string that contains the average number of inches of rainfall in Michigan for every month (in inches) with every month separated by a comma. 
# Write code to compute the number of months that have more than 3 inches of rainfall. Store the result in the variable num_rainy_months. In other words, count the number of items with values > 3.0.

# Hard-coded answers will receive no credit.

rainfall_mi = "1.65, 1.46, 2.05, 3.03, 3.35, 3.46, 2.83, 3.23, 3.5, 2.52, 2.8, 1.85"

# Step 1: Split the string into a list of strings
rain_values = rainfall_mi.split(", ")

# Step 2: Convert each string to a float
rain_floats = [float(val) for val in rain_values]

# Step 3: Count values greater than 3.0
num_rainy_months = 0
for rain in rain_floats:
    if rain > 3.0:
        num_rainy_months += 1

print(num_rainy_months)


#--------

# The variable sentence stores a string. Write code to determine how many words in sentence start and end with the same letter, including one-letter words. 
# Store the result in the variable same_letter_count.

# Hard-coded answers will receive no credit.


# Write your code here.

# Step 1: Split the sentence into words
words = sentence.split()

# Step 2: Initialize the counter
same_letter_count = 0

# Step 3: Loop through each word and compare first and last letters
for word in words:
    if word[0] == word[-1]:
        same_letter_count += 1

print(same_letter_count)

#--------

# Write code to count the number of strings in list items that have the character w in it. Assign that number to the variable acc_num.

# HINT 1: Use the accumulation pattern!

# HINT 2: the in operator checks whether a substring is present in a string.

# Hard-coded answers will receive no credit

items = ["whirring", "wow!", "calendar", "wry", "glass", "", "llama","tumultuous","owing"]

# Step 1: Initialize accumulator
acc_num = 0

# Step 2: Loop through each string in the list
for word in items:
    if 'w' in word:
        acc_num += 1

print(acc_num)


#--------

# Write code that counts the number of words in sentence that contain either an “a” or an “e”. Store the result in the variable num_a_or_e.

# Note 1: be sure to not double-count words that contain both an a and an e.

# HINT 1: Use the in operator.

# HINT 2: You can either use or or elif.

# Hard-coded answers will receive no credit.

sentence = "python is a high level general purpose programming language that can be applied to many different classes of problems."

# Step 1: Split the sentence into words
words = sentence.split()

# Step 2: Initialize the counter
num_a_or_e = 0

# Step 3: Loop through each word and check for 'a' or 'e'
for word in words:
    if 'a' in word or 'e' in word:
        num_a_or_e += 1

print(num_a_or_e)

#--------
# Write code that will count the number of vowels in the sentence s and assign the result to the variable num_vowels. For this problem, 
# vowels are only a, e, i, o, and u. Hint: use the in operator with vowels.

s = "singing in the rain and playing in the rain are two entirely different situations but both can be fun"
vowels = ['a','e','i','o','u']

# Write your code here.

num_vowels = 0

# Step 2: Loop through each character in the sentence
for char in s:
    if char in vowels:
        num_vowels += 1

print(num_vowels)

