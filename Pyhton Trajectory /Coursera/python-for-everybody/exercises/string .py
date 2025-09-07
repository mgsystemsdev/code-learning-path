#atomic strings

greting = "hello , world "
print (greting)

print("")

names = "kai"
print (names)

print("")

color = "neon pink"
print(color)

print("")


mood = "focus or curious"
print (mood)

print("")

animal = "wolf"
print  (animal)


#concanation basics

print("")

first_name = "miguel"
last_name = "gonzalez"
full_name = first_name + " " + last_name
print(full_name)

print("")

day = "Monday"
weather = "sunny"
message = "Today is " + day + " and it is " + weather + "."
print(message)

print()


fruit = "grapes"
color = "purple"
message = "the" + " " + fruit + " " + "is" + " " + color
print (message)

print()

language = "python"
activity = "practice"
duration = "daily"
message = language + " " + "should be " + " " +activity + " " + duration

print(message)

print()

animal = "dog"
name = "luna"
years = "3"
message = "my" +" " + animal + " " + name + " " + "is" +" "+ years +" "+"years"+" "+ "old"
print(message)
print()

##Length & Index Acces

print()

word = "banana"
print (len(word))
print (word[0])

print()

animal = "tiger"
print(len(animal))
print (animal[-4])


city = "london"
print(city[0])    
print(city[-2])   

movie = "Inception"
print(len(movie))        
print(movie[4])      

print()

message = "I love strings"
print(len(message))       
print(message[0])        
print(message[-1])       

# index slicing 

phrase = "coding is fun"
print(phrase[0:6])

country = "argentina"
print("\n" ,country[0:3])

language = "portugues"
print ("\n",language[3:])

tool = "hammer"
print("\n" ,tool[-3:])

planet = "saturn"
print("\n" ,planet[1:4])


#Basic Methods I

tittle = "hello python "
print(tittle.upper())

mood = "TIRED"
print(mood.lower())


book = "the great escape"
print (book.title())

shout = "this is CoOL"
print (shout.lower())
print (shout.upper())

qoute = "be kind to others"
print(qoute.title())
print  (qoute.upper())


# Basic methods 

raw_text = "   hello world   "
cleaned = raw_text.strip()
print(cleaned)

line = "apples are good"
new_line = line.replace("good", "great")
print(new_line)

sentece = "fun is fun when fun is shared"
print (sentece.count("fun"))

qoute = "This is not what I expected"
print (qoute.replace("not", "definitely"))

line = "   okay okay   "
print(line.strip()) 
print(line.count("ok"))



# search and positioning

email = "contact@example.com"
position = email.find("@")
print(position)


text = "learning to code is cool and coding is fun"
last = text.rfind("is")
print(last)

quote = "Never say never"
print("never" in quote)

sentence = "A panda ran across the yard"
first_a = sentence.find("a")
last_a = sentence.rfind("a")
print(first_a)
print(last_a)

message = "yes or no, yes is better"
first_yes = message.find("yes")
last_yes = message.rfind("yes")
print(first_yes)
print(last_yes)

#Looping Through Strings 
word = "code"
for letter in word:
    print(letter)


animal = "zebra"
for letter in animal:
    print(letter + "-")

phrase = "loop it"
for letter in phrase:
    if letter in "aeiou":
        print(letter)
        
phrase = "loop it"
for letter in phrase:
    if letter in "aeiou":
        print(letter)
        
text = "Python is powerful"
for index, char in enumerate(text):
    print(index, char)
    
# Multi-line Strings
    
poem = """Roses are red
Violets are blue
Strings in Python
Are fun to do"""

print(poem)

quote_block = """Talk is cheap. Show me the code.
– Linus Torvalds"""

print(quote_block)

letter = """Dear friend,
Hope you're doing well.
See you soon!
"""

print(letter)

menu = """Burger
Fries
Shake"""

print(menu)

instructions = """Step 1: Open the box
Step 2: Plug it in
Step 3: Press the power button"""

print(instructions)



# comparison strings

word1 = "apple"
word2 = "banana"
comparison = word1 == word2
print(comparison)

a = "Zebra"
b = "antelope"
comp = a < b 
comp2 = a == b
print(comp)
print(comp2)

x = "dog"  
y = "Dog"
comx = x == y
comp = x > y
print(comx)
print(comp)


first = "grape"
second = "grapefruit"

compari1 = first < second

compari2 = first == second

print(compari1)
print(compari2)


name1 = "anna"
name2 = "Anna"

print(name1 != name2)   # True — case-sensitive
print(name1 < name2)    # False — lowercase "a" comes after uppercase "A"


# format strings

lang = "Python"
level = "fun"
print("Learning {} is really {}.".format(lang, level))

first = "Kai"
last = "Wren"
print("my name is {} {}".format(first ,last))

fruit = "mango"
color = "yellow"

print("the {} is {}".format(fruit ,color))

name = "Luna"
pet = "cat"
age = "5"


print("my {} {} is a {} years old ".format(name,pet ,age))

first = "Maria"
activity = "coding"
duration = "every day"

print("{} practice {} {}".format(first , activity , duration))

emotion = "happy"
reason = "finished the project"

print("i feel {} because i {} ".format(emotion,reason))
adjective = "bright"
color = "blue"
object = "sky"

sentence = "The {} {} {} is beautiful.".format(adjective, color, object)
print(sentence)


name = "Leo"
age = "25"
job = "developer"
city = "Barcelona"

sentence = "{} is a {}-year-old {} living in {}.".format(name, age, job, city)
print(sentence)
