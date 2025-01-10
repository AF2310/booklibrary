import mysql.connector
from getpass import getpass
from Member_menu import browse_by_subject,add_to_cart
from check_out import check_out,invoice


conn = mysql.connector.connect(host="localhost", user="root", password="010580sis", database="book_store")
cursor=conn.cursor()


# Function for new member registration

def registeration():
    fname = input('Enter first name:')
    lname = input('Enter last name:')
    email = input('Enter email:')
    password = getpass('Enter password:') # Use getpass for secure password entry
    address = input('Enter street address:')
    city = input('Enter city name:')
    zip_code = int(input('Enter zip code:'))
    phone = int(input('Enter phone number:'))

    # Insert the new member's details into the Members table

    cursor.execute("""
    INSERT INTO Members(Fname, Lname, Email, Password, Address, City, Zip ,Phone)    
    VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
    """,(fname,lname,email,password,address,city,zip_code,phone))
    conn.commit()
    print("You have registered successfully!")
    choice()

n=64

def login():
    email = input('Enter email:')
    password = getpass('Enter password:')

    # Query to verify user credentials
    cursor.execute("""
            SELECT Userid FROM members WHERE Email = %s AND Password = %s
        """, (email, password))
    user = cursor.fetchone() # Fetch user ID if credentials match

    if user:
        user_id = user
        print("Login successful!")
        return user_id
    else:
        print("Incorrect email or password. Please try again.")
        return None


def member_menu(userid):
    while True:
        print('*' * 64)
        print('*** \t\t\t\t\t\t\t\t\t\t\t\t\t\t ***')
        print(f'*** \t\t\tWelcome to the Online Store,!\t\t\t\t ***')
        print('*** \t\t\t\t\tMember Menu\t\t\t\t\t\t\t ***')
        print('*** \t\t\t\t\t\t\t\t\t\t\t\t\t\t ***')
        print('*' * 64)
        print('\t\t\t\t1. Browse by Subject')
        print('\t\t\t\t2. Search by Author/Title')
        print('\t\t\t\t3. Check Out')
        print('\t\t\t\t4. Logout')

        user_choice_login = input("Enter your choice: ")

        if user_choice_login == '1':
            browse_by_subject(userid[0])        # Redirect to browse books by subject
            return member_menu(userid) # Recursively return to menu after browsing
        elif user_choice_login == '2':
            search(userid[0])         # Redirect to search by author/title function
        elif user_choice_login == '3':
            check_out(userid)        # Handle checkout process
            to_checkout = input('Proceed to check out(Y/N):')
            while True:
                if to_checkout.lower() == 'y':
                    invoice(userid)                # Generate invoice if user proceeds to checkout
                    to_exit = input("Press 'n' to go back to the menu:")
                    while True:
                        if to_exit == 'n': # Exit back to the menu
                            exit(member_menu(userid))
                        else:
                            to_exit = input("Press 'n' to go back to the menu:")
                if to_checkout.lower() == 'n':
                        member_menu(userid)
                else:
                    # Handle invalid input and loop back to checkout options
                    print('Please input the correct choice')
                    check_out(userid)
                    to_checkout = input('Proceed to check out(Y/N):')
        elif user_choice_login == '4':
            exit(choice())         # Log out and redirect to the main choice menu
        else:
            print('Please input the correct choice')


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
            print(f"Author: {book[0]}\nTitle: {book[1]}\n ISBN: {
                  book[2]}\n Price: {book[3]}\n Subject: {book[4]}\t")
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
                choose = input("enter 1  to go back to menu or 2 to add books: ").strip()
                if choose=='1':
                    return
                elif choose=='2':
                    return search(userid)
                else:
                    print('invalid choice try again')
                    return search(userid)
            except ValueError:
                print('Invalid input.')
        else:
            print('Returning to menu.')
            return
    except mysql.connector.Error as e:
        print(F'Database error: {e}')


def choice():

    print('*' * n)
    print('*** \t\t\t\t\t\t\t\t\t\t\t\t\t\t ***')
    print('*** \t\t\tWelcome to the Online Store\t\t\t\t\t ***')
    print('*** \t\t\t\t\t\t\t\t\t\t\t\t\t\t ***')
    print('*' * n)
    print('\t\t\t\t\t1.Member Login')
    print('\t\t\t\t\t2.New Member Registration')
    print('\t\t\t\t\tq.quit')
    user_choice=input('Type in your option:')

    if user_choice == '1':
        userid = login()
        if userid:
            return member_menu(userid)
        else:
            print("Login failed. Please try again.")
            return choice()
    elif user_choice == '2':
        registeration()
    elif user_choice.lower()== 'q':
        print('Quiting....')
        exit()
    else:
        print('Please type in the correct option')
        choice()

choice()