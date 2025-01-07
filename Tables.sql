USE book_store;

CREATE TABLE books(
    ISBN CHAR(10) PRIMARY KEY,
    Author VARCHAR(100),
    Title VARCHAR(200),
    Price  DECIMAL(10,2),
    Subject VARCHAR(100)
);

CREATE TABLE members(
    Userid INT AUTO_INCREMENT PRIMARY KEY,
    Fname VARCHAR(50),
    Lname VARCHAR(50),
    Email VARCHAR(40) UNIQUE,
    Password VARCHAR(200),
    Phone VARCHAR(15) NULL,
    Address VARCHAR(50),
    City VARCHAR(30),
    Zip INT
);

CREATE TABLE orders(
    Orderid INT AUTO_INCREMENT PRIMARY KEY,
    Userid INT,
    Createdate DATE,
    shipAddress VARCHAR(50),
    shipCity VARCHAR(30),
    shipZip INT,
    FOREIGN KEY(Userid) REFERENCES members(Userid)
);

CREATE TABLE odetails(
    odetailID INT AUTO_INCREMENT PRIMARY KEY,
    OrderID INT,
    ISBN CHAR(10),
    quantity INT,
    amount Decimal(10,2),
    FOREIGN KEY (OrderID) REFERENCES orders(OrderID),
    FOREIGN KEY(ISBN) REFERENCES books(ISBN)
);

CREATE TABLE cart(
    userid INT,
    ISBN CHAR(10),
    quantity INT,
    PRIMARY KEY (userid, ISBN),
    FOREIGN KEY (userid) REFERENCES members(Userid),
    FOREIGN KEY (ISBN) REFERENCES books(ISBN)
);

