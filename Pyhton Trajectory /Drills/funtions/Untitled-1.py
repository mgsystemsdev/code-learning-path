



# def outer():
#     def inner():
#         print("I'm inside!")
#     inner()

# outer()

# from functools import reduce

# nums = [5, 10, 15, 20]

# divided = list(map(lambda x: x / 5, nums))
# greater = list(filter(lambda x: x > 10, nums))
# product = reduce(lambda a, b: a * b, nums)

# print(divided)  # expect [1.0, 2.0, 3.0, 4.0]
# print(greater)  # expect [15, 20]
# print(product)  # expect 15000




def decorator(func):
    def wrapper():
        print("Before function runs...")
        func()
        print("After function runs...")
    return wrapper

@decorator
def say_hello():
    print("Hello!")

say_hello()
