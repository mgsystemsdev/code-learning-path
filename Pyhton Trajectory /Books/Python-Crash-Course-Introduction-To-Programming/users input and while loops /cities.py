
# using  break to exit a loop

promt = "\nPlease enter the name of a city you have visited:"
promt += "\n(Enter 'quit' when you are finished.) "

while True:
    city = input(promt)

    if city == 'quit':
        break
    else:
        print(f"I'd love to go to {city.title()}!")
        print("That's a great city!")
        
