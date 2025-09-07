text = 'Hello World'
alphabet = 'abcdefghijklmnopqrstuvwxyz'


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