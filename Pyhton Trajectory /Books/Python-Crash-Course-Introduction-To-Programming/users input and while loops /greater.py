


#writing clear prompts

name = input("Please enter your name: ")
print(f"\nHello, {name.title()}!")




prompt = "if you tell me who you are ,we can personalize the messages you see"
prompt += "\nWhat is your first name? "

name = input(prompt)
print(f"\nHello, {name.title()}!")




# using int() to accept numerical input

age = input("How old are you? ")
age =int(age)
print(age)
