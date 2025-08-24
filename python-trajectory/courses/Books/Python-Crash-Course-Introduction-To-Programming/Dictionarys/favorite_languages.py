

# a dictionary of similar objects 

favorites_languages = {
    'jen': 'python',
    'sarah': 'c',
    'edward': 'ruby',
    'phil': 'python',
}


language = favorites_languages['sarah'].title()
print(f"Sarah's favorite language is {language}.")





#looping thorught  all keys in dictionary 
for name, language in favorites_languages.items():
    print(f"{name.title()}'s favorite language is {language.title()}.")

for name in favorites_languages.keys():
    print(name.title())



friends = ['phil', 'sarah']
for name in favorites_languages.keys():
    print(f"Hi {name.title()}.")

    if name in friends:
        language = favorites_languages[name].title()
        print(f"\t{name.title()}, I see you love  {language}.")



if 'erin' not in favorites_languages.keys():
    print("Erin, please take our poll!")




#looping through dictionary in particular oder


for name in sorted(favorites_languages.keys()):
    print(f"{name.title()},thank you for taking the poll")





# looping through all values in a dictionary

favorites_languages = {
    'jen': ['python', 'ruby'],
    'sarah': ['c'],
    'edward': ['ruby', 'go'],
    'phil': ['python', 'haskell'],
}
 

for name,language in favorites_languages.items():
    print(f"\n{name.title()}'s favorite languages are ")
    for language in language:
        print(f"\t{language.title()}")