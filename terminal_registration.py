def terminal_input_register():

    loop1 = True
    loop2 = True

    #todo: maybe introduce if statements in the loops to check if username/pwd satisfy certain conventions

    while loop1:
        username = input("Please select your username: ")
        
        loop1 = False

    while loop2:
        pwd_clear = input("Please select your password: ")
        loop2 = False

    print(f"Your username is ", {username})
    print(f"Your password is: ", {pwd_clear})

terminal_input_register()