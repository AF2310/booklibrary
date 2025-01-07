import mysql.connector

conn = mysql.connector.connect(host="localhost", user="root", password="010580sis", database="book_store")
cursor=conn.cursor()

def browse_by_subject(userid):
    cursor.execute("SELECT DISTINCT Subject FROM books ORDER BY Subject")
    subjects = cursor.fetchall()
    for i,subject in enumerate(subjects,1):
        print(f'{i}.{subject[0]}')
    choice = int(input('Enter a choice:'))-1
    choice_subject=subjects[choice][0]
    cursor.execute("""
        SELECT COUNT(*) FROM books WHERE Subject = %s
    """,(choice_subject,))
    book_count = cursor.fetchone()[0]
    print(f'{book_count} books available for this subject')

    cursor.execute("""
    SELECT Author,Title,ISBN,Price,Subject FROM books WHERE Subject=%s  
    """,(choice_subject,))
    all_books=cursor.fetchall()
    books_per_page=2
    current_page=0
    total_books=len(all_books)
    while True:
        start_index = current_page * books_per_page
        end_index = start_index + books_per_page
        page_books = all_books[start_index:end_index]

        for i,book in enumerate(page_books,start=start_index+1):
            print(f'{i}:')
            print(f'Author:\t{book[0]}')
            print(f'Title:\t{book[1]}')
            print(f'ISBN:\t{book[2]}')
            print(f'Price:\t{book[3]}')
            print(f'Subjects:\t{book[4]}')
        if end_index < total_books:
            print("\n Enter ISBN to add to cart or enter 'n' to browse enter Enter to go back")
        else:
            print("\nNo more books to display. Enter ISBN to add to cart or press Enter to return to the main menu.")
        user_input = input("Enter your choice: ")
        if user_input == 'n' and end_index < total_books:
            current_page += 1
        elif not user_input:
            print("Returning to main menu...")
            browse_by_subject(userid)
        if int(len(user_input))==10:
            user_quantity=int(input('Enter a quantity:'))
            add_to_cart(userid,user_input,user_quantity)
        else:
            print("Invalid input. Try again.")

def add_to_cart(id,isbn,quantity):
    cursor.execute("""
    SELECT * FROM cart WHERE userid= %s AND ISBN = %s
    """,(id,isbn))
    existing_item = cursor.fetchone()
    if existing_item:
        cursor.execute("""
        UPDATE cart SET QUANTITY=QUANTITY+%s WHERE userid=%s AND ISBN=%s 
        """,(quantity,id,isbn))
    else:
        cursor.execute("""
        INSERT INTO cart (userid,ISBN,quantity) VALUES(%s,%s,%s)
        """,(id,isbn,quantity))
    conn.commit()
    print("Book added to cart!")


#def main():
 #   userid = login()
  #  if userid:
   #     while True:
    #        choice = input("Enter your choice: ")

     #       if choice == '1':
      #          browse_by_subject(userid)
       #     elif choice == '2':
        #        print("Goodbye!")
         #       break
          #  else:
           #     print("Invalid choice. Please try again.")
    #else:
     #   print("Login failed. Exiting.")

#main()