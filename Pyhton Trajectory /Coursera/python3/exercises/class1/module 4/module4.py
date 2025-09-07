# ============================================================
#  File:        module4.py
#  Author:      Miguel Gonzalez Almonte
#  Created:     2025-06-01
#  Description: 
# ------------------------------------------------------------
#  Course:      Python 3 Programming Specialization (Coursera)
#  Module:      Module 4 of Class 1
#  Purpose:     
# ------------------------------------------------------------
#  Notes:
#  - 
#  - 
#  - 
# ============================================================


# ============================================================
#      9.2.1. Lists are Mutable
# ============================================================

fruit = ["banana", "apple", "cherry"]
print(fruit)

fruit[0] = "pear"
fruit[-1] = "orange"
print(fruit)

#--------

alist = ['a', 'b', 'c', 'd', 'e', 'f']
alist[1:3] = ['x', 'y']
print(alist)

#--------

alist = ['a', 'd', 'f']
alist[1:1] = ['b', 'c']
print(alist)
alist[4:4] = ['e']
print(alist)

# ============================================================
#   9.2.2. Strings are Immutable   
# ============================================================

greeting = "Hello, world!"
greeting[0] = 'J'            # ERROR!
print(greeting)

#--------

greeting = "Hello, world!"
newGreeting = 'J' + greeting[1:]
print(newGreeting)
print(greeting)          # same as it was


#--------

phrase = "many moons"
phrase_expanded = phrase + " and many stars"
phrase_larger = phrase_expanded + " litter"
phrase_complete = "M" + phrase_larger[1:] + " the night sky."
excited_phrase_complete = phrase_complete[:-1] + "!"


# ============================================================
#      9.3. List Element Deletion
# ============================================================


a = ['one', 'two', 'three']
del a[1]
print(a)

alist = ['a', 'b', 'c', 'd', 'e', 'f']
del alist[1:5]
print(alist)

# ============================================================
#      9.4. Objects and References
# ============================================================

a = "banana"
b = "banana"

print(a is b)

#--------

a = "banana"
b = "banana"

print(id(a))
print(id(b))

#--------

a = [81,82,83]
b = [81,82,83]

print(a is b)

print(a == b)

print(id(a))
print(id(b))

# ============================================================
#      9.5. Aliasing
# ============================================================

a = [81, 82, 83]
b = a
print(a is b)

#--------

a = [81,82,83]
b = [81,82,83]
print(a is b)

b = a
print(a == b)
print(a is b)

b[0] = 5
print(a)

# ============================================================
#      9.6. Cloning Lists
# ============================================================

a = [81,82,83]

b = a[:]       # make a clone using slice
print(a == b)
print(a is b)

b[0] = 5

print(a)
print(b)

# ============================================================
#     course_1_assessment_8 
# ============================================================

# Could aliasing cause potential confusion in this problem? 
# yes

b = ['q', 'u', 'i']
z = b
b[1] = 'i'
z.remove('i')
print(z)

#--------

# Could aliasing cause potential confusion in this problem?

sent = "Holidays can be a fun time when you have good company!"
phrase = sent
phrase = phrase + " Holidays can also be fun on your own!"



# ============================================================
#    9.7.1. List Methods
# ============================================================

# Be sure to experiment with these methods to gain a better understanding of what they do.

# | **Method** | **Parameters**   | **Result**    | **Description**                                      |
# |------------|------------------|---------------|------------------------------------------------------|
# | `append`   | `item`           | mutator       | Adds a new item to the end of a list                |
# | `insert`   | `position, item` | mutator       | Inserts a new item at the position given            |
# | `pop`      | *none*           | hybrid        | Removes and returns the last item                   |
# | `pop`      | `position`       | hybrid        | Removes and returns the item at position            |
# | `sort`     | *none*           | mutator       | Modifies a list to be sorted                        |
# | `reverse`  | *none*           | mutator       | Modifies a list to be in reverse order              |
# | `index`    | `item`           | return idx    | Returns the position of first occurrence of item    |
# | `count`    | `item`           | return ct     | Returns the number of occurrences of item           |
# | `remove`   | `item`           | mutator       | Removes the first occurrence of item                |

#--------

mylist = []
mylist.append(5)
mylist.append(27)
mylist.append(3)
mylist.append(12)
print(mylist)

mylist = mylist.sort()   #probably an error
print(mylist)



# ============================================================
#    9.8. Append versus Concatenate
# ============================================================

origlist = [45,32,88]

origlist.append("cat")
print(origlist)

#--------

origlist = [45,32,88]
print("origlist:", origlist)
print("the identifier:", id(origlist))             #id of the list before changes
newlist = origlist + ['cat']
print("newlist:", newlist)
print("the identifier:", id(newlist))              #id of the list after concatentation
origlist.append('cat')
print("origlist:", origlist)
print("the identifier:", id(origlist))             #id of the list after append is used

#--------

st = "Warmth"
a = []
print(st)

#--------

st = "Warmth"
a = []
b = a + [st[0]]
c = b + [st[1]]
d = c + [st[2]]
e = d + [st[3]]
f = e + [st[4]]
g = f + [st[5]]
print(g)


#--------

st = "Warmth"
a = []
a.append(st[0])
a.append(st[1])
a.append(st[2])
a.append(st[3])
a.append(st[4])
a.append(st[5])
print(a)

# ============================================================
#    9.9. Non-mutating Methods on Strings
# ============================================================

ss = "Hello, World"
print(ss.upper())

tt = ss.lower()
print(tt)
print(ss)

#--------

ss = "    Hello, World    "

els = ss.count("l")
print(els)

print("***"+ss.strip()+"***")

news = ss.replace("o", "***")
print(news)

#--------

food = "banana bread"
print(food.upper())

# ============================================================
#    9.10. String Format Method
# ============================================================

name = "Rodney Dangerfield"
score = -1  # No respect!
print("Hello " + name + ". Your score is " + str(score))


#--------

scores = [("Rodney Dangerfield", -1), ("Marlon Brando", 1), ("You", 100)]
for person in scores:
    name = person[0]
    score = person[1]
    print("Hello " + name + ". Your score is " + str(score))


#--------

person = input('Your name: ')
greeting = 'Hello {}!'.format(person)
print(greeting)


#--------

person = input('Enter your name: ')
print('Hello {}!'.format(person))

#--------

origPrice = float(input('Enter the original price: $'))
discount = float(input('Enter discount percentage: '))
newPrice = (1 - discount/100)*origPrice
calculation = '${} discounted by {}% is ${}.'.format(origPrice, discount, newPrice)
print(calculation)

#--------

origPrice = float(input('Enter the original price: $'))
discount = float(input('Enter discount percentage: '))
newPrice = (1 - discount/100)*origPrice
calculation = '${:.2f} discounted by {}% is ${:.2f}.'.format(origPrice, discount, newPrice)
print(calculation)

#--------

name = "Sally"
greeting = "Nice to meet you"

# 1. Correct order — matches placeholders
s = "Hello, {}. {}."
print(s.format(name, greeting))  # Output: Hello, Sally. Nice to meet you.

# 2. Reversed order — still works, different meaning
print(s.format(greeting, name))  # Output: Hello, Nice to meet you. Sally.

# 3. Mismatched argument count — not enough arguments
print(s.format(name))  # Output: Hello, Sally. {}.

# 4. Named placeholders — more explicit and safer
t = "Hello, {name}. {greeting}."
print(t.format(name="Sally", greeting="Nice to meet you"))  # Output: Hello, Sally. Nice to meet you.

# 5. Precision formatting — rounding with format specifier
pi = 3.1415926535
print("Rounded to 2 decimal places: {:.2f}".format(pi))  # Output: Rounded to 2 decimal places: 3.14

# 6. Precision formatting — change the precision
print("Rounded to 4 decimal places: {:.4f}".format(pi))  # Output: Rounded to 4 decimal places: 3.1416


# ============================================================
#    9.11. f-Strings
# ============================================================

name = "Rodney Dangerfield"
score = -1
print("Hello {}. Your score is {}.".format(name, score))
print(f"Hello {name}. Your score is {score}.")

#--------

first_name = "Peter"
last_name = "Huang"
score = 96.75
print(f"Hello {'Peter' + ' ' + 'Huang'}. Your score is {90 + 6.75}.")

#--------

first_name = "Peter"
last_name = "Huang"
score = 96.75
print(f"Hello {first_name} {last_name}. Your score is {score}.")

#--------

first_name = "Peter"
last_name = "Huang"
score = 96.75
print(f"Hello {first_name} {last_name}. Your score is {max(score, 60)}.")


#--------

first_name = "Peter"
last_name = "Huang"
score = 96.75
print(f"Hello {first_name} {last_name}. Your score is {score:.1f}.")
print(f"Hello {first_name} {last_name}. Your score is {max(score, 60):.1f}.")


#--------

first_name = "Peter"
last_name = "Huang"
score = 96.75
print(f"Hello {first_name + " " + last_name}. Your score is {score}.")


#--------

first_name = "Peter"
last_name = "Huang"
score = 96.75
print("Hello {}. Your score is {}.".format(first_name + " " + last_name, score))


#--------


print("{} {}".format("{I need braces.}", "{I also need braces.}"))

# ============================================================
#    course_1_assessment_9
# ============================================================


# Write code to add ‘horseback riding’ to the third position (i.e., right before volleyball) in the list sports.

sports = ['cricket', 'football', 'volleyball', 'baseball', 'softball', 'track and field', 'curling', 'ping pong', 'hockey']

sports = ['cricket', 'football', 'volleyball', 'baseball', 'softball', 'track and field', 'curling', 'ping pong', 'hockey']
sports.insert(2, 'horseback riding')
print(sports)


#--------

# Write code to take ‘London’ out of the list trav_dest.

trav_dest = ['Beirut', 'Milan', 'Pittsburgh', 'Buenos Aires', 'Nairobi', 'Kathmandu', 'Osaka', 'London', 'Melbourne']

trav_dest.remove('London')
print(trav_dest)

#--------

trav_dest = ['Beirut', 'Milan', 'Pittsburgh', 'Buenos Aires', 'Nairobi', 'Kathmandu', 'Osaka', 'Melbourne']

trav_dest.append('Guadalajara')
print(trav_dest)

# ============================================================
#    9.12. The Accumulator Pattern with Lists
# ============================================================


nums = [3, 5, 8]
accum = []
for w in nums:
    x = w**2
    accum.append(x)
print(accum)


#--------

# For each word in the list verbs, add an -ing ending. Save this new list in a new list, ing.

verbs = ["kayak", "cry", "walk", "eat", "drink", "fly"]
ing = [verb + "ing" for verb in verbs]
print(ing)

#--------

# Given the list of numbers, numbs, create a new list of those same numbers increased by 5. Save this new list to the variable newlist.

numbs = [5, 10, 15, 20, 25]
newlist = [num + 5 for num in numbs]
print(newlist)

#--------

# Given the list of numbers, numbs, modifiy the list numbs so that each of the original numbers are increased by 5. Note this is not an accumulator pattern problem, but its a good review.

numbs = [5, 10, 15, 20, 25]

for i in range(len(numbs)):
    numbs[i] += 5

print(numbs)

#--------

# For each number in lst_nums, multiply that number by 2 and append it to a new list called larger_nums.

lst_nums = [4, 29, 5.3, 10, 2, 1817, 1967, 9, 31.32]
larger_nums = []
for num in lst_nums:
    larger_nums.append(num * 2)

print(larger_nums)


