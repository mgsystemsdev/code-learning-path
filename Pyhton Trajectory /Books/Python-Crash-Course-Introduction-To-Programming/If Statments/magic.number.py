

# numerical comparison 
 
answer = 17
if answer != 42:
    print("That is not the correct answer. Please try again.")

age = 21
if age < 21:
    print("You are not old enough to enter.")
elif age == 21:
    print("You just reached the age to enter.")
else:
    print("You are old enough to enter.")


#----------------------

# checking multiple condition

age_0 = 22
age_1 = 18

# Check if both ages are at least 21 and print the result
print(age_0 >= 21 and age_1 >= 21)

age = 19
if age < 21:
    print("You are not old enough to enter.")
else:
    print("You are old enough to enter.")


#----------------------

# numerical comparisons

age = 18
print(age == 18)


age = 19
print(age < 21)

print(age <= 21)

print(age > 21)

print(age >= 21)

#--------------------

#checking weather a value is in a list

request_topping = ['mushroom', 'onions', 'pineapple']

print('mushroom' in request_topping)
print('peperoni' in request_topping)


