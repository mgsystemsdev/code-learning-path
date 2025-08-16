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


# Step 8Passed
# You can see 11 printed on the terminal because 'Hello World' contains 11 characters.

# Another useful built-in function is type(), which returns the data type of a variable. Modify your print() call to print the data type of text.


text = 'Hello World'
print(type(text))


# Step 9Passed
# As you can see, the output of printing type(text) is <class 'str'>, which means that your variable is a string, indicated as str.

# Now go to a new line and create another variable called shift and assign the value 3 to this variable.

text = 'Hello World'
print(type(text))
shift = 3


# Step 10Passed
# And now print your new variable.

text = 'Hello World'
print(type(text))
shift = 3
print(shift)

# Step 11Passed
# Modify your print(shift) call to print the data type of your shift variable.



text = 'Hello World'
print(type(text))
shift = 3
print(type(shift))


# Key aspects of variable naming in Python are:

# Some words are reserved keywords (e.g. for, while, True). They have a special meaning in Python, so you cannot use them for variable names.
# Variable names cannot start with a number, and they can only contain alpha-numeric characters or underscores.
# Variable names are case sensitive, i.e. my_var is different from my_Var and MY_VAR.
# Finally, it is a common convention to write variable names using snake_case, where each space is replaced by an underscore character and the words are written in lowercase letters.
# # Remove both calls to print() and declare another variable called alphabet. Assign the string 'abcdefghijklmnopqrstuvwxyz' to this variable.

text = 'Hello World'
print()
shift = 3
print()
alphabet ='abcdefghijklmnopqrstuvwxyz'

# Step 12Passed
# Key aspects of variable naming in Python are:

# Some words are reserved keywords (e.g. for, while, True). They have a special meaning in Python, so you cannot use them for variable names.
# Variable names cannot start with a number, and they can only contain alpha-numeric characters or underscores.
# Variable names are case sensitive, i.e. my_var is different from my_Var and MY_VAR.
# Finally, it is a common convention to write variable names using snake_case, where each space is replaced by an underscore character and the words are written in lowercase letters.
# Remove both calls to print() and declare another variable called alphabet. Assign the string 'abcdefghijklmnopqrstuvwxyz' to this variable.

text = 'Hello World'
shift = 3
alphabet ='abcdefghijklmnopqrstuvwxyz'

# Step 13Passed
# You are going to use the .find() method to find the position in the alphabet of each letter in your message. A method is similar to a function, but it belongs to an object.

# Example Code
# sentence = 'My brain hurts!'
# sentence.find('r')
# Above, the .find() method is called on sentence (the string to search in), and 'r' (the character to locate) is passed as the argument. The sentence.find('r') call will return 4, which is the index of the first occurrence of 'r' in sentence.

# At the end of your code, call .find() on alphabet and pass 'z' as the argument to the method. 

text = 'Hello World'
shift = 3
alphabet = 'abcdefghijklmnopqrstuvwxyz'
alphabet.find('z')



# Step 14Passed
# The first kind of cipher you are going to build is called a Caesar cipher. Specifically, you will take each letter in your message, find its position in the alphabet, take the letter located after 3 positions in the alphabet, and replace the original letter with the new letter.

# To implement this, you will use the .find() method discussed in the previous step. Modify your existing .find() call passing it text[0] as the argument instead of 'z'.


text = 'Hello World'
shift = 3
alphabet = 'abcdefghijklmnopqrstuvwxyz'
alphabet.find(text[0])


# Step 15Passed
# The print() function gives you only an output in the console, but functions and methods can have a return value that you can use in your code.

# Now assign alphabet.find(text[0]) to a variable named index. In this way, index will store the value returned by alphabet.find(text[0]).

text = 'Hello World'
shift = 3
alphabet = 'abcdefghijklmnopqrstuvwxyz'
index = alphabet.find(text[0])



# Step 16Passed
# Next, print the index variable to the console.
text = 'Hello World'
shift = 3
alphabet = 'abcdefghijklmnopqrstuvwxyz'
index = alphabet.find(text[0])
print(index)

# Step 17Passed
# .find() returns the index of the matching character inside the string. If the character is not found, it returns -1. As you can see, the first character in text, uppercase 'H', is not found, since alphabet contains only lowercase letters.

# You can transform a string into its lowercase equivalent with the .lower() method. Add another print() call to print text.lower() and see the output.


text = 'Hello World'
shift = 3
alphabet = 'abcdefghijklmnopqrstuvwxyz'
index = alphabet.find(text[0])
print(index)
print(text.lower())

# Step 18Passed
 #  # Remove the last print() call. Then, instead of text[0], pass text[0].lower() as the argument to your .find() call and see the output.
text = 'Hello World'
shift = 3
alphabet = 'abcdefghijklmnopqrstuvwxyz'
index = alphabet.find(text[0].lower())
print(index)


# Step 19
# Declare a new variable named shifted. Use the bracket notation to access the value of alphabet at index index and assign it to your new variable.


shifted = alphabet[index]
text = 'Hello World'
shift = 3
alphabet = 'abcdefghijklmnopqrstuvwxyz'
index = alphabet.find(text[0].lower())
shifted = alphabet[index]
print(shifted)



# Step 20
# Print your shifted variable.

text = 'Hello World'
shift = 3
alphabet = 'abcdefghijklmnopqrstuvwxyz'
index = alphabet.find(text[0].lower())
print(index)
shifted = alphabet[index]
print(shifted)


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
   
                
