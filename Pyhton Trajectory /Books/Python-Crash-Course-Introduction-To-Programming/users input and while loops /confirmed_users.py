
# moving  items from one list  to another 

uncorfirmed_users = ['alice', 'brian', 'candace']
confirmed_users = []

while uncorfirmed_users:
    current_user = uncorfirmed_users.pop()

    confirmed_users.append(current_user)

    print(f"Verifying user: {current_user.title()}")

print("\nThe following users have been confirmed:")
for confirmed_user in confirmed_users:
    print(confirmed_user.title())
