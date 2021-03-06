from user import User
from inventory import Inventory
from cart import Cart

def driver():
    user = User()
    inv = Inventory()
    cart = Cart()
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
            
            elif choice == "2":
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
            print("|| 3. View order history          ||")
            print("|| 4. View inventory              ||")
            print("|| 5. Manage cart                 ||")
            print("|| 6. Checkout                    ||")
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
                
                elif choice == "2":
                    address = input("Enter address :: ")
                    pobox = input("Enter PO box (\"none\" for no PO box) :: ")
                    city = input("Enter city :: ")
                    state = input("Enter state :: ")
                    zip = input("Enter zip code :: ")

                    if user.setShippingInformation(address, pobox, city, state, zip):
                        print("Shipping information successfully set\n")
                    else:
                        print("There was an error during shipping information setting\n")

            elif choice == "2":
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

                elif choice == "2":
                    cardNumber = input("Enter card number :: ")
                    expirationDate = input("Enter expiration date (MM/YY) :: ")
                    zip = input("Enter zip code :: ")
                    securityCode = input("Enter security code :: ")

                    if user.setPaymentInformation(cardNumber, expirationDate, zip, securityCode):
                        print("Payment information successfully set\n")
                    else:
                        print("There was an error during payment information setting\n")

            elif choice == "3":
                hist = user.getOrderHistory()
                if not hist:
                    print("You have no order history\n")
                else:
                    for entry in hist:
                        print(f"Title: {entry['title']}\nQuantity: {entry['quantity']}\nPrice: {entry['price']}\nDate: {entry['date']}\n")

            elif choice == "4":
                if not inv.items:
                    print("The inventory is empty")
                else:
                    for movie in inv.items:
                        print(f"ID: {movie.movieID}\nTitle: {movie.title}\nGenre: {movie.genre}\nDirector: {movie.director}\nRating: {movie.rating}\nYear: {movie.year}\nPrice: {movie.price}\nQuantity: {movie.quantity}\n")

            elif choice == "5":
                print("==========[ eCommerce CLI ]=========")
                print("|| 1. View cart                   ||")
                print("|| 2. Add item to cart            ||")
                print("|| 3. Remove item from cart       ||")
                print("|| 4. Go back                     ||")
                print("====================================\n")

                choice = input("Enter your choice :: ").lower()
                print()
                if choice == "1":
                    items = cart.getCart(user.userID)
                    if not items: 
                        print ("Cart is empty\n")
                    else: 
                        for item in items: 
                            print (f"ID: {item['movieID']} | Title: {item['title']} | Quantity: {item['quantity']}")
                        formattedTotal = "{:.2f}".format(cart.getCost(user.userID))
                        print(f"\nTotal price: ${formattedTotal}")
                        print()
                elif choice == "2":
                    id = input("Enter movie ID :: ")
                    qty = input("Enter quantity :: ")
                    if cart.addItem(user.userID, id, qty):
                        print("Items added to the cart\n")
                    else: 
                        print("Failed to add to cart\n")
                elif choice == "3":
                    id = input("Enter movie ID :: ")

                    if cart.removeItem(user.userID, id):
                        print("Successfully removed from cart\n")
                    else: 
                        print("Failed to remove from cart\n")
            
            elif choice == "6":
                if not cart.getCart(user.userID):
                    print("Your cannot checkout with an empty cart\n")
                else: 
                    if cart.checkout(user, inv):
                        print("Successfully checked out\n")
                    else: 
                        print("Failed to checkout. Are you trying to buy more movies that are in stock?\n")

            elif choice == "l":
                print(f"Goodbye, {user.firstname}\n")
                user.logout()

            elif choice == "d":
                sure = input("Are you sure? (y/n) :: ").lower()
                if sure == "y":
                    if user.delete():
                        print("Account successfully deleted\n")
                    else:
                        print("There was an error during account deletion\n")    

if __name__ == "__main__":
    driver()
