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
#    9.12. The Accumulator Pattern with Lists¶
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

# ============================================================
#    9.13. The Accumulator Pattern with Strings
# ============================================================

s = input("Enter some text")
ac = ""
for c in s:
    ac = ac + c + "-"

print(ac)

#--------

s = "Murphy"
ac = ""
for c in s:
    ac = c + ac

print(ac)

#--------
# Accumulate all the characters from the string in the variable str1 into a list of characters called chars.

str1 = "I love python"
# HINT: what's the accumulator? That should go here.
chars = []
for ch in str1:
    chars.append(ch)

print(chars)


#--------
# Assign an empty string to the variable output. Using the range function, write code to make it so that the variable output has 35 a s inside it (like "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"). Hint: use the accumulation pattern!
output = ""  # Step 1: Initialize the accumulator

for _ in range(35):  # Step 2: Accumulate 'a' 35 times
    output += "a"

print(output)  # Step 3: Display the result


#--------





#--------



#--------



#--------



#--------



#--------



#--------



#--------



#--------



#--------



#--------
# ============================================================
#    
# ============================================================



#--------



#--------



#--------



#--------





#--------



#--------



#--------



#--------



#--------



#--------



#--------



#--------



#--------



#--------
# ============================================================
#    
# ============================================================



#--------



#--------



#--------



#--------





#--------



#--------



#--------



#--------



#--------



#--------



#--------



#--------



#--------



#--------
# ============================================================
#    
# ============================================================



#--------



#--------



#--------



#--------





#--------



#--------



#--------



#--------



#--------



#--------



#--------



#--------



#--------



#--------
# ============================================================
#    
# ============================================================



#--------



#--------



#--------



#--------





#--------



#--------



#--------



#--------



#--------



#--------



#--------



#--------



#--------



#--------
# ============================================================
#    
# ============================================================



#--------



#--------



#--------



#--------





#--------



#--------



#--------



#--------



#--------



#--------



#--------



#--------



#--------



#--------
# ============================================================
#    
# ============================================================



#--------



#--------



#--------



#--------





#--------



#--------



#--------



#--------



#--------



#--------



#--------



#--------



#--------



#--------
# ============================================================
#    
# ============================================================



#--------



#--------



#--------



#--------





#--------



#--------



#--------



#--------



#--------



#--------



#--------



#--------



#--------



#--------
