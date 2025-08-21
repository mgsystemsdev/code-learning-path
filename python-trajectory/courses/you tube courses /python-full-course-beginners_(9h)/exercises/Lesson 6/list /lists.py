# === Python Collections: Lists and Tuples - Learning Demo ===
# This script explores how to work with lists and tuples in Python using real examples

# --- 📦 LIST CREATION ---

user = ['miguel', 'erika', 'logan']  # A list of strings (names)
data = ['luis', 43, True]           # A mixed list: string, int, boolean
empty = []                          # An empty list

# --- 🔍 LIST INDEXING & SLICING ---

# Accessing list items by index (uncomment to try)
# print("\n", user[0], "\n")        # First item
# print("\n", user[-2], "\n")       # Second-to-last item
# print("\n", user.index('logan'), "\n")  # Get index of 'logan'

# List slicing
# print("\n", user[0:2], "\n")      # First two elements
# print("\n", user[1:2], "\n")      # Just element at index 1
# print(user[-3:-1])                # From start to one-before-last

# --- 📏 LENGTH & MEMBERSHIP ---

# print('\n', len(data), '\n')      # Get number of items in list
# print("\n", 'miguel' in empty, "\n")  # Check if 'miguel' is in empty list (False)

# --- 🧰 ADDING TO LISTS ---

user.append('luis')                # Adds 'luis' to the end of the list
user += ['jason']                  # Adds 'jason' to the end (like append)

print(user)                        # Show current list

user.extend(['robert', 'jimmy'])   # Add multiple elements at once
print('\n', user, '\n')

user.insert(5, 'Bob')              # Inserts 'Bob' at index 5 (shifts others)
print('\n', user, '\n')

user[2:2] = ["Eddie", 'Alex']      # Insert at index 2 (splice-in between items)
print('\n', user, '\n')

user[1:3] = ['Roberts', 'JPJ']     # Replaces two elements (index 1 and 2)
print('\n', user, '\n')

# --- ❌ REMOVING ITEMS ---

user.remove('Bob')                # Removes the first occurrence of 'Bob'
print(user.pop())                 # Removes and returns the last item
print('\n', user, '\n')

del user[0]                       # Deletes element at index 0
print('\n', user, "\n")

# --- 🚿 CLEARING AND REPLACING ITEMS ---

data.clear()                      # Empties the list
print('\n', data, '\n')

user[1:2] = ["dave"]              # Replace index 1 with 'dave'

# --- 🔃 SORTING ---

user.sort()                       # Sorts alphabetically (case-sensitive)
print('\n', user, '\n')

user.sort(key=str.lower)         # Sorts alphabetically (case-insensitive)
print('\n', user, '\n')

# --- 🔁 REVERSING & SORTED COPY ---

nums = [4, 42, 78, 1, 5]
nums.reverse()                   # Reverses the list in-place
print('\n', nums, '\n')

print(sorted(nums, reverse=True))  # Returns a new sorted list in descending order
print('\n', nums, '\n')            # Original list is unchanged

# --- 🧪 COPYING LISTS SAFELY ---

numscopy = nums.copy()           # Creates a full copy
mynums = list(nums)              # Another way to copy
mycopy = nums[:]                 # Slice copy

print('\n', numscopy, '\n')
print('\n', mynums, '\n')

mycopy.sort()                    # Sorting copy doesn't affect original
print('\n', mycopy, '\n')
print('\n', nums, '\n')          # nums is unchanged

print("\n", type(nums), "\n")    # Confirm it's still a list

mylist = list([1, "neil", True])  # Create list from another list (redundant but possible)
print('\n', mylist, '\n')

# --- 📦 TUPLES ---

mytuple = tuple(('miguel', 42, True))  # Tuple with multiple data types
anothertuple = tuple((1, 2, 3, 4))     # Another tuple of numbers

print('\n', mytuple, '\n')
print('\n', type(mytuple), '\n')       # Type confirmation
print('\n', type(anothertuple), '\n')

# --- 🔄 CONVERTING TUPLE TO LIST (TO MODIFY) AND BACK ---

newlist = list(mytuple)          # Convert tuple to list
newlist.append('neil')           # Now we can modify
newtuple = tuple(newlist)        # Convert back to tuple
print('\n', newtuple, '\n')

# --- 🧵 TUPLE UNPACKING ---

(one, *hey, two) = anothertuple  # Unpack first and last, with middle as a list
print(one)                       # First value
print(two)                       # Last value
print(hey)                       # Middle values as list

print(anothertuple.count(2))     # Count how many times '2' appears
