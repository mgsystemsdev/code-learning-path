# copying a list

foods = ['pizza', 'falafel', 'carrot cake']
friends_foods = foods[:]

print('my favorite foods are:')
print(foods)

print('\nMy friend\'s favorite foods are:')
print(foods)


foods = ['pizza', 'falafel', 'carrot cake']
friends_foods = foods[:]

foods.append('canoli')
friends_foods.append('ice cream')

print('my favorite foods are:')
print(foods)

print('\nMy friend\'s favorite foods are:')
print(friends_foods)
