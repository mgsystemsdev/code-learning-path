# === Python Type: Data Types, Casting, Operators, String Manipulation & Formatting ===
# This walkthrough shows how Python handles types, conversion, math, formatting, and string operations

# --- BOOLEAN TYPES & TYPE CHECKING ---

myvalue = True  # Boolean literal assigned to a variable
x = bool(False)  # Explicitly casting to a Boolean type using bool() constructor

print("\n", type(x))  # Prints the data type of x, expected: <class 'bool'>
print(isinstance(myvalue, bool), "\n")  # Checks if 'myvalue' is a Boolean type; returns True


# --- NUMERIC TYPES & MATH OPERATORS ---

gpa = 3.28  # Float value assigned
y = float(1.14)  # Explicit float conversion

# Built-in functions with numeric input
print(abs(gpa))        # abs() gives absolute value: stays 3.28
print(abs(gpa * -1))   # abs() flips negative to positive: becomes 3.28

print(round(gpa))      # round() to nearest integer: becomes 3
print(round(gpa, 1))   # round() to 1 decimal place: stays 3.3


# --- TYPE CASTING TO STRING ---

print("")  # Spacer line
decade = str(1980)  # Casting integer to string
print(type(decade))  # Confirms 'decade' is now a string
print(decade)        # Outputs the string '1980'

# Method 1: String concatenation with +
statement = "I like rock music from the " + decade + "s."
print(statement)  # Combines strings with + operator

print("")  # Spacer

# Method 2: Using an f-string (formatted string literal)
decade = 1980
statement = f"I like rock music from the {decade}s."
print(statement)

# Method 3: f-string with embedded newlines
statement = f"\nI like rock music from the {decade}s.\n"
print(statement)


# --- STRING CONCATENATION ---

first = "Miguel"
last = "Gonzalez"

print("")  # Spacer
fullname = first + " " + last  # Basic string concatenation with space
print(fullname)

print("")  # Spacer
fullname += "!"  # Adds exclamation point to fullname using +=
print(fullname)
print('')  # Blank line


# Concatenation Method 2: Using f-strings
print("")
fullname = f"{first} {last}!"  # Formatted string with embedded variables
print(fullname)
print("")


# --- TYPE CONSTRUCTION FUNCTIONS ---

pizza = "\n" + str("pepperoni")  # Casts a string to string again, with newline in front

print("\n")                     
print(type(pizza))              # Should show <class 'str'>
print(type(pizza) == str)       # True, confirms it is a string type
print(str(isinstance(pizza, str)) + "\n")  # Confirms using isinstance() and casts result to string


# --- ESCAPING SPECIAL CHARACTERS ---

# Method 1: Using backslashes to escape quotes and slashes
sentence = '\nI\'m back at work!\they!\n\nwhere\s this at\located\n'
print(sentence)

# Method 2: Using raw string to ignore escape sequences (useful for file paths)
file_path = "\n" + r"C:\newfolder\myfiles\notes.txt" + '\n'
print(file_path)


# --- STRING TYPE CHECKING & IDENTITY ---

first = "Miguel"
last = "Gonzalez"

print("\n" + str(type(first)))        # Outputs the type of the string variable
print(type(first) == str)            # Confirms it's of type str using comparison
print(str(isinstance(first, str)) + "\n")  # Confirms using isinstance()


# --- MATH LIBRARY FUNCTIONS ---

gpa = 3.28
import math  # Importing math module

print("\n", math.pi)             # Shows value of pi
print(math.sqrt(64))            # Square root function
print(math.ceil(gpa))           # Rounds up to next whole number
print(math.floor(gpa), "\n")    # Rounds down to previous whole number


# --- TEXT FORMATTING WITH ALIGNMENT ---

tittle = "menu".upper()  # Converts to uppercase
print("\n" + tittle.center(20, "="))  # Centers title with '=' padding

# Menu items aligned with formatting
print("cofee".ljust(16, ".") + "$1\n".rjust(4))     
print("Muffin".ljust(16, ".") + "$2\n".rjust(4))    
print("donuts".ljust(16, ".") + "$4\n".rjust(4))    
print("juices".ljust(16, ".") + "$6\n".rjust(4))    
print("sandwitches".ljust(16, ".") + "$10\n".rjust(4))


# --- MULTILINE STRINGS ---

multiline = '''

           hey how are you


       i was just checking in.          

                        All good ?

 '''
print(multiline)


# --- STRING METHODS DEMO ---

print(first + "\n")        # Original name
print(first.lower() + "\n")  # Lowercase conversion
print(first.upper() + "\n")  # Uppercase conversion
print(first + "\n")        # Again original

print(multiline.title())       # Capitalizes first letter of each word
print(multiline.replace("good", "ok"))  # Replaces text in string
print(multiline)               # Prints original again (unchanged)

print(len(multiline))          # Length of the string including all whitespace
multiline += ''                # No change
multiline = ''                 # Clears the variable

# Trimming string (no effect now since it's empty)
print(len(multiline.strip()))     # Length after stripping both sides
print(len(multiline.lstrip()))    # Left-stripped
print(len(multiline.rstrip()))    # Right-stripped


# --- STRING INDEXING & SLICING ---

print("\n" + first[0])       # First character (index 0)
print(first[0:6])            # Slicing from index 0 to 5 (not inclusive of 6)
print(first[12:6])           # Invalid slice; returns empty string
print(first[3])              # Character at index 3
print(first[4])              # Character at index 4
print(first[5] + "\n")       # Character at index 5, with newline


# --- INTEGER TYPE CHECKING ---

price = 100                 # Integer literal
best_price = int(80)        # Explicitly cast to int
print("\n", type(price))    # Shows type
print(isinstance(best_price, int), "\n")  # Checks if int


# --- FLOAT TYPE ---

gpa = 3.28
y = float(1.14)
print("\n", type(gpa), "\n")  # Outputs float type


# --- COMPLEX TYPE ---

comp_value = 5 + 3j  # Complex number (5 real, 3 imaginary)
print(type(comp_value))          # Shows it's a complex type
print(type(comp_value.real))     # Real part is float
print(type(comp_value.imag))     # Imaginary part is also float


# --- STRING STARTS/ENDS CHECK ---

print("\n")
print(first.startswith("M"))  # Checks if string starts with 'M'
print(first.endswith("l"))    # Checks if string ends with 'l'
print("\n")

# Method 2: Using f-strings
print(f"\nStarts with 'M': {first.startswith('M')}")
print(f"Ends with 'l': {first.endswith('l')}\n")

# Method 3: Inline logic
print("\n", first.startswith("M"), first.endswith("l"), "\n")
