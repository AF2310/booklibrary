from prettytable import PrettyTable
import mysql.connector
conn = mysql.connector.connect(host="localhost", user="root", password="010580sis", database="book_store")
from datetime import date

cursor= conn.cursor()
today=date.today()
def check_out(userid):
    cursor.execute("""
    SELECT Books.ISBN, Books.Title, Books.Price, Cart.Quantity
    FROM Cart
    JOIN Books ON Cart.ISBN = Books.ISBN
    WHERE Cart.UserID = %s
    """,userid)
    # Fetch ISBN, Title, Price, and Quantity of items in the user's cart

    items=cursor.fetchall()

    print('Current cart contents:')
    # Initialize total price calculation
    total_price=0
    final_price=0

    # Creating a table with headers using PrettyTable
    myTable=PrettyTable(["ISBN","Title","Price","Qty","Total"])
    # Iterate through each item in the cart
    for item in items:
        final_price+=item[3]*item[2]
        total_price+=final_price # Add to grand total
        # Add the item details to the table
        myTable.add_row([item[0],item[1],item[2],item[3],final_price])
        final_price=0
    # Display the cart in table format
    print(myTable)
    print('Total=',total_price)

def invoice(userid):
    # Fetch ISBN, Title, Price, and Quantity of items in the user's cart
    cursor.execute("""
        SELECT Books.ISBN, Books.Title, Books.Price, Cart.Quantity
        FROM Cart
        JOIN Books ON Cart.ISBN = Books.ISBN
        WHERE Cart.UserID = %s
        """, userid)
    items = cursor.fetchall()

    # Fetch user details (First Name, Last Name, Address, City, Zip) for shipping
    cursor.execute("""
            SELECT Fname,Lname,Address,City,Zip
            FROM members
            WHERE Userid = %s
            """, (userid[0],))
    user_details = cursor.fetchone()

    # Insert a new order into the 'orders' table
    cursor.execute("""
    INSERT INTO orders(Userid,Createdate,ShipDate,shipAddress,shipCity,shipZip)
    VALUES(%s,CURDATE(), DATE_ADD(CURDATE(), INTERVAL 7 DAY),%s,%s,%s)
    """,(userid[0],user_details[2],user_details[3],user_details[4]))

    cursor.execute("SELECT DATE_ADD(CURDATE(), INTERVAL 7 DAY)")
    shipment_date = cursor.fetchone()[0]
    print(f"Ship Date: {shipment_date}")

    conn.commit()
    # Get the Order ID of the newly created order
    order_id=cursor.lastrowid

    # Insert each item in the cart into 'odetails' (Order Details) table
    for item in items:
        cursor.execute("""
        INSERT INTO odetails(OrderID,ISBN,quantity,amount)
        VALUES(%s,%s,%s,%s)
        """,(order_id,item[0],item[3],item[2]*item[3]))
        conn.commit()

    # Display the Invoice Header
    print('\t\t\tInvoice Order no.:')
    print('Shipping Address')
    print(f'Name:\t\t{user_details[0]}\t{user_details[1]}')
    print(f'Address:\t  {user_details[2]}\n\t\t\t{user_details[3]}\n\t\t\t{user_details[4]}')

    # Initialize total price calculation

    final_check_out_price=0

    check_out_price=0

    # Creating a table with headers for the invoice
    myTable=PrettyTable(['ISBN','Title','€','Qty','Total'])

    # Iterate through each item and calculate total
    for books in items:
            check_out_price += books[3] * books[2]
            final_check_out_price+=check_out_price
            # Add the item details to the invoice table
            myTable.add_row([books[0],books[1],books[2],books[3],check_out_price])
            check_out_price=0
    # Display the invoice table
    print(myTable)
    print('Total=', final_check_out_price)

    cursor.execute("""
       DELETE FROM Cart WHERE UserID = %s
       """, userid)
    conn.commit()
    print("Checkout complete! Your cart has been cleared.")


