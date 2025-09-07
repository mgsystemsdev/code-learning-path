# ============================================================
#  File:        module1b.py
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
#      -Turtles
# ============================================================

import turtle             # allows us to use the turtles library
wn = turtle.Screen()      # creates a graphics window
alex = turtle.Turtle()    # create a turtle named alex
alex.forward(150)         # tell alex to move forward by 150 units
alex.left(90)             # turn by 90 degrees
alex.forward(75)          # complete the second side of a rectangle


#----------------

import turtle

wn = turtle.Screen()
wn.bgcolor("lightgreen")        # set the window background color

tess = turtle.Turtle()
tess.color("blue")              # make tess blue
tess.pensize(3)                 # set the width of her pen

tess.forward(50)
tess.left(120)
tess.forward(50)

wn.exitonclick()                # wait for a user click on the canvas

#-----------------

import turtle
wn = turtle.Screen()             # Set up the window and its attributes
wn.bgcolor("lightgreen")


tess = turtle.Turtle()           # create tess and set his pen width
tess.pensize(5)

alex = turtle.Turtle()           # create alex
alex.color("hotpink")            # set his color

tess.forward(80)                 # Let tess draw an equilateral triangle
tess.left(120)
tess.forward(80)
tess.left(120)
tess.forward(80)
tess.left(120)                   # complete the triangle

tess.right(180)                  # turn tess around
tess.forward(80)                 # move her away from the origin so we can see alex

alex.forward(50)                 # make alex draw a square
alex.left(90)
alex.forward(50)
alex.left(90)
alex.forward(50)
alex.left(90)
alex.forward(50)
alex.left(90)

wn.exitonclick()

# ============================================================
#     Repetition with a For Loop¶
# ============================================================

print("This will execute first")

for _ in range(3):
    print("This line will execute three times")
    print("This line will also execute three times")

print("Now we are outside of the for loop!")

#-----------------

import turtle
wn = turtle.Screen()

elan = turtle.Turtle()

distance = 50
for _ in range(10):
    elan.forward(distance)
    elan.right(90)
    distance = distance + 10

#-----------------

import turtle
wn = turtle.Screen()

#-----------------

import turtle
wn = turtle.Screen()
wn.bgcolor("lightgreen")
tess = turtle.Turtle()
tess.color("blue")
tess.shape("turtle")

dist = 5
tess.up()                     # this is new
for _ in range(30):    # start with size = 5 and grow by 2
    tess.stamp()                # leave an impression on the canvas
    tess.forward(dist)          # move tess along
    tess.right(24)              # and turn her
    dist = dist + 2
wn.exitonclick()

# ============================================================
#     Ramdon module
# ============================================================

import random

prob = random.random()
result = prob * 5
print(result)

#-----------------

import random

prob = random.random()
print(prob)

diceThrow = random.randrange(1,7)       # return an int, one of 1,2,3,4,5,6
print(diceThrow)

# ============================================================
#     Runtine error
# ============================================================


subtotal = input("Enter total before tax:")
# tax = .08 * subTotal
print("tax on", subtotal, "is:", tax)

#-----------------

num1 = input('Enter a number:')
num2 = input('Enter another number:')
sum = num1 + num2

print('The sum of', num1, 'and', num2, 'is', sum)


#-----------------

# current_time_str = input("What is the current time (in hours 0-23)?")
# wait_time_str = input("How many hours do you want to wait")

# current_time_int = int(current_time_str)
# wait_time_int = int(wait_time_int)

# final_time_int = current_time_int + wait_time_int
# print(final_time_int)


#-----------------

# current_time_str = input("What is the current time (in hours 0-23)?")
# #wait_time_str = input("How many hours do you want to wait"

# current_time_int = int(current_time_str)
# wait_time_int = int(wait_time_str)

# final_time_int = current_time_int + wait_time_int
# print(final_time_int)


#-----------------

# #current_time_str = input("What is the "current time" (in hours 0-23)?")
# wait_time_str = input("How many hours do you want to wait")

# current_time_int = int(current_time_str)
# wait_time_int = int(wait_time_str)

# final_time_int = current_time_int + wait_time_int
# print(final_time_int)

#-----------------

a = input('wpisz godzine')
x = input('wpisz liczbe godzin')
int(x)
int(a)
h = x // 24
s = x % 24
print (h, s)
a = a + s
print ('godzina teraz', a)


#-----------------


# str_time = input("What time is it now?")
# str_wait_time = input("What is the number of hours to wait?")
# time = int(str_time)
# wai_time = int(str_wait_time)

# time_when_alarm_go_off = time + wait_time
# print(time_when_alarm_go_off)

# ============================================================
#     Semantic Errors
# ============================================================


num1 = input('Enter a number:')
num2 = input('Enter another number:')
sum = num1 + num2

print('The sum of', num1, 'and', num2, 'is', sum)

#-----------------

# Which of the following is a semantic error?

#. Forgetting to divide by 100 when printing a percentage amount.

#-----------------

# Who or what typically finds semantic errors?

#. The programmer

# ============================================================
#     Know Your Error Messages
# ============================================================
# current_time_str = input("What is the current time (in hours 0-23)?")
# wait_time_str = input("How many hours do you want to wait")

# current_time_int = int(current_time_str)
# wait_time_int = int(wait_time_int)

# final_time_int = current_time_int + wait_time_int
# print(final_time_int)

#-----------------
# Which of the following explains why wait_time_int = int(wait_time_int) is an error?

# . wait_time_int does not have a value so it cannot be used on the right hand side

#-----------------
# 3.8.1. SyntaxError¶
#-----------------

# current_time_str = input("What is the current time (in hours 0-23)?")
# wait_time_str = input("How many hours do you want to wait"

# current_time_int = int(current_time_str)
# wait_time_int = int(wait_time_str)

# final_time_int = current_time_int + wait_time_int
# print(final_time_int)

# Answer


# current_time_str = input("What is the current time (in hours 0-23)?")
# wait_time_str = input("How many hours do you want to wait"

# current_time_int = int(current_time_str)
# wait_time_int = int(wait_time_str)

# final_time_int = current_time_int + wait_time_int
# print(final_time_int)


#-----------------

# current_time_str = input("What is the "current time" (in hours 0-23)?")
# wait_time_str = input("How many hours do you want to wait")

# current_time_int = int(current_time_str)
# wait_time_int = int(wait_time_str)

# final_time_int = current_time_int + wait_time_int
# print(final_time_int)

# Answer

# current_time_str = input("What is the "current time" (in hours 0-23)?")
# wait_time_str = input("How many hours do you want to wait")

# current_time_int = int(current_time_str)
# wait_time_int = int(wait_time_str)

# final_time_int = current_time_int + wait_time_int
# print(final_time_int)

#-----------------
#. 3.8.2. TypeError¶
#-----------------



a = input('wpisz godzine')
x = input('wpisz liczbe godzin')
int(x)
int(a)
h = x // 24
s = x % 24
print (h, s)
a = a + s
print ('godzina teraz', a)


# Solution

# In finding this error there are few lessons to think about. First, you may find it very disconcerting that you cannot understand the whole program.

# Unless you speak Polish then this won’t be an issue. But, learning what you can ignore, and what you need to focus on is a very important part of the debugging process.

#  Second, types and good variable names are important and can be very helpful. In this case a and x are not particularly helpful names, and in particular they do not help you

# think about the types of your variables, which as the error message implies is the root of the problem here. The rest of the lessons we will get back to in a minute.

# The error message provided to you gives you a pretty big hint. TypeError: unsupported operand type(s) for FloorDiv: 'str' and 'number' on line: 5 On line five we are trying to use integer 
#
# division on x and 24. The error message tells you that you are tyring to divide a string by a number. In this case you know that 24 is a number so x must be a string. But how? You can see the 

# function call on line 3 where you are converting x to an integer. int(x) or so you think. This is lesson three and is one of the most common errors we see in introductory programming. 

# What is the difference between int(x) and x = int(x)

# The expression int(x) converts the string referenced by x to an integer but it does not store it anywhere. It is very common to assume that int(x) somehow changes x itself, 

#  as that is what you are intending! The thing that makes this very tricky is that int(x) is a valid expression, so it doesn’t cause any kind of error, but rather the error happens later on in the program.

# The assignment statement x = int(x) is very different. Again, the int(x) expression converts the string referenced by x to an integer, but this time it also changes 

# what x references so that x now refers to the integer value returned by the int function.

# So, the solution to this problem is to change lines 3 and 4 so they are assignment statements.

#-----------------

# str_time = input("What time is it now?")
# str_wait_time = input("What is the number of hours to wait?")
# time = int(str_time)
# wai_time = int(str_wait_time)

# time_when_alarm_go_off = time + wait_time
# print(time_when_alarm_go_off)

# Solution

# In this example, the student seems to be a fairly bad speller, as there are a number of typos to fix. The first one is identified as wait_time is not defined on line 6. 
# Now in this example you can see that there is str_wait_time on line 2, and wai_time on line 4 and wait_time on line 6. If you do not have very sharp eyes its easy to miss 
# that there is a typo on line 4.

#-----------------
#. 3.8.3. NameError¶
#-----------------
# n = input("What time is it now (in hours)?")
# n = imt(n)
# m = input("How many hours do you want to wait?")
# m = int(m)
# sum_time = n + m
# time_of_day = sum_time % 12
# print("The time is now", time_of_day)

# Solution

# This one is once again a typo, but the typo is not in a variable name, but rather, the name of a function. The search strategy would help you with this one easily, but there is another clue for you as well. The editor in the textbook, as well as almost all Python editors in the world provide you with color clues. Notice that on line 2 the function imt is not highlighted blue like the word int on line 4.

#-----------------

# present_time = input("Enter the present timein hours:")
# set_alarm = input("Set the hours for alarm:")
# int (present_time, set_time, alarm_time)
# alarm_time = present_time + set_alarm
# print(alarm_time)

# Solution

# In this example the error message is about set_time not defined on line 3. In this case the undefined name is not used in an assignment statement, but is used as a parameter (incorrectly) to a function call. A search on set_time reveals that in fact it is only used once in the program. Did the author mean set_alarm? If we make that assumption we immediately get another error NameError: name 'alarm_time' is not defined on line: 3. The variable alarm_time is defined on line 4, but that does not help us on line 3. Furthermore we now have to ask the question is this function call int(present_time, set_alarm, alarm_time) even the correct use of the int function? The answer to that is a resounding no. Let’s list all of the things wrong with line 3:

# set_time is not defined and never used, the author probably meant set_alarm.

# alarm_time cannot be used as a parameter before it is defined, even on the next line!

# int can only convert one string to an integer at a time.

# Finally, int should be used in an assignment statement. Even if int was called with the correct number of parameters it would have no real effect.

#-----------------
#. 3.8.2. TypeError¶
#-----------------

# current_time_str = input("What is the current time (in hours 0-23)?")
# current_time_int = int(current_time_str)

# wait_time_str = input("How many hours do you want to wait")
# wait_time_int = int(wait_time_str)

# final_time_int = current_time_int + wait_time_int
# print(final_time_int)