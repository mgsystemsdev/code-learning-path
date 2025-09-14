# def get_formatted_name(firts_name, last_name):
#     full_name = f"{firts_name}  {last_name}"
#     return full_name.title()
# while True:
#     print("\nPlease tell me your name:")
#     print("(enter 'q' at any time to quit )")

#     f_name = input("First name : ")
#     if f_name == 'q':
#         break

#     l_name = input("Last name:")
#     if l_name == 'q':
#         break

#     formatted_name = get_formatted_name(f_name, l_name)
#     print(f"\nHello, {formatted_name}!")


# def greet_users(names):

#     for name in names:
#         msg = f"Hello, {name.title()} ! "
#         print(msg)

# usernames = ['hannna', 'ty','margot']

# greet_users(usernames)





# make_ready_nvm = ['notice', 'vacant', 'schedule to move in ', 'move in']
# nvm = []

# while make_ready_nvm:
#     current_desings = make_ready_nvm.pop()
#     print(f"status:{current_desings}")
#     nvm.append(current_desings)

# print("\nThe following models have been printed :")

# for nvms in nvm:
#     print(nvms)






def nvmmr(nvm, make_ready_nvm):

    while make_ready_nvm:
        current_desings = make_ready_nvm.pop()
        print(f"status:{current_desings}")
        nvm.append(current_desings)


def show_full(nvm):
    print("\nThe following status have been printed :")

    for nvms in nvm:
        print(nvms)



make_ready_nvm = ['notice', 'vacant', 'schedule to move in ', 'move in']
nvm = []

nvmmr(nvm, make_ready_nvm)
show_full(nvm)


