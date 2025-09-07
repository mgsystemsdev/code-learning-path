# def box():
#     return "hello"
# print(box())

# def ping():
#     answer = "pong"
#     return answer
# answer = ping()
# print(f"Ping {answer}")
# a blueprint with nothing inside (yet)
class Dog:
    pass

# build one dog from the blueprint
buddy = Dog()

print(buddy)            # shows "a Dog object lives here"
print(type(buddy))      # shows the object's type
print(isinstance(buddy, Dog))  # True: buddy is a Dog
