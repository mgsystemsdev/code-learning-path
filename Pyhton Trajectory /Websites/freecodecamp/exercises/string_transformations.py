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