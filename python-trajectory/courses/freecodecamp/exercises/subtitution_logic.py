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



# Step 40
# Comparison operators allow you to compare two objects based on their values. You can use a comparison operator by placing it between the objects you want to compare. They return a Boolean value — namely True or False — depending on the truthfulness of the expression.

# Python has the following comparison operators:

# Operator	Meaning
# ==	Equal
# !=	Not equal
# >	Greater than
# <	Less than
# >=	Greater than or equal to
# <=	Less than or equal to
# At the beginning of your loop body, print the result of comparing char with a space (' '). Use the equality operator == for that.
text = 'Hello World'
shift = 3
alphabet = 'abcdefghijklmnopqrstuvwxyz'
encrypted_text = ''

for char in text.lower():
    print(char == ' ')
    index = alphabet.find(char)
    new_index = index + shift
    encrypted_text += alphabet[new_index]
    print('char:', char, 'encrypted text:', encrypted_text)



# Step 41
# Currently, spaces get encrypted as 'c'. To maintain the original spacing in the plain message, you'll require a conditional if statement. This is composed of the if keyword, a condition, and a colon :.

# Example Code
# if x != 0:
#     print(x)
# In the example above, the condition of the if statement is x != 0. The code print(x), inside the if statement body, runs only when the condition evaluates to True (in this example, meaning that x is different from zero).

# At the top of your for loop, replace print(char == ' ') with an if statement. The condition of this if statement should evaluate to True if char is an empty space and False otherwise. Inside the if body, print the string 'space!'. Remember to indent this line.

text = 'Hello World'
shift = 3
alphabet = 'abcdefghijklmnopqrstuvwxyz'
encrypted_text = ''

for char in text.lower():
    if char == ' ':
        print('space!')
    index = alphabet.find(char)
    new_index = index + shift
    encrypted_text += alphabet[new_index]
    print('char:', char, 'encrypted text:', encrypted_text)


# Step 42
# Now, instead of printing 'space!', use the addition assignment operator to add the space (currently stored in char) to the current value of encrypted_text.
text = 'Hello World'
shift = 3
alphabet = 'abcdefghijklmnopqrstuvwxyz'
encrypted_text = ''

for char in text.lower():
    if char == ' ':
        encrypted_text += char
    index = alphabet.find(char)
    new_index = index + shift
    encrypted_text += alphabet[new_index]
    print('char:', char, 'encrypted text:', encrypted_text)


# Step 43
# A conditional statement can also have an else clause. This clause can be added to the end of an if statement to execute alternative code if the condition of the if statement is false:

# Example Code
# if x != 0:
#     print(x)
# else:
#     print('x = 0')
# As you can see in your output, when the loop iterations reach the space, a space is added to the encrypted string. Then the code outside the if block executes and a c is added to the encrypted string.

# To fix it, add an else clause after encrypted_text += char and indent all the subsequent lines of code except the print() call.

text = 'Hello World'
shift = 3
alphabet = 'abcdefghijklmnopqrstuvwxyz'
encrypted_text = ''

for char in text.lower():
    if char == ' ':
        encrypted_text += char
    else:
        index = alphabet.find(char)
        new_index = index + shift
        encrypted_text += alphabet[new_index]
    print('char:', char, 'encrypted text:', encrypted_text)

# Step 44
# Try to assign the string 'Hello Zaira' to your text variable and see what happens in the terminal.

# You'll see a string index out of range exception. Don't worry, you'll figure out how to fix it soon!

text = 'Hello Zaira'
shift = 3
alphabet = 'abcdefghijklmnopqrstuvwxyz'
encrypted_text = ''

for char in text.lower():
    if char == ' ':
        encrypted_text += char
    else:
        index = alphabet.find(char)
        new_index = index + shift
        encrypted_text += alphabet[new_index]
    print('char:', char, 'encrypted text:', encrypted_text)


# Step 45
# When the loop reaches the letter Z, the sum index + shift exceeds the last index of the string alphabet. Therefore, alphabet[new_index] is trying to use an invalid index, which causes an IndexError to be thrown.

# You can notice that the output in the terminal stops at the space immediately before the Z, the last print before the error is thrown.

# In this case, the modulo operator (%) can be used to return the remainder of the division between two numbers. For example: 5 % 2 is equal to 1, because 5 divided by 2 has a quotient of 2 and a remainder of 1.

# Surround index + shift with parentheses, and modulo the expression with 26, which is the alphabet length.



# Step 46
# If you wish to incorporate additional characters into the alphabet string, such as digits or special characters, you'll find it's necessary to manually modify the right operand of the modulo operation.

# Replace 26 with len(alphabet) to avoid this issue.

text = 'Hello Zaira'
shift = 3
alphabet = 'abcdefghijklmnopqrstuvwxyz'
encrypted_text = ''

for char in text.lower():
    if char == ' ':
        encrypted_text += char
    else:
        index = alphabet.find(char)
        new_index = (index + shift) % len(alphabet)
        encrypted_text += alphabet[new_index]
    print('char:', char, 'encrypted text:', encrypted_text)




# Step 47
# Next, modify your print() call to print 'encrypted text:', encrypted_text and put it outside the for loop, so that the encrypted string is printed one time.
text = 'Hello Zaira'
shift = 3
alphabet = 'abcdefghijklmnopqrstuvwxyz'
encrypted_text = ''

for char in text.lower():
    if char == ' ':
        encrypted_text += char
    else:
        index = alphabet.find(char)
        new_index = (index + shift) % len(alphabet)
        encrypted_text += alphabet[new_index]
print('encrypted text:', encrypted_text)

# Step 48
# Right before the print call, add another one and pass 'plain text:', text as the arguments to print(). Use the same indentation.

text = 'Hello Zaira'
shift = 3
alphabet = 'abcdefghijklmnopqrstuvwxyz'
encrypted_text = ''

for char in text.lower():
    if char == ' ':
        encrypted_text += char
    else:
        index = alphabet.find(char)
        new_index = (index + shift) % len(alphabet)
        encrypted_text += alphabet[new_index]
print('plain text:',text)
print('encrypted text:', encrypted_text)