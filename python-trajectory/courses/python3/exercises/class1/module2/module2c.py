# ============================================================
#  File:        module2.py
#  Author:      Miguel Gonzalez Almonte
#  Created:     2025-06-01
#  Description: 
# ------------------------------------------------------------
#  Course:      Python 3 Programming Specialization (Coursera)
#  Module:      Module 2 of Class 1
#  Purpose:     
# ------------------------------------------------------------
#  Notes:
#  - 
#  - 
#  - 
# ============================================================

# ============================================================
#      the for loop 
# ============================================================

for name in ["Joe", "Amy", "Brad", "Angelina", "Zuki", "Thandi", "Paris"]:
    print("Hi", name, "Please come to my party on Saturday!")

# ============================================================
#      7.4. Strings and for loops
# ============================================================

for achar in "Go Spot Go":
    print(achar)

#--------

# How many times is the word HELLO printed by the following statements? 
# 12

s = "python rocks"
for ch in s:
   print("HELLO")

#--------

# How many times is the word HELLO printed by the following statements? 
# 5

s = "python rocks"
for ch in s[3:8]:
   print("HELLO")

# ============================================================
#      7.5. Lists and for loops
# ============================================================

fruits = ["apple", "orange", "banana", "cherry"]

for afruit in fruits:     # by item
    print(afruit)


#--------

print("This will execute first")

for _ in range(3):
    print("This line will execute three times")
    print("This line will also execute three times")

print("Now we are outside of the for loop!")

# ============================================================
#      7.5.2. Iteration Simplifies our Turtle Program
# ============================================================

import turtle            # set up alex
wn = turtle.Screen()
alex = turtle.Turtle()

for i in [0, 1, 2, 3]:      # repeat four times
    alex.forward(50)
    alex.left(90)

wn.exitonclick()


#--------

import turtle            # set up alex
wn = turtle.Screen()
alex = turtle.Turtle()

for aColor in ["yellow", "red", "purple", "blue"]:      # repeat four times
    alex.forward(50)
    alex.left(90)

wn.exitonclick()

#--------

import turtle            # set up alex
wn = turtle.Screen()
alex = turtle.Turtle()

for aColor in ["yellow", "red", "purple", "blue"]:
    alex.color(aColor)
    alex.forward(50)
    alex.left(90)

wn.exitonclick()

#--------

# How many times will the for loop iterate in the following statements? 
# 9

p = [3, 4, "Me", 3, [], "Why", 0, "Tell", 9.3]
for ch in p:
   print(ch)


#--------

# How does python know what statements are contained in the loop body?

# A. They are indented to the same degree from the loop header.

#--------

# Consider the following code: 
# Draw one side of a square

for aColor in ["yellow", "red", "green", "blue"]:
   alex.forward(50)
   alex.left(90)

# ============================================================
#      7.5.2. Iteration Simplifies our Turtle Program
# ============================================================

nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
accum = 0
for w in nums:
    accum = accum + w
print(accum)

#--------

print("range(5): ")
for i in range(5):
    print(i)

print("range(0,5): ")
for i in range(0, 5):
    print(i)

# Notice the casting of `range` to the `list`
print(list(range(5)))
print(list(range(0,5)))

#--------

accum = 0
for w in range(11):
    accum = accum + w
print(accum)

# or, if you use two inputs for the range function

sec_accum = 0
for w in range(1,11):
    sec_accum = sec_accum + w
print(sec_accum)


#--------

nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
count = 0
for w in nums:
    count = count + 1
print(count)


#--------

# Write code to create a list of integers from 0 through 52 and assign that list to the variable numbers. 
# You should use the Python range function and don’t forget to covert the result to a list – do not type out the whole list yourself.

numbers = list(range(53))

#--------

# Count the number of characters in string str1. Do not use len(). Save the number in variable numbs.

#--------

# Count the number of characters in string str1. Do not use len(). Save the number in variable numbs.

str1 = "I like nonsense, it wakes up the brain cells. Fantasy is a necessary ingredient in living."

numbs = 0
for char in str1:
    numbs += 1

#--------

# Create a list of numbers 0 through 40 and assign this list to the variable numbers. Then, accumulate the total of the list’s values and assign that sum to the variable sum1.

numbers = list(range(41))

sum1 = 0
for num in numbers:
    sum1 += num

# ============================================================
#      7.10. 👩‍💻 Naming Variables in For Loops
# ============================================================

# x is a list defined elsewhere

# for y in x:
#     print(y)

#--------

# genres is a list defined elsewhere

for genre in genres:
     print(genre)

# ============================================================
#      7.9. 👩‍💻 Printing Intermediate Results
# ============================================================

w = range(10)

tot = 0
for num in w:
    tot += num
print(tot)

#--------

w = range(10)

tot = 0
for num in w:
    print(num)
    tot += num
print(tot)

#--------

w = range(10)


tot = 0
for num in w:
    print(num)
    tot += num
    print(tot)
print(tot)

#--------

w = range(10)

tot = 0
print("***** Before the For Loop ******")
for num in w:
    print("***** A New Loop Iteration ******")
    print("Value of num:", num)
    tot += num
    print("Value of tot:", tot)
print("***** End of For Loop *****")
print("Final total:", tot)