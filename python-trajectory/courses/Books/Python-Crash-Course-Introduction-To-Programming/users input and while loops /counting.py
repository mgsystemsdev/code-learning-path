# the while loop in actions 

current_number = 1
while current_number <= 5:
    print(current_number)
    current_number += 1


prompt = "\nTell me something, and I will repeat it back to you:"
prompt += "\nEnter 'quit' to end the program. "
message = ""

while message != 'quit':
    message = input(prompt)
    if message == 'quit':
        break
    print(message)






# using  a flag 

prompt = "\nTell me something, and I will repeat it back to you:"
prompt += "\nEnter 'quit' to end the program. "

active = True
while active:
    message = input(prompt)
    
    if message == 'quit':
        active = False
    else:
        print(message)






# using continue in a loop

current_number = 0
while current_number < 10:
    current_number += 1
    if current_number % 2 == 0:
        continue
    print(current_number)


# avoiding infinite loops

x = 1
while x <= 5:
    print(x)
    x += 1

# # this loop run forever
# x= 1 while x <= 5:
#     print(x)
# To avoid an infinite loop in the provided code, you need to ensure that the loop's condition will eventually evaluate to False. This can be achieved by modifying the loop variable (x) within the loop. Here's how you can fix the code:

# Corrected Code:

# x = 1  # Initialize xwhile x <= 5:  # Loop condition    print(x)  # Print the current value of x    x += 1  # Increment x to ensure the condition becomes False
# Key Steps to Avoid Infinite Loops:
# Initialize the Loop Variable: Ensure the variable used in the condition (x in this case) is initialized before the loop starts.
# Update the Loop Variable: Modify the loop variable within the loop body to ensure progress toward the termination condition.
# Check the Condition: Write a condition that will eventually evaluate to False as the loop progresses.
# Common Practices:
# Use a clear and logical condition for the loop.
# Test the loop with different inputs to ensure it behaves as expected.
# If the loop depends on user input, provide a clear way to exit (e.g., a break statement when a specific input is received).
# By following these practices, you can prevent infinite loops and ensure your program runs as intended.