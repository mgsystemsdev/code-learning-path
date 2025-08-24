
# a simple dictionary 

alien_0 = {'color': 'green', 'points': 5}
alien_x = {'color': 'green', 'points': 5}
alien_1 = {'color': 'yellow', 'points': 10}
alien_2 = {'color': 'red', 'points': 15}

print(alien_0['color'])
print(alien_0['points'])



# working with dictionaries 

alien_0 = {'color': 'green', 'points': 5}

alien_0 = {'color': 'green'}


# Accesing  value in a dictionary
alien_0 = {'color': 'green'}
print(alien_0['color'])


alien_0 = {'color': 'green', 'points': 5}

new_points = alien_0['points']
print(f"you just earn {new_points} points!")


# Adding new key-value pairs to a dictionary


alien_0 = {'color': 'green', 'points': 5}
print(alien_0)



alien_0['x_position'] = 0
alien_0['y_position'] = 25
print(alien_0)



# starting with an empty dictionary

alien_0 = {}

alien_0['color'] = 'green'
alien_0['points'] = 5
print(alien_0)

# modifyng  values  in dictionary


alien_0 = {'color': 'green'}
print(f"The alien is {alien_0['color']}.")

alien_0['color'] = 'yellow'
print(f"The alien is now {alien_0['color']}.")



# Modifying values in a dictionary

alien_0 = {'x_position': 0, 'y_position': 25, 'speed': 'fast'}
print(f"original position:{alien_0['x_position']},")

if alien_0['speed'] == 'slow':
    x_increment = 1
elif alien_0['speed'] == 'medium':
    x_increment = 2
else:
    x_increment = 3

alien_0['x_position'] = alien_0['x_position'] + x_increment

print(f"new position: {alien_0['x_position']},")


# removing keys values


alien_0 = {'color': 'green', 'points': 5}
print(alien_0)
del alien_0['points']
print(alien_0)


# a list of dictionaries

aliens = [alien_x, alien_1, alien_2]

for alien in aliens:
    print(alien)



aliens = []

for alien_number in range(30):
    new_alien = {'color': 'green', 'points': 5, 'speed': 'slow'}
    aliens.append(new_alien)

for alien in aliens[:20]:
    print(alien)

print("...")



print(f"Total number of aliens :{len(aliens)}")





aliens = []

for alien_number in range(30):
    new_alien = {'color': 'green', 'points': 5, 'speed': 'slow'}
    aliens.append(new_alien)

for alien in aliens[:3]:
    if alien['color'] == 'green':
        alien['color'] = 'yellow'
        alien['points'] = 10
        alien['speed'] = 'medium'
    

for alien in aliens[:10]:
    print(alien)
print("...")

aliens = []

for alien_number in range(30):
    new_alien = {'color': 'green', 'points': 5, 'speed': 'slow'}
    aliens.append(new_alien)

for alien in aliens[:4]:
    if alien['color'] == 'green':
        alien['color'] = 'yellow'
        alien['points'] = 10
        alien['speed'] = 'medium'

for alien in aliens[:4]:
    if alien['color'] == 'yellow':
        alien['color'] = 'red'
        alien['speed'] = 'fast'
        alien['points'] = 15

for alien in aliens[:15]:
    print(alien)
print("...")



