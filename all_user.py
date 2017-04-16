# from connection import Connection

class LogIn():
    def login(self, name, pwd, connection):
        username = name
        password = pwd
        cursor = connection.cursor()
        sql = "SELECT Username, Password, Type FROM User WHERE Username = %s"
        cursor.execute(sql, username)
        results = cursor.fetchone()

        if username == "" or password == "":
            print("Error! Please do not leave any fields blank")
        else:
            if results is None:
                print("Invalid! Please enter a correct username and password combination")
            else:
                if password == results["Password"]:
                    print results
                    print("Congrats! You successfully logged in")
                    utype = results["Type"]
                    print utype
                else:
                    print("Error! Please enter a correct username and password combination")


    def register(self, name, email, pwd, cpwd, utype, connection, *others):
        if not self.checkUniqueName(name, connection):
            print 'Username has been used, try another one'
            return
        if not self.checkUniqueEmail(email, connection):
            print 'Email has been registered, try another one'
            return
        if pwd != cpwd:
            print 'password must be matched'
            return
        cursor = connection.cursor()
        sql = "INSERT INTO User (EmailAddress, UserName, Password, Type) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (email, name, pwd, utype))
        connection.commit()
        print 'Added new user successfully'

        if utype == 'City Official':
            extras = []
            for x in others: extras.append(x)
            cursor = connection.cursor()
            sql = "INSERT INTO City_Official (EmailAddress, Title, City, State) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (email, extras[0], extras[1], extras[2]))
            connection.commit()
            print 'Added New City Official Successfully'

    def checkUniqueName(self, name, connection):
        cursor = connection.cursor()
        sql = "SELECT username FROM User WHERE Username = %s"
        cursor.execute(sql, name)
        results = cursor.fetchone()
        return results == None

    def checkUniqueEmail(self, email, connection):
        cursor = connection.cursor()
        sql = "SELECT EmailAddress FROM User WHERE EmailAddress = %s"
        cursor.execute(sql, email)
        results = cursor.fetchone()
        return results == None
