# from connection import Connection

class LogIn():
    def login(self, name, pwd, connection):
        username = name
        password = pwd
        cursor = connection.cursor()
        sql = "SELECT Username, Password, Type FROM User WHERE Username = %s"
        cursor.execute(sql, username)
        getname = cursor.fetchone()

        if username == "" or password == "":
            print("Error! Please do not leave any fields blank")
        else:
            if getname is None:
                print("Error! Please enter a correct username and password combination")
            else:
                if password == getname["Password"]:
                    print("Congrats! You successfully logged in")
                    utype = getname["Type"]
                    print(utype)

                else:
                    print("Error! Please enter a correct username and password combination")

    def register(self):
        pass
