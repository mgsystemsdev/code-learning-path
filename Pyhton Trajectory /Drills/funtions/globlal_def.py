

# name = "Miguel"  # global variable

# def greet():
#     name = "Ada"  # local variable
#     print(f"Hello, {name}!")  # uses local

# greet()
# print(name)  # uses global


# status = "offline"

# def set_online():
#     global status  # tell Python to use the global variable
#     status = "online"
#     print(f"Inside function: {status}")

# set_online()
# print(f"Outside function: {status}")


counter = 100  # global

def increment():
    global counter  # tell Python to use the global variable
    counter += 1
    print(f"Inside function: {counter}")

increment()
print(f"Outside function: {counter}")
