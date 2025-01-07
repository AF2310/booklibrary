
import mysql.connector
from getpass import getpass
from Member_menu import browse_by_subject

conn = mysql.connector.connect(host="localhost", user="root", password="010580sis", database="book_store")
cursor=conn.cursor()

def registeration():
    fname = input('Enter first name:')
    lname = input('Enter last name:')
    email = input('Enter email:')
    password = getpass('Enter password:')
    address = input('Enter street address:')
    city = input('Enter city name:')
    zip_code = int(input('Enter zip code:'))
    phone = int(input('Enter phone number:'))

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


    cursor.execute("""
            SELECT Userid FROM members WHERE Email = %s AND Password = %s
        """, (email, password))
    user = cursor.fetchone()

    if user:
        user_id = user
        print("Login successful!")
        print('*' * 50)
        print('*** \t\t\t\t\t\t\t\t\t\t\t\t\t\t ***')
        print(f'*** \t\t\tWelcome to the Online Store,!\t\t\t\t ***')
        print('*** \t\t\t\t\tMember Menu\t\t\t\t\t\t\t ***')
        print('*** \t\t\t\t\t\t\t\t\t\t\t\t\t\t ***')
        print('*' * 50)
        print('\t\t\t\t1. Browse by Subject')
        print('\t\t\t\t2. Search by Author/Title')
        print('\t\t\t\t3. Check Out')
        print('\t\t\t\t4. Logout')

        return user_id[0]
    else:
        print("Incorrect email or password. Please try again.")
        return None

print('*'*n)
print('*** \t\t\t\t\t\t\t\t\t\t\t\t\t\t ***')
print('*** \t\t\tWelcome to the Online Store\t\t\t\t\t ***')
print('*** \t\t\t\t\t\t\t\t\t\t\t\t\t\t ***')
print('*'*n)

def choice():
    print('\t\t\t\t\t1.Member Login')
    print('\t\t\t\t\t2.New Member Registration')
    print('\t\t\t\t\tq.quit')
    user_choice=input('Type in your option:')
    while True:
        if user_choice == '1':
            userid=login()
            if userid:
                while True:
                    user_choice_login = input("Enter your choice: ")
                    if user_choice_login == '1':
                        browse_by_subject(userid)
                    elif not user_choice_login :
                        print("Goodbye!")
                        exit(choice())
                    else:
                        print("Invalid choice. Please try again.")
            else:
                print("Login failed. Exiting.")
            break
        if user_choice == '2':
            registeration()
        if not user_choice.lower():
            print('Quiting....')
            exit()
        else:
            print('Please type in the correct option')
            choice()

choice()