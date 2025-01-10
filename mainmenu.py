from member_reg_and_log import *
import mysql.connector

conn = mysql.connector.connect(
    host="localhost", user="root", password="010580sis", database="book_store")
cursor = conn.cursor()


# allows the user to browse books by subject and has the option of adding them to cart
def browse_by_subject(userid):
    try:    # error handling for database connection
        # fetch all unique sibjects from the books table alphabetically
        cursor.execute("SELECT DISTINCT Subject FROM books ORDER BY Subject")
        subjects = cursor.fetchall()
        if not subjects:  # checks if there are subjects available
            print('no subjects available')
            return
        print('\n--- Available Subjects ---')
        for i, subject in enumerate(subjects, 1):  # displays available subjects
            print(f'{i}.{subject[0]}')
        try:    # error handling for value error
            choice = int(input('Enter a choice:')) - 1    # convert choice to index
            # error handling for subject choice
            if choice < 0 or choice >= len(subjects):
                print('invalid subject choice')
                return

            choice_subject = subjects[choice][0]    # gets chosen subject
        except ValueError:
            print('invalid input')
            return
        cursor.execute("""
            SELECT COUNT(*) FROM books WHERE Subject = %s
        """, (choice_subject,))     # counts the number of books available for subject
        book_count = cursor.fetchone()[0]
        print(f'{book_count} books available for this subject')

        cursor.execute("""
        SELECT Author,Title,ISBN,Price,Subject FROM books WHERE Subject=%s
        """, (choice_subject,))     # retrieves all books from selected subject
        all_books = cursor.fetchall()
        if not all_books:   # checks if no books are found and returns to menu
            print('no books found')
            return
        books_per_page = 2  # intialization to display two books in one page
        current_page = 0
        total_books = len(all_books)  # length of all books
        while True:  # loop for displaying and continous user input until termination
            start_index = current_page * books_per_page
            end_index = start_index + books_per_page
            page_books = all_books[start_index:end_index]
            # start and end index for the current page
            # loop to display books on current page
            for i, book in enumerate(page_books, start=start_index+1):
                print(f'{i}:')
                print(f'Author:\t{book[0]}')
                print(f'Title:\t{book[1]}')
                print(f'ISBN:\t{book[2]}')
                print(f'Price:\t{book[3]}')
                print(f'Subjects:\t{book[4]}')
            if end_index < total_books:     # checks if there are more available cooks
                print(
                    "\n Enter ISBN to add to cart or enter 'n' to browse enter Enter to go back")
            else:
                print(
                    "\nNo more books to display. Enter ISBN to add to cart or press Enter to return to the main menu.")
            # user input for available options
            user_input = input("Enter your choice: ").strip()
            if user_input.lower() == 'n' and end_index < total_books:
                current_page += 1  # changes page
            elif user_input == '':  # exits and returns to menu
                print("Returning to main menu...")
                break
            elif len(user_input) in [10, 13]:  # validation for isbn length
                # user input for quantity and adding to cart
                user_quantity = int(input('Enter a quantity:'))
                if user_quantity > 0:
                    add_to_cart(userid, user_input, user_quantity)
                else:
                    print('quantity must be positive')
            else:
                print("Invalid input. Try again.")
    except mysql.connector.Error as e:
        print(f"database connection error: {e}")


def add_to_cart(user_id, isbn, quantity):
    try:
        # checks if the book is already in the cart
        cursor.execute("""
            SELECT * FROM cart WHERE userid = %s AND ISBN = %s
        """, (user_id, isbn))
        existing_item = cursor.fetchone()

        if existing_item:
            # updates quantity if the book already exists in the cart
            cursor.execute("""
                UPDATE cart SET quantity = quantity + %s WHERE userid = %s AND ISBN = %s
            """, (quantity, user_id, isbn))
        else:
            # adds new record if the book is not in the cart
            cursor.execute("""
                INSERT INTO cart (userid, ISBN, quantity) VALUES (%s, %s, %s)
            """, (user_id, isbn, quantity))
        conn.commit()  # commits changes to the database
        print("Book added to cart!")
    except mysql.connector.Error as e:
        print(f"Database error: {e}")


def search(userid):
    # searches books by titles or author
    try:    # error handling for database error
        print("\n---Search Books---")
        print("1. Search by Title")
        print("2. Search by Author")
        # displays search options
        choice = input("enter your choice: ").strip()
        #  user choice for searching by title or author

        if choice == '1':
            keyword = input('Enter part of the titles: ').strip()
            query = "SELECT Author, Title, ISBN, Price, Subject FROM books WHERE Title LIKE %s"
        elif choice == '2':
            keyword = input('Enter part of the authors name: ').strip()
            query = "SELECT Author, Title, ISBN, Price, Subject FROM books WHERE Author LIKE %s"
        else:
            print('Invalid choice.Return to menu')
            return
        cursor.execute(query, (f"%{keyword}%",))
        # cursos.execute the search query with the provided keyword
        books = cursor.fetchall()
        if not books:   # display search results or no matches found
            print('no books found')
            return
        for book in books:  # print chosen book and its details
            print(f"Author: {book[0]}, Title: {book[1]}, ISBN: {
                  book[2]}, Price: {book[3]}, Subject: {book[4]}")
        # user choice to add a book to the cart from the search results
        isbn = input(
            "\nEnter ISBN to add to cart or press ENTER to go back: ").strip()
        if isbn:
            if len(isbn) != 10:   # validate isbn length
                print('INVALID ISBN.Should be atlest ten characters')
                return
            try:
                # ask for quantity before adding to cart
                quantity = int(input('Enter quantity: '))
                if quantity <= 0:
                    print('Invalid quantity.It must be positive')
                    return
                add_to_cart(userid, isbn, quantity)
            except ValueError:
                print('Invalid input.')
        else:
            print('Returning to menu.')
    except mysql.connector.Error as e:
        print(F'Database error: {e}')

def checkout(userid):   # function that that retrieves cart items displays their cost and allows user to complete purchase
    try:
        # fetches items from the users cart along with book details
        cursor.execute("""
            SELECT c.ISBN, b.Title, c.quantity, b.Price
            FROM cart c
            JOIN books b ON c.ISBN = b.ISBN
            WHERE c.userid = %s
        """, (userid,))
        cartbasket=cursor.fetchall()
        if not cartbasket:  # checks if the cart if empty 
            print('empty cart')
            return
        totalprice=0    # initialize total price
        for item in cartbasket: # iterates through the cartitems to display all the items and calculate the total price
            isbn,title,quantity,price=item  # unpacks tuple item into four variables 
            total=quantity*price
            totalprice+=total
            print(f"ISBN: {isbn}, Title: {title}, Quantity: {quantity}, Price: {price}, Total: {total}")
        print(f'total price: {totalprice}')
        accept=input('accept purchase?(y/n):').strip().lower()  # user choice to confirm purchase
        if accept=='y':
            # inserts new order in the orders table 
            cursor.execute("""
                INSERT INTO orders (Userid, Createdate, shipAddress, shipCity, shipZip)
                VALUES (%s, CURDATE(), 
                (SELECT Address FROM members WHERE Userid = %s),
                (SELECT City FROM members WHERE Userid = %s),
                (SELECT Zip FROM members WHERE Userid = %s))
            """, (userid, userid, userid, userid))
            orderid=cursor.lastrowid  # gets the id of the new order inserted
            for item in cartbasket:  # iterates through the cart to calculate the amount
                isbn,title,quantity,price=item
                amount=quantity*price
                cursor.execute("""
                    INSERT INTO odetails (OrderID, ISBN, quantity, amount) VALUES (%s, %s, %s, %s)
                """, (orderid, isbn, quantity, amount))     # adds items from the cart in the order details table
            cursor.execute("DELETE FROM cart WHERE userid = %s",(userid))   # clears the cart after chckout
            conn.commit()   # commits changes to the database 
            print('check out completed')
            print("\n--- Invoice ---")
            print(f"Order ID: {orderid}")
            print(f"User ID: {userid}")
            print(f"Shipping Address: {address}, {city}, {zip_code}")
            print(f"Order Date: {cursor.execute('SELECT CURDATE()').fetchone()[0]}")
            print(f"Shipment Date: {cursor.execute('SELECT DATE_ADD(CURDATE(), INTERVAL 7 DAY)').fetchone()[0]}")
            print("\nItems:")
            for item in cartbasket:
                isbn, title, quantity, price = item
                total = quantity * price
                print(f"ISBN: {isbn}, Title: {title}, Quantity: {quantity}, Price: {price}, Total: {total}")

            print(f"\nTotal Price: {totalprice}")
            print("\nCheckout completed. Thank you for your purchase!")
        else:
            print('checkout cancelled')
    except mysql.connector.Error as e:
        print(f"database connection error: {e}")


def mainmenu():
    # disaplays the main menu and allows for user interaction
    while True:  # loop for menu options until exiting
        print("\n--- MAIN MENU ---")
        print('1.REGISTER')
        print('2.LOGIN')
        print('3.QUIT')
        choice = input('Enter your choice: ').strip()
        # calls the other functions depending on user choice or exits the program
        if choice == '1':
            registeration()
        elif choice == '2':
            userid = login()
            if userid:
                membermenu(userid)
        elif choice == '3':
            print('exiting the application')
            exit()
        else:
            print('invalid choice ')


def membermenu(userid):     # displays the menu for logged in users
    while True:  # loop for member menu options until termination
        print("\n--- MEMBER MENU ---")
        print('1.BROWSE BY SUBJECT')
        print('2.SEARCH BY TITLE/AUTHOR')
        print('3.CHECKOUT')
        print('4.LOGOUT')
        choice = input('Enter your choice: ').strip()
        # calls the other functions depending on user choice or exits to main menu
        if choice == '1':
            browse_by_subject(userid)
        elif choice == '2':
            search(userid)
        # elif choice=='3':
            # checkout(userid)
        elif choice == '4':
            print('logging out.')
            break
        else:
            print('invalid choice')
