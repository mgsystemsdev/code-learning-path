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
#      6.2. Strings, Lists, and Tuples
# ============================================================

# A list is a sequential collection of Python data values, where each value is identified by an index. The values that make up a list are called its elements. 
# Lists are similar to strings, which are ordered collections of characters, except that the elements of a list can have any type and for any one list, the items can be of different types.
# There are several ways to create a new list. The simplest is to enclose the elements in square brackets ( [ and ]).

[10, 20, 30, 40]
["spam", "bungee", "swallow"]

#--------

# The first example is a list of four integers. The second is a list of three strings. As we said above, the elements of a list don’t have to be the same type. 
# The following list contains a string, a float, an integer, and another list.

["hello", 2.0, 5, [10, 20]]

#--------

# ============================================================
#  6.3.1. Index Operator: Accessing Elements of a List or Tuple
# ============================================================



# A tuple, like a list, is a sequence of items of any type. The printed representation of a tuple is a comma-separated sequence of values, enclosed in parentheses. 
# In other words, the representation is just like lists, except with parentheses () instead of square brackets [].

# One way to create a tuple is to write an expression, enclosed in parentheses, that consists of multiple other expressions, separated by commas.

julia = ("Julia", "Roberts", 1967, "Duplicity", 2009, "Actress", "Atlanta, Georgia")

# The key difference between lists and tuples is that a tuple is immutable, meaning that its contents can’t be changed after the tuple is created. 
# We will examine the mutability of lists in detail in the chapter on Mutability.

# To create a tuple with a single element (but you’re probably not likely to do that too often), we have to include the final comma, because without the final comma, 
# Python treats the (5) below as an integer in parentheses:

#--------

t = (5,)
print(type(t))

x = (5)
print(type(x))


#--------

# A list is only allowed to contain integer items.

# A. False

# ============================================================
#  6.3. Index Operator: Working with the Characters of a String¶
# ============================================================

school = "Luther College"
m = school[2]
print(m)

lastchar = school[-1]
print(lastchar)

# ============================================================
#  6.3.1. Index Operator: Accessing Elements of a List or Tuple
# ============================================================




numbers = [17, 123, 87, 34, 66, 8398, 44]
print(numbers[2])
print(numbers[9-8])
print(numbers[-2])

#--------

prices = (1.99, 2.00, 5.50, 20.95, 100.98)
print(prices[0])
print(prices[-1])
print(prices[3-5])

#--------

# What is printed by the following statements?
# h

s = "python rocks"
print(s[3])

#--------

#What is printed by the following statements?
# to

s = "python rocks"
print(s[2] + s[-4])
s = "python rocks"
print(s[2] + s[-4])

#--------

# What is printed by the following statements? 
# 3.14

alist = [3, 67, "cat", [56, 57, "dog"], [ ], 3.14, False]
print(alist[5])

#--------
# Assign the value of the 34th element of lst to the variable output. Note that the l in lst is a letter, not a number; variable names can’t start with a number.

lst = ["hi", "morning", "dog", "506", "caterpillar", "balloons", 106, "yo-yo", "python", "moon", "water", "sleepy", "daffy", 45, "donald", "whiteboard", "glasses", "markers", "couches", "butterfly", "100", "magazine", "door", "picture", "window", ["Olympics", "handle"], "chair", "pages", "readings", "burger", "juggle", "craft", ["store", "poster", "board"], "laptop", "computer", "plates", "hotdog", "salad", "backpack", "zipper", "ring", "watch", "finger", "bags", "boxes", "pods", "peas", "apples", "horse", "guinea pig", "bowl", "EECS"]


#--------

# Assign the value of the 23rd element of l to the variable checking.

l = ("hi", "goodbye", "python", "106", "506", 91, ['all', 'Paul', 'Jackie', "UMSI", 1, "Stephen", 4.5], 109, "chair", "pizza", "wolverine", 2017, 3.92, 1817, "account", "readings", "papers", 12, "facebook", "twitter", 193.2, "snapchat", "leaders and the best", "social", "1986", 9, 29, "holiday", ["women", "olympics", "gold", "rio", 21, "2016", "men"], "26trombones")


#--------

# Assign the value of the 23rd element of l to the variable checking.

#--------

# Assign the value of the last chacter of lst to the variable output. Do this so that the length of lst doesn’t matter

lst = "Every chess or checkers game begins from the same position and has a finite number of moves that can be played. While the number of possible scenarios and moves is quite large, it is still possible for computers to calculate that number and even be programmed to respond well against a human player..."

output = lst[-1]
print(output)


# ============================================================
#  6.4. Disambiguating []: creation vs indexing
# ============================================================

new_lst = []


#--------

new_lst = ["NFLX", "AMZN", "GOOGL", "DIS", "XOM"]
part_of_new_lst = new_lst[0]

#--------

lst = [0]
n_lst = lst[0]

print(lst)
print(n_lst)

# ============================================================
#  6.5. Length
# ============================================================

fruit = "Banana"
print(len(fruit))

#--------

fruit = "Banana"
sz = len(fruit)
last = fruit[sz]       # ERROR!
print(last)


#--------

fruit = "Banana"
sz = len(fruit)
lastch = fruit[sz - 1]
print(lastch)


#--------

alist = ["hello", 2.0, 5]
print(len(alist))
print(len(alist[0]))


#--------

# What is printed by the following statements? 
# 12

s = "python rocks"
print(len(s))

#--------

#  What is printed by the following statements? 
# 5

alist = [3, 67, "cat", 3.14, False]
print(len(alist))

#--------

# Assign the number of elements in lst to the variable output.

lst = ["hi", "morning", "dog", "506", "caterpillar", "balloons", 106, "yo-yo", "python", "moon", "water", "sleepy", "daffy", 45, "donald", "whiteboard", "glasses", "markers", "couches", "butterfly", "100", "magazine", "door", "picture", "window", ["Olympics", "handle"], "chair", "pages", "readings", "burger", "juggle", "craft", ["store", "poster", "board"], "laptop", "computer", "plates", "hotdog", "salad", "backpack", "zipper", "ring", "watch", "finger", "bags", "boxes", "pods", "peas", "apples", "horse", "guinea pig", "bowl", "EECS"]

output = len(lst)

#--------



#--------



#--------



#--------



#--------
