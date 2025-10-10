# Empty users, which is filled with dicts of users with "username" and "password"
user_list = {}


def register():

    global user_list

    loop1 = True
    loop2 = True

    #todo: maybe introduce if statements in the loops to check if username/pwd satisfy certain conventions

    username = None
    pwd = None

    while loop1:
        username = input("Please select your username: ")
        loop1 = False

    while loop2:
        pwd_clear = input("Please select your password: ")
        loop2 = False

    #print(f"Your username is ", {username})
    #print(f"Your password is: ", {pwd_clear})

    if username not in user_list:
      user_list[username] = {
        'password': pwd_clear
      }
    else:
        print("Username is already taken.")
        return

    print("You were successfully added as a new user :)")


def authenticate():
    # would probably be prettier if we pass it as an input parameter instead of using a global variable
    global user_list 
    loop1 = True
    loop2 = True

    while loop1:
        username = input("Please input your username: ")
        loop1 = False

    while loop2:
        pwd_clear = input("Please input your password: ")
        loop2 = False

    # Fails if its either the wrong password or the username does not exist
    # Important to check it after both, username and pwd, are already inputted
    if username not in user_list:
        print("Username or password wrong.")
    elif user_list[username]["password"] != pwd_clear:
        print("Username or password wrong.")
    else:
        print("Successfully authenticated!")
        

def register_or_authenticate():
    selection = input("Do you already have an account? y for yes and n for no: ")
    if selection == "y":
        authenticate()
    elif selection == "n":
        register()
    else:
        print("Sorry, we couldn't understand your input. Please restart the program and try again.")

#register()
#authenticate()
register_or_authenticate()