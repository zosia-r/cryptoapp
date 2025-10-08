import pandas as pd

# Idea: use pd.DataFrame to store all the information about the users
# Is probably a bit overkill, so a list/array of dictionaries? or sth similar would probably be sufficient
user_list = pd.DataFrame(columns=["username", "password"])



def terminal_register():

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

    print(f"Your username is ", {username})
    print(f"Your password is: ", {pwd_clear})
    
    new_user = {"username": username, "password": pwd}
    global user_list
    user_list = pd.concat([user_list, pd.DataFrame([new_user])], ignore_index=True)

    print("You were successfully added as a new user :)")

terminal_register()