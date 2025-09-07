# dictionaries_and_sets_explained.py

"""
🧠 Python Dictionaries & Sets — Beginner Learning Script

This walkthrough teaches how to use:
- 📕 Dictionaries (key:value pairs)
- 🔢 Sets (unique, unordered collections)

Each section includes learning comments to help you understand and apply these structures.
"""

# === 📕 DICTIONARIES ===

# --- 🧱 1. DICTIONARY CREATION ---

# Dictionary using curly braces {}
band = {
    "vocals": "plant",
    "guitar": "page"
}

# Dictionary using the dict() constructor
band2 = dict(vocals="Not like us", guitar="Benito")

# Print dictionaries and confirm types
print('\n', band, '\n')
print('\n', band2, '\n')
print('\n', type(band), '\n')
print('\n', type(band2), '\n')
print('\n', len(band), '\n')
print('\n', len(band2), '\n')

# 🔍 What You Learned:
# Dictionaries are built using key:value pairs
# They can be created with {} or the dict() function
# You can inspect their type and length easily


# --- 🔍 2. ACCESSING ITEMS ---

print('\n', band["vocals"], '\n')        # Direct access
print('\n', band2["vocals"], '\n')
print('\n', band.get("guitar"), '\n')    # Safer access with .get()
print('\n', band2.get("guitar"), '\n')

# 🔍 .get() avoids errors if the key is missing — returns None instead of crashing


# --- 📋 3. KEYS, VALUES, ITEMS ---

print('\n', band.keys(), '\n')         # All keys
print('\n', band2.keys(), '\n')

print('\n', band.values(), '\n')       # All values
print('\n', band2.values(), '\n')

print('\n', band.items(), '\n')        # All items (key:value pairs)
print('\n', band2.items(), '\n')


# --- ✅ 4. CHECK IF KEY EXISTS ---

print('\n', 'guitar' in band, '\n')        # True
print('\n', 'triangle' in band, '\n')      # False

# 🔍 Use `in` to check if a key exists before accessing or modifying it


# --- ✏️ 5. UPDATING / ADDING KEYS ---

band['vocals'] = "kendrick"               # Overwrites 'vocals'
band2['vocals'] = "lamar"

band.update({"bass": "benito"})           # Adds new key:value
band2.update({"bass": "bad bunny"})

print('\n', band, '\n')
print('\n', band2, '\n')


# --- 🗑️ 6. REMOVING ITEMS ---

print(band.pop("guitar"))                # Removes and returns value
print('\n', band, '\n')

band["drums"] = "bonham"
print('\n', band, '\n')

print(band.popitem())                    # Removes last added item
print('\n', band, '\n')


# --- ❌ 7. DELETE OR CLEAR ---

band["drums"] = "bonham"
del band['drums']                        # Deletes specific key
print('\n', band, '\n')

band2.clear()                            # Empties the dictionary
print('\n', band2, '\n')

# del band2                             # Destroys the variable entirely (commented for safety)


# --- 📎 8. COPYING DICTIONARIES ---

# ❌ Bad copy (by reference): band2 = band — this would link them
# ✅ Correct copy: .copy()
band2 = band.copy()
band2["vocals"] = "dave"

print('\n', "good copy!", '\n')
print('\n', band, '\n')
print('\n', band2, '\n')

# ✅ Another copy method: using dict()
band3 = dict(band)
print('\n', band3, '\n')


# --- 🧬 9. NESTED DICTIONARIES ---

member1 = {
    "name": "plant",
    "instrument": "vocals"
}

member2 = {
    "name": "page",
    "instrument": "guiter"
}

band = {
    "member1": member1,
    "member2": member2
}

print('\n', band, '\n')
print('\n', band['member1']["name"], '\n')  # Access nested data

# 🔍 Dictionaries can hold other dictionaries (nested structures)


# === 🔢 SETS ===

# Sets store unique, unordered values with no duplicates and no indexing

# --- 🔧 1. CREATE SETS ---

nums = {1, 2, 3, 4}
nums2 = set((1, 2, 3, 4))

print(nums)
print(nums2)
print(type(nums))
print(len(nums))


# --- 🧼 2. NO DUPLICATES ALLOWED ---

nums = {1, 2, 2, 3, 4}     # 2 appears twice, but only stored once
print(nums)               # Output: {1, 2, 3, 4}

nums = {1, True, 2, False, 3, 4, 0}
print('\n', nums, '\n')   # True == 1, False == 0 (counts as duplicates)

# 🔍 Sets remove all duplicates automatically


# --- 🔍 3. CHECK IF VALUE EXISTS ---

print(2 in nums)  # Returns True or False


# --- 🚫 4. NO INDEXING ---

# nums[0] would crash — sets do not maintain order


# --- ➕ 5. ADDING TO SETS ---

nums.add(8)                 # Add a single item
print(nums)

morenums = {5, 6, 7}
nums.update(morenums)      # Add multiple items
print(nums)


# --- 🔄 6. MERGING SETS ---

# Union = combine sets (remove duplicates)
one = {1, 2, 3}
two = {5, 6, 7}
mynewser = one.union(two)
print(mynewser)


# --- 🔁 7. INTERSECTION (KEEP DUPLICATES ONLY) ---

one = {1, 5, 7}
two = {5, 6, 7}
one.intersection_update(two)
print(one)  # Output: {5, 7}


# --- 🔁 8. SYMMETRIC DIFFERENCE (KEEP DIFFERENCES ONLY) ---

one = {1, 5, 7}
two = {5, 6, 7}
one.symmetric_difference_update(two)
print(one)  # Output: {1, 6}

"""
✅ Summary of Key Concepts:

🔹 Dictionaries
- Use key:value pairs
- Can be nested and copied
- Allow for quick lookups and flexible data structures

🔹 Sets
- Store only unique values
- Are unordered and unindexed
- Support powerful math-like operations (union, intersection, etc.)

Use dictionaries for structured data and sets for uniqueness filtering or fast comparisons.
"""
