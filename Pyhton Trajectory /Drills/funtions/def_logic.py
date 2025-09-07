# def grade(score):
#     if score >= 90:
#         return "A"
#     elif score >= 75:
#         return "B"
#     else:
#         return "C"

# print(grade(95))  # "A"
# print(grade(80))  # "B"
# print(grade(50))  # "C"



def coffee_recommendation(time_of_day):
    if time_of_day == "morning":
        return "espresso"
    elif time_of_day == "afternoon":
        return "latte"
    else:
        return "decaf"

print(coffee_recommendation("morning"))
print(coffee_recommendation("afternoon"))
print(coffee_recommendation("night"))
