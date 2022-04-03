from os import getenv
from dotenv import load_dotenv
import mysql.connector as sql

load_dotenv()

def openDBConnection():
    return sql.connect(
        user=getenv('USERNAME'),
        password=getenv('PASS'),
        host=getenv('HOST'),
        database=getenv('DB')
    )

class User:
    def __init__(self):
        self.userID = -1
        self.isLoggedIn = False
        self.firstname = ""
        self.lastname = ""

    def setUserID(self, id):
        self.userID = id
    
    def setShippingInformation(self, address, pobox, city, state, zip):
        success = True
        db = openDBConnection()
        cursor = db.cursor(dictionary=True)

        # check if the user already has shipping information
        if not self.getShippingInformation(): # need to make new entry in table
            query = "INSERT INTO shipping_info (userID, address, pobox, city, state, zip) VALUES (%s, %s, %s, %s, %s, %s)"
            data = (str(self.userID), address, pobox, city, state, zip)

            try:
                cursor.execute(query, data)
                db.commit()
            except:
                success = False
        
        else: # just update the existing info
            query = f"UPDATE shipping_info SET address=%s, pobox=%s, city=%s, state=%s, zip=%s WHERE userID=%s"
            data = (address, pobox, str(self.userID))

            try:
                cursor.execute(query, data)
                db.commit()
            except:
                success = False

        cursor.close()
        db.close()

        return success

    def setPaymentInformation(self, cardNumber, expirationDate, zip, securityCode):
        success = True
        db = openDBConnection()
        cursor = db.cursor(dictionary=True)

        # check if the user already has payment information
        if not self.getPaymentInformation(): # need to make new entry in table
            query = "INSERT INTO payment_info (userID, cardNumber, expirationDate, zip, securityCode) VALUES (%s, %s, %s, %s, %s)"
            data = (str(self.userID), cardNumber, expirationDate, zip, securityCode)

            try:
                cursor.execute(query, data)
                db.commit()
            except:
                success = False
        
        else: # just update the existing info
            query = "UPDATE payment_info SET cardNumber=%s, expirationDate=%s, zip=%s, securityCode=%s WHERE userID=%s"
            data = (cardNumber, expirationDate, zip, securityCode, str(self.userID))

            try:
                cursor.execute(query, data)
                db.commit()
            except:
                success = False

        cursor.close()
        db.close()

        return success

    def getShippingInformation(self):
        db = openDBConnection()
        cursor = db.cursor(dictionary=True)

        query = f"SELECT * FROM shipping_info WHERE userID=%s"
        data = (str(self.userID), )

        cursor.execute(query, data)
        
        result = cursor.fetchall()

        cursor.close()
        db.close()

        return result

    def getPaymentInformation(self):
        db = openDBConnection()
        cursor = db.cursor(dictionary=True)

        query = f"SELECT * FROM payment_info WHERE userID=%s"
        data = (str(self.userID), )

        cursor.execute(query, data)
        
        result = cursor.fetchall()

        cursor.close()
        db.close()

        return result
    
    def getOrderHistory(self):
        ...
    
    def login(self, username, password):
        db = openDBConnection()
        cursor = db.cursor(dictionary=True)

        query = f"SELECT * FROM users WHERE username=\"{username}\" AND password=\"{password}\""
        cursor.execute(query)

        result = cursor.fetchall()

        if len(result) == 1:
            user = result[0]
            self.setUserID(user["userID"])
            self.isLoggedIn = True
            self.firstname = user["firstname"]
            self.lastname = user["lastname"]

        cursor.close()
        db.close()

        return self.isLoggedIn
    
    def logout(self):
        self.isLoggedIn = False

    def delete(self):
        db = openDBConnection()
        cursor = db.cursor(dictionary=True)
        success = True

        tablesToDeleteFrom = ["shipping_info", "payment_info", "users"]

        for table in tablesToDeleteFrom:
            query = f"DELETE FROM {table} WHERE userID=\"{self.userID}\""

            try:
                cursor.execute(query)
                db.commit()
                self.logout()
            except:
                success = False
        
        cursor.close()
        db.close()

        return success 

    def createAccount(self, username, password, firstname, lastname):
        db = openDBConnection()
        cursor = db.cursor(dictionary=True)
        success = True

        query = f"INSERT INTO users (username, password, firstname, lastname) VALUES (%s, %s, %s, %s)"
        data = (username, password, firstname, lastname)

        try:
            cursor.execute(query, data)
            db.commit()

        except:
            success = False

        return success

def driver():
    user = User()
    choice = "0"
    while choice != "x":
        if not user.isLoggedIn:
            print("=====[ eCommerce CLI ]=====")
            print("|| 1. Login              ||")
            print("|| 2. Create new account ||")
            print("|| X. Exit               ||")
            print("===========================\n")

            choice = input("Enter your choice :: ").lower()
            print()

            if choice == "1":
                username = input("Enter username :: ")
                password = input("Enter password :: ")

                if user.login(username, password):
                    print(f"\nHello, {user.firstname} {user.lastname}!\n")
                
                else:
                    print("\nInvalid credentials.\n")
            
            if choice == "2":
                username = input("Enter username :: ")
                password = input("Enter password :: ")
                firstname = input("Enter first name :: ")
                lastname = input("Enter last name :: ")

                if user.createAccount(username, password, firstname, lastname):
                    print("Account created\n")
                
                else:
                    print("There was an error during account creation\n")
        
        else:
            print("==========[ eCommerce CLI ]=========")
            print("|| 1. Manage shipping information ||")
            print("|| 2. Manage payment information  ||")
            print("|| L. Logout                      ||")
            print("|| D. Delete account              ||")
            print("|| X. Exit                        ||")
            print("====================================\n")

            choice = input("Enter your choice :: ").lower()
            print()

            if choice == "1":
                print("==========[ eCommerce CLI ]=========")
                print("|| 1. View shipping information   ||")
                print("|| 2. Set shipping information    ||")
                print("|| 3. Go back                     ||")
                print("====================================\n")

                choice = input("Enter your choice :: ").lower()
                print()

                if choice == "1":
                    info = user.getShippingInformation()
                    if not info:
                        print("You have no shipping information\n")
                    else:
                        print(f"Address: {info[0]['address']}")
                        print(f"PO Box: {info[0]['pobox']}")
                        print(f"City: {info[0]['city']}")
                        print(f"State: {info[0]['state']}")
                        print(f"Zip Code: {info[0]['zip']}\n")
                
                if choice == "2":
                    address = input("Enter address :: ")
                    pobox = input("Enter PO box (\"none\" for no PO box) :: ")
                    city = input("Enter city :: ")
                    state = input("Enter state :: ")
                    zip = input("Enter zip code :: ")

                    if user.setShippingInformation(address, pobox, city, state, zip):
                        print("Shipping information successfully set\n")
                    else:
                        print("There was an error during shipping information setting\n")

            if choice == "2":
                print("==========[ eCommerce CLI ]=========")
                print("|| 1. View payment information    ||")
                print("|| 2. Set payment information     ||")
                print("|| 3. Go back                     ||")
                print("====================================\n")

                choice = input("Enter your choice :: ").lower()
                print()

                if choice == "1":
                    info = user.getPaymentInformation()
                    if not info:
                        print("You have no payment information\n")
                    else:
                        print(f"Card Number: {info[0]['cardNumber']}")
                        print(f"Expiration Date: {info[0]['expirationDate']}")
                        print(f"Zip Code: {info[0]['zip']}")
                        print(f"Security Code: {info[0]['securityCode']}\n")

                if choice == "2":
                    cardNumber = input("Enter card number :: ")
                    expirationDate = input("Enter expiration date (MM/YY) :: ")
                    zip = input("Enter zip code :: ")
                    securityCode = input("Enter security code :: ")

                    if user.setPaymentInformation(cardNumber, expirationDate, zip, securityCode):
                        print("Payment information successfully set\n")
                    else:
                        print("There was an error during payment information setting\n")

            if choice == "l":
                print(f"Goodbye, {user.firstname}\n")
                user.logout()

            if choice == "d":
                sure = input("Are you sure? (y/n) :: ").lower()
                if sure == "y":
                    if user.delete():
                        print("Account successfully deleted\n")
                    else:
                        print("There was an error during account deletion\n")    

if __name__ == "__main__":
    driver()
