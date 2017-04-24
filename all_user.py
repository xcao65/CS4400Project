from connection import *

class LogIn():
    def login(self, name, pwd):
        username = name
        password = pwd
        connection = connect()
        cursor = connection.cursor()
        sql = "SELECT Username, Password, Type, EmailAddress FROM User WHERE Username = %s"
        cursor.execute(sql, username)
        results = cursor.fetchone()
        connection.close()

        if username == "" or password == "":
            # print("Error! Please do not leave any fields blank")
            return None
        else:
            if results is None:
                # print "Invalid! Please enter a correct username and password combination"
                return None
            else:
                if password == results["Password"]:
                    print results
                    utype = results["Type"]
                    # print utype
                    if utype == "City Official" and not self.check_official(results["EmailAddress"]):
                        print "Your city official account is pending"
                        return None
                    else:
                        #print utype
                        print("Congrats! You successfully logged in")
                        return utype
                else:
                    # print "Error! Please enter a correct username and password combination"
                    return None

    # check if the city official is approved or not
    def check_official(self, email):
        connection = connect()
        cursor = connection.cursor()
        sql = "SELECT Status FROM City_Official WHERE EmailAddress = %s"
        cursor.execute(sql, email)
        result = cursor.fetchone()
        connection.close()
        # print result['Status']
        return result['Status'] == 'Approved'


    def register(self, name, email, pwd, cpwd, utype, *others):
        if not self.checkUniqueName(name):
            # print 'Username has been used, try another one'
            return False
        if not self.checkUniqueEmail(email):
            # print 'Email has been registered, try another one'
            return False
        if pwd != cpwd:
            # print 'password must be matched'
            return False
        connection = connect()
        cursor = connection.cursor()
        sql = "INSERT INTO User (EmailAddress, UserName, Password, Type) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (email, name, pwd, utype))
        connection.commit()
        result = cursor.fetchone()
        connection.close()
        print 'Added new user successfully'


        if utype == 3:
            connection = connect()
            extras = []
            for x in others: extras.append(x)
            cursor = connection.cursor()
            sql = "INSERT INTO City_Official (EmailAddress, Title, City, State) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (email, extras[0], extras[1], extras[2]))
            connection.commit()
            connection.close()
            print 'Added New City Official Successfully'

        if result == None:
            return True
        else:
            return False


    def checkUniqueName(self, name):
        connection = connect()
        cursor = connection.cursor()
        sql = "SELECT username FROM User WHERE Username = %s"
        cursor.execute(sql, name)
        results = cursor.fetchone()
        connection.close()
        return results == None

    def checkUniqueEmail(self, email):
        connection = connect()
        cursor = connection.cursor()
        sql = "SELECT EmailAddress FROM User WHERE EmailAddress = %s"
        cursor.execute(sql, email)
        results = cursor.fetchone()
        connection.close()
        return results == None

    def deleteUser(self, name):
        connection = connect()
        cursor = connection.cursor()
        sql = "DELETE FROM User WHERE Username =  %s "
        # cursor.execute(sql, 'Justin Bieber')
        cursor.execute(sql, name)
        connection.commit()
        connection.close()
        # print 'delete successfully'

if __name__ == "__main__":
    test = LogIn()
    #print test.deleteUser('Oprah Winfrey')
    #print test.checkUniqueName('Justin Bieber')
    #print test.login('Oprah Winfrey', 'OprahWinfrey')
    #print test.register('Oprah Winfrey','Oprah.Winfrey@gatech.edu', 'OprahWinfrey','OprahWinfrey', 'City Official', 'Major', 'Jacksonville', 'Florida')
    print test.check_official('456@gatech.edu')
    print test.login('456', '456')
