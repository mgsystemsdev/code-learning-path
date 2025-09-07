

## **Stage 7: Returning & Unpacking Multiple Values**

# **core idea:** a function can return **more than one value**, and you can easily **unpack** them into separate variables.

# ---

### **mini-lesson**

def get_user():
    return "Miguel", "Python Developer"

name, role = get_user()
print(name)  # Miguel
print(role)  # Python Developer



# ```

# ---

# ### **exercise 7.1 – basic unpacking**

# 1. Write a function called `get_weather` that returns:

#    * temperature (number)
#    * condition (string)
# 2. Unpack those values into `temp` and `condition`.
# 3. Print a nice message like:

#    ```
#    The temperature is 72°F and the condition is sunny.
#    ```

# **starter template:**

# ```python

def get_weather():
    # return two values
    temp = 72
    condition = "sunny"
    humidity = 55  # bonus challenge
    return temp, condition, humidity

temp, condition, humidity = get_weather()
print(f"The temperature is {temp}°F and the condition is {condition}.")
print(f"The humidity is {humidity}%.")

# ```

# ---

# ### **bonus challenge**

# * Change the function to return **three values**:
#   temperature, condition, and humidity.
# * Unpack and print all three in a sentence.

# ---

# want to try it?
# paste your code, and we’ll review it step by step until you feel **rock-solid**.
