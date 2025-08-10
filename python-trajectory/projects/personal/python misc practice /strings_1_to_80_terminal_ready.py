
# Drill 1
# Assign and print a name
name = "Kai"
print(name)

# Drill 2
# Assign and print another string
animal = "tiger"
print(animal)

# Drill 3
# Print two strings
food = "pizza"
drink = "cola"
print(food)
print(drink)

# Drill 4
# Create and print a short word
word = "wow"
print(word)

# Drill 5
# Print a blank line
print("")

# Drill 6
# Pair and print variables
name = "Luna"
animal = "cat"
print(name)
print(animal)

# Drill 7
# Print on two lines
print("Name:")
print(name)
print("Animal:")
print(animal)

# Drill 8
# Add third variable
color = "gray"
print(color)

# Drill 9
# Change value and print
name = "Milo"
print(name)

# Drill 10
# Print all with spacing
print(name)
print(animal)
print(color)

# Drill 11
# Join two strings
first = "hello"
second = "world"
print(first + second)

# Drill 12
# Add space manually
print(first + " " + second)

# Drill 13
# Full name
first_name = "Anna"
last_name = "Lee"
print(first_name + " " + last_name)

# Drill 14
# Sentence from parts
verb = "likes"
thing = "Python"
print("She " + verb + " " + thing)

# Drill 15
# Store full sentence
sentence = "He " + verb + " " + thing
print(sentence)

# Drill 16
# Description sentence
mood = "happy"
place = "home"
print("She is " + mood + " at " + place)

# Drill 17
# Object message
animal = "dog"
mood = "excited"
print("The " + animal + " is " + mood + ".")

# Drill 18
# Add punctuation
print("Wow" + "!")

# Drill 19
# New object sentence
object = "car"
condition = "new"
print("The " + object + " is " + condition)

# Drill 20
# Change value and print
mood = "calm"
print("She is " + mood + " at " + place)

# Drill 21
# Length of string
word = "banana"
print(len(word))

# Drill 22
# First character
print(word[0])

# Drill 23
# Last character
print(word[-1])

# Drill 24
# Length + index
print(word[len(word)-1])

# Drill 25
# Try more indexes
print(word[1])
print(word[2])

# Drill 26
# Slice beginning
print(word[0:3])

# Drill 27
# Slice rest
print(word[2:])

# Drill 28
# Slice negative
print(word[-3:])

# Drill 29
# Middle slice
print(word[1:4])

# Drill 30
# Slice and store
mid = word[1:5]
print(mid)

# Drill 31
# Uppercase
text = "python"
print(text.upper())

# Drill 32
# Lowercase
text = "HELLO"
print(text.lower())

# Drill 33
# Title case
book = "gone with the wind"
print(book.title())

# Drill 34
# Chain method
print("TeXT".lower().count("t"))

# Drill 35
# Mix method and join
print("cool".upper() + "!")

# Drill 36
# Strip spaces
raw = "  hello  "
print(raw.strip())

# Drill 37
# Replace letter
print("banana".replace("a", "o"))

# Drill 38
# Count letter
print("banana".count("a"))

# Drill 39
# Strip tabs/newlines
messy = "
	banana	
"
print(messy.strip())

# Drill 40
# Replace word
line = "I like cats"
print(line.replace("cats", "dogs"))

# Drill 41
# Find letter
print("banana".find("n"))

# Drill 42
# Starts with
print("hello world".startswith("hello"))

# Drill 43
# Ends with
print("myfile.txt".endswith(".txt"))

# Drill 44
# Find in sentence
text = "Where is the cat?"
print(text.find("cat"))

# Drill 45
# Find and if
if "cat" in text:
    print("Found cat")

# Drill 46
# f-string simple
name = "Kai"
print(f"Hello {name}")

# Drill 47
# f-string with 3 variables
a = "apples"
b = "bananas"
c = "cherries"
print(f"I bought {a}, {b}, and {c}")

# Drill 48
# f-string with number
weight = 70
print(f"You weigh {weight} kg")

# Drill 49
# f-string with method
msg = "great"
print(f"This is {msg.upper()}!")

# Drill 50
# f-string sentence
tool = "hammer"
print(f"The tool is a {tool}")

# Drill 51
# .format() simple
print("I like {}".format("pizza"))

# Drill 52
# Format with 2
lang = "Python"
fun = "fun"
print("Learning {} is really {}.".format(lang, fun))

# Drill 53
# Reorder
print("{1} comes before {0}".format("b", "a"))

# Drill 54
# Format + method
word = "hello"
print("Your word is: {}".format(word.upper()))

# Drill 55
# Format number and word
age = 25
print("You are {} years old.".format(age))

# Drill 56
# Loop rebuild
word = "code"
output = ""
for letter in word:
    output += letter
print(output)

# Drill 57
# Add dash after each
output = ""
for letter in word:
    output += letter + "-"
print(output)

# Drill 58
# Remove a letter
word = "banana"
no_a = ""
for letter in word:
    if letter != "a":
        no_a += letter
print(no_a)

# Drill 59
# Only uppercase
msg = "The Sky Is Blue"
shout = ""
for char in msg:
    if char.isupper():
        shout += char
print(shout)

# Drill 60
# Double letters
text = "fun"
doubled = ""
for letter in text:
    doubled += letter * 2
print(doubled)

# Drill 61
# Add space after letters
text = "code"
spaced = ""
for letter in text:
    spaced += letter + " "
print(spaced)

# Drill 62
# Add index
text = "cat"
result = ""
for i, char in enumerate(text):
    result += f"{i}:{char} "
print(result)

# Drill 63
# Count letter manually
word = "apple"
count = 0
for char in word:
    if char == "p":
        count += 1
print(count)

# Drill 64
# Reverse a word
word = "code"
rev = ""
for char in word:
    rev = char + rev
print(rev)

# Drill 65
# Remove punctuation
sentence = "I love Python!"
cleaned = ""
for char in sentence:
    if char not in "!":
        cleaned += char
print(cleaned)

# Drill 66
# Check for substring
sentence = "I love programming."
if "love" in sentence:
    print("Found it!")

# Drill 67
# Check for not in
message = "The sky is blue."
if "green" not in message:
    print("Not found.")

# Drill 68
# Case-sensitive check
word = "Python"
if "python" in word:
    print("yes")
else:
    print("no")

# Drill 69
# Lower before checking
phrase = "Coding Is Fun"
if "coding" in phrase.lower():
    print("Match found")

# Drill 70
# Word in text
text = "apple banana cherry"
if "banana" in text:
    print("Fruit found!")

# Drill 71
# Count words
line = "hello hello hello"
count = line.count("hello")
print(count)

# Drill 72
# Starts with
name = "Samurai Jack"
if name.startswith("Samurai"):
    print("Starts correctly")

# Drill 73
# Ends with
filename = "report.txt"
if filename.endswith(".txt"):
    print("Text file detected")

# Drill 74
# Count with loop
text = "apple banana apple grape apple"
count = 0
for word in text.split():
    if word == "apple":
        count += 1
print(count)

# Drill 75
# Count starts with
sentence = "I saw a dog and a dolphin and a dragon."
d_words = 0
for word in sentence.split():
    if word.startswith("d"):
        d_words += 1
print(d_words)
