# ============================================================
#  File:        module2.py
#  Author:      Miguel Gonzalez Almonte
#  Created:     2025-06-01
#  Description: 
# ------------------------------------------------------------
#  Course:      Python 3 Programming Specialization (Coursera)
#  Module:      Module 2 of Class 1
#  Purpose:     
# ------------------------------------------------------------
#  Notes:
#  - 
#  - 
#  - 
# ============================================================

# ============================================================
#      6.6. The Slice Operator
# ============================================================

singers = "Peter, Paul, and Mary"
print(singers[0:5])
print(singers[7:11])
print(singers[17:21])

#--------

fruit = "banana"
print(fruit[:3])
print(fruit[3:])

# ============================================================
#      6.6.1. List Slices
# ============================================================

a_list = ['a', 'b', 'c', 'd', 'e', 'f']
print(a_list[1:3])
print(a_list[:4])
print(a_list[3:])
print(a_list[:])

# ============================================================
#      6.6.2. Tuple Slices
# ============================================================

julia = ("Julia", "Roberts", 1967, "Duplicity", 2009, "Actress", "Atlanta, Georgia")
print(julia[2])
print(julia[2:6])

print(len(julia))

julia = julia[:3] + ("Eat Pray Love", 2010) + julia[5:]
print(julia)

#--------

# What is printed by the following statements? 
# hon r

s = "python rocks"
print(s[3:8])

#--------

# What is printed by the following statements? 
# A. [ [ ], 3.14, False]

alist = [3, 67, "cat", [56, 57, "dog"], [ ], 3.14, False]
print(alist[4:])


#--------

# What is printed by the following statements?
#  3

L = [0.34, '6', 'SI106', 'Python', -2]
print(len(L[1:-1]))

#--------

# Create a new list using the 9th through 12th elements (four items in all) of new_lst and assign it to the variable sub_lst.

new_lst = ["computer", "luxurious", "basket", "crime", 0, 2.49, "institution", "slice", "sun", ["water", "air", "fire", "earth"], "games", 2.7, "code", "java", ["birthday", "celebration", 1817, "party", "cake", 5], "rain", "thunderstorm", "top down"]

sub_lst = new_lst[8:12]

# ============================================================
#      6.7. Concatenation and Repetition
# ============================================================

fruit = ["apple","orange","banana","cherry"]
print([1,2] + [3,4])
print(fruit+[6,7,8,9])

print([0] * 4)


#--------

# What is printed by the following statements? 
# [1,3,5,2,4,6]


alist = [1,3,5]
blist = [2,4,6]
print(alist + blist)


#--------

# What is printed by the following statements? 
#  [1,3,5,1,3,5,1,3,5]

alist = [1,3,5]
print(alist * 3)

# ============================================================
#      6.8.1. Count
# ============================================================

a = "I have had an apple on my desk before!"
print(a.count("e"))
print(a.count("ha"))

#--------

z = ['atoms', 4, 'neutron', 6, 'proton', 4, 'electron', 4, 'electron', 'atoms']
print(z.count("4"))
print(z.count(4))
print(z.count("a"))
print(z.count("electron"))

# ============================================================
#      6.8.2. Index
# ============================================================


music = "Pull out your music and dancing can begin"
bio = ["Metatarsal", "Metatarsal", "Fibula", [], "Tibia", "Tibia", 43, "Femur", "Occipital", "Metatarsal"]

print(music.index("m"))
print(music.index("your"))

print(bio.index("Metatarsal"))
print(bio.index([]))
print(bio.index(43))

#--------

seasons = ["winter", "spring", "summer", "fall"]

print(seasons.index("autumn"))  #Error!

#--------

# What will be stored in the variable ty below? 
# 5

qu = "wow, welcome week!"
ty = qu.index("we")

#--------

#  What will be stored in the variable ht below? 
# 2

rooms = ['bathroom', 'kitchen', 'living room', 'bedroom', 'closet', "foyer"]
ht = rooms.index("garden")

#--------

# What will be stored in the variable ht below? 
# There is an error.


rooms = ['bathroom', 'kitchen', 'living room', 'bedroom', 'closet', "foyer"]
ht = rooms.index("garden")

# ============================================================
#     6.9. Splitting and Joining Strings
# ============================================================

song = "The rain in Spain..."
wds = song.split()
print(wds)

#--------

song = "The rain in Spain..."
wds = song.split('ai')
print(wds)

#--------

wds = ["red", "blue", "green"]
glue = ';'
s = glue.join(wds)
print(s)
print(wds)

print("***".join(wds))
print("".join(wds))

#--------

# Create a new list of the 6th through 13th elements of lst (eight items in all) and assign it to the variable output.

lst = ["swimming", 2, "water bottle", 44, "lollipop", "shine", "marsh", "winter", "donkey", "rain", ["Rio", "Beijing", "London"], [1,2,3], "gold", "bronze", "silver", "mathematician", "scientist", "actor", "actress", "win", "cell phone", "leg", "running", "horse", "socket", "plug", ["Phelps", "le Clos", "Lochte"], "drink", 22, "happyfeet", "penguins"]


#--------

# Create a variable output and assign to it a list whose elements are the words in the string str1.

str1 = "OH THE PLACES YOU'LL GO"