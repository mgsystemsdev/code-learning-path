# chaging adding , and removing elements 


# modifying elements 

motorcycles = ['honda', 'yamaha', 'suzuki']
print(motorcycles)

motorcycles[0] = 'ducati'
print(motorcycles)


#---------

# Adding elements

motorcycles = ['honda', 'yamaha', 'suzuki']
print(motorcycles)

motorcycles.append('ducati')
print(motorcycles)



motorcycles = []

motorcycles.append('honda')
motorcycles.append('yamaha')
motorcycles.append('suzuki')

print(motorcycles)


#-----------

# inserting element into a list

motorcycles = ['honda', 'yamaha', 'suzuki']

motorcycles.insert(0, 'ducati')
print(motorcycles)

#-------------

# removing items of. a list



motorcycles = ['honda', 'yamaha', 'suzuki']
print(motorcycles)

del motorcycles[0]
print(motorcycles)


#---------------

# removing an item using pop()

motorcycles = ['honda', 'yamaha', 'suzuki']
print(motorcycles)

popped_motorcycle = motorcycles.pop()
print(motorcycles)
print(popped_motorcycle)


motorcycles = ['honda', 'yamaha', 'suzuki']
print(motorcycles)

last_own = motorcycles.pop()
print(f'The last motorcycle I owned was a {last_own.title()}.')

# popping items from any position 

motorcycles = ['honda', 'yamaha', 'suzuki']
print(motorcycles)

last_own = motorcycles.pop(0)
print(f'The last motorcycle I owned was a {last_own.title()}.')

# removing item by value

motorcycles = ['honda', 'yamaha', 'suzuki']
print(motorcycles)


motorcycles.remove('yamaha')
print(motorcycles)



motorcycles = ['honda', 'yamaha', 'suzuki', 'ducati']
print(motorcycles)

too_expensive = 'ducati'
motorcycles.remove(too_expensive)
print(motorcycles)
print(f'\nA {too_expensive.title()} is too expensive')

