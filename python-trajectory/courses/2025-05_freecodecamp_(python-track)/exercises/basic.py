# Step 1Passed
# Variables are an essential part of Python and any programming language. A variable is a name that references or points to an object. You can declare a variable by writing the variable name on the left side of the assignment operator = and specifying the value to assign to that variable on the right side of the assignment operator:

# Example Code
# variable_name = value
# Create a variable called number and assign the value 5 to your new variable.

number = 5

# Step 2Passed
# Variables can store values of different data types. You just assigned an integer value, but if you want to represent some text, you need to assign a string. Strings are sequences of characters enclosed by single or double quotes, but you cannot start a string with a single quote and end it with a double quote or vice versa:

# Example Code
# string_1 = "I am a string"
# string_2 = 'I am also a string'
# string_3 = 'This is not valid"
# Delete your number variable and its value. Then, declare another variable called text and assign the string 'Hello World' to this variable.

text = "Hello World"



# Step 3Passed
# You can use the built-in function print() to print the output of your code on the terminal.

# Functions are reusable code blocks that you can call, or invoke, to run their code when you need them. To call a function, you just need to write a pair of parentheses next to its name. You will learn more about functions very soon.

# For now, go to a new line and add an empty call to the print() function. You should not see any output yet.

text = 'Hello World'
print()


# Step 4Passed
# An argument is an object or an expression passed to a function — added between the opening and closing parentheses — when it is called:

# Example Code
# greet = 'Hello!'
# print(greet)
# The code in the example above would print the string 'Hello!', which is the value of the variable greet passed to print() as the argument.

# Print your text variable to the screen by passing the text variable as the argument to the print() function.

text = 'Hello World'
print(text)


# Step 5Passed
# Each string character can be referenced by a numerical index. The index count starts at zero. So the first character of a string has an index of 0. For example, in the string 'Hello World', 'H' is at index 0, 'e' is at index 1, and so on.

# Each character of a string can be accessed by using bracket notation. You need to write the variable name followed by square brackets and add the index of the character between the brackets:

# Example Code
# text = 'Hello World'
# r = text[8]
# Now, instead of printing text, print just the character at index 6.

text = 'Hello World'
print(text[6])


# Step 6Passed
# You can also access string characters starting from the end of the string. The last character has an index of -1, the second to last -2 and so on.

# Now modify your existing print() call to print the last character in your string.


text = 'Hello World'
print(text[-1])


# Step 7Passed
# You can access the number of characters in a string with the built-in len() function.

# Modify your existing print() call by passing len(text) instead of text[-1].

text = 'Hello World'
print(len(text))