# Step 21
# As you can see from the output, 'h' is at index 7 in the alphabet string. Now you need to find the letter at index 7 plus the value of shift. For that, you can use the addition operator, +, in the same way you would use it for a mathematical addition.

# Modify your shifted variable so that it stores the value of alphabet at index index + shift.

text = 'Hello World'
shift = 3
alphabet = 'abcdefghijklmnopqrstuvwxyz'
index = alphabet.find(text[0].lower())
print(index)
shifted = alphabet[index + shift]
print(shifted)


# Step 22
# Repeating the process of locating the letter inside the alphabet and determine the shifted letter for each character in text can be tedious. Thankfully, you can simplify it using a loop.

# For now, remove all the lines of code below the declaration of the alphabet variable. 

text = 'Hello World'
shift = 3
alphabet = 'abcdefghijklmnopqrstuvwxyz'




# Step 23
# A loop allows you to systematically go through a sequence of elements and execute actions on each one.

# In this case, you'll employ a for loop. Here's how you can iterate over text:

# Example Code
# for i in text:
# for is the keyword denoting the loop type. i is a variable that sequentially takes the value of the elements in text. The statement ends with a colon, :.

# Below the line where you declared alphabet, write a for loop to iterate over text. Use i as the loop variable.

# Doing so, there is an error in the terminal. You will learn about it in the next step.
text = 'Hello World'
shift = 3
alphabet = 'abcdefghijklmnopqrstuvwxyz'
for i in text:
    print(i)
    shifted = alphabet[index + shift]
    print(shifted)


# Step 24
# The code to execute at each iteration — placed after the : — constitutes the body of the loop. This code must be indented. In Python, it is recommended to use 4 spaces per indentation level. This indented level is a code block.

# Example Code
# for i in text:
#     print(i)
# Python relies on indentation to indicate blocks of code. A colon at the end of a line is a signal that a new indented block of code will follow.

# So, when no indented block is found after the final colon, the code execution stops and an IndentationError is thrown. This code will not show the output and instead raise an IndentationError:

# Example Code
# for i in text:
# print(i)
# Give your for loop a body by adding a call to print(i). Remember to indent the loop body.
text = 'Hello World'
shift = 3
alphabet = 'abcdefghijklmnopqrstuvwxyz'

for i in text:
    print(i)



# Step 25
# The iteration variable can have any valid name, but it's convenient to give it a meaningful name.

# Rename your i variable to char.
for char in text:
    print(char)



    # Step 26
    # Inside the for loop, before printing the current character, declare a variable called index and assign the value returned by alphabet.find(char) to this variable.
    index = alphabet.find(char)
for char in text:                       
    print(char)
   

# Step 27
# Currently, the print() function is taking a single argument char, but it can take multiple arguments, separated by a comma.

# Add a second argument to print(char) so that it prints the character and its index inside the alphabet.

text = 'Hello World'
shift = 3
alphabet = 'abcdefghijklmnopqrstuvwxyz'

for char in text:
    index = alphabet.find(char)
    print(char ,index)


# Step 28
# find is again returning -1 for uppercase letters, and for the space character, too. You are going to take care of the space later on.

# For now, instead of iterating over text, change the for loop to iterate over text.lower().
text = 'Hello World'
shift = 3
alphabet = 'abcdefghijklmnopqrstuvwxyz'

for char in text.lower():
    index = alphabet.find(char)
    print(char, index)

# Step 29
# At the end of your loop body, declare a variable called new_index and assign the value of index + shift to this variable.

text = 'Hello World'
shift = 3
alphabet = 'abcdefghijklmnopqrstuvwxyz'

for char in text.lower():
    index = alphabet.find(char)
    print(char, index)
    new_index = index + shift




# Step 30
# Strings are immutable, which means they cannot be changed once created. For example, you might think that the following code changes the value of my_string into the string 'train', but this is not valid:

# Example Code
# my_string = 'brain'
# my_string[0] = 't'
# Confirm that by using the bracket notation to access the first letter in text and try to change it into a character of your choice. You will see the ouput disappear and an error appear.
text = 'Hello World'
text[0] = "h"


# Step 31Passed
# When you try to change the individual characters of a string as you did in the previous step, you get a TypeError, which occurs when an object of inappropriate type is used in your code.

# As you can see from the error message, strings do not support item assignment, because they are immutable. However, a variable can be reassigned another string:

# Example Code
# message = 'Hello World'
# message = 'Hello there!'
# Delete the text[0] line and reassign text the string 'Albatross'.
text = 'Hello World'
text = 'Albatross'


# Step 32
# As you can see, each character of the reassigned string gets printed inside the loop.

# Go back to the original string by deleting the text reassignment.

text = 'Hello World'


# Step 33
# Now you need to create a new_char variable at the end of your loop body. Set its value to alphabet[new_index].
text = 'Hello World'
shift = 3
alphabet = 'abcdefghijklmnopqrstuvwxyz'

for char in text.lower():
    index = alphabet.find(char)
    print(char, index)
    new_index = index + shift
    new_char = alphabet[new_index]


# Step 34
# Next, print new_char and see the output.
text = 'Hello World'
shift = 3
alphabet = 'abcdefghijklmnopqrstuvwxyz'

for char in text.lower():
    index = alphabet.find(char)
    print(char, index)
    new_index = index + shift
    new_char = alphabet[new_index]
    print(new_char)


    # Step 35
    # Clean the output a bit. Delete print(char, index), and turn the last print() call into print('char:', char, 'new char:', new_char).
text = 'Hello World'
shift = 3
alphabet = 'abcdefghijklmnopqrstuvwxyz'

for char in text.lower():
    index = alphabet.find(char)
    new_index = index + shift
    new_char = alphabet[new_index]
    print('char:', char, 'new char:', new_char)


# Step 36
# At the moment, the encrypted character is updated in every iteration. It would be better to store the encrypted string in a new variable. Before your for loop, declare a variable called encrypted_text and assign an empty string ('') to this variable.

text = 'Hello World'
shift = 3
alphabet = 'abcdefghijklmnopqrstuvwxyz'
encrypted_text = ""

for char in text.lower():
    index = alphabet.find(char)
    new_index = index + shift
    new_char = alphabet[new_index]
    print('char:', char, 'new char:', new_char)


# Step 37
# Now, replace new_char with encrypted_text. Also, modify the print() call into print('char:', char, 'encrypted text:', encrypted_text) to reflect this change.
# Sorry, your code does not pass. You're getting there.

# You should replace new_char with encrypted_text inside your for loop.
text = 'Hello World'
shift = 3
alphabet = 'abcdefghijklmnopqrstuvwxyz'
encrypted_text = ''

for char in text.lower():
    index = alphabet.find(char)    
    new_index = index + shift
    encrypted_text = alphabet[new_index]
    print('char:', char, 'encrypted text:', encrypted_text)


# Step 38
# Instead of assigning alphabet[new_index] to encrypted_text, assign the current value of encrypted_text plus alphabet[new_index] to this variable.


text = 'Hello World'
shift = 3
alphabet = 'abcdefghijklmnopqrstuvwxyz'
encrypted_text = ''

for char in text.lower():
    index = alphabet.find(char)    
    new_index = index + shift
    encrypted_text = encrypted_text + alphabet[new_index]
    print('char:', char, 'encrypted text:', encrypted_text)
    



# Step 39
# You can obtain the same effect of a = a + b by using the addition assignment operator:

# Example Code
# a += b
# The addition assignment operator enables you to add a value to a variable and then assign the result to that variable.

# Use the += operator to add a value and assign it at the same time to encrypted_text.

for char in text.lower():
    index = alphabet.find(char)
    new_index = index + shift
    encrypted_text += alphabet[new_index]
    print('char:', char, 'encrypted text:', encrypted_text)