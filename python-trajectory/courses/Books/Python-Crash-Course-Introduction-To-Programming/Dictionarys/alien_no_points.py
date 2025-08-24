


#using get() to access values in a dictionary

# alien_0 = {'color':'green', 'speed':'slow'}
# print(alien_0['points'])


alien_0 = {'color':'green', 'speed':'slow'}

point_value = alien_0.get('points','no points value assigned')
print(point_value)

