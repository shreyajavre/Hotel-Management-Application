# db_setup.py

import mysql.connector

def initialize_database():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Jshreya%7"  # Update if your password is different
    )
    cursor = conn.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS HotelDB")
    cursor.execute("USE HotelDB")

    tables = {
        "Staff": """
            CREATE TABLE IF NOT EXISTS Staff (
                staff_id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE,
                password VARCHAR(100),
                role ENUM('admin', 'receptionist', 'accountant') NOT NULL
            )
        """,
        "Customers": """
            CREATE TABLE IF NOT EXISTS Customers (
                customer_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                contact VARCHAR(15),
                email VARCHAR(100)
            )
        """,
        "Rooms": """
            CREATE TABLE IF NOT EXISTS Rooms (
                room_id INT AUTO_INCREMENT PRIMARY KEY,
                room_number VARCHAR(10),
                room_type VARCHAR(50),
                is_available BOOLEAN DEFAULT TRUE,
                price_per_night DECIMAL(10, 2)
            )
        """,
        "Bookings": """
            CREATE TABLE IF NOT EXISTS Bookings (
                booking_id INT AUTO_INCREMENT PRIMARY KEY,
                customer_id INT,
                room_id INT,
                check_in DATE,
                check_out DATE,
                FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
                FOREIGN KEY (room_id) REFERENCES Rooms(room_id)
            )
        """,
        "Billing": """
            CREATE TABLE IF NOT EXISTS Billing (
                bill_id INT AUTO_INCREMENT PRIMARY KEY,
                booking_id INT,
                total_amount DECIMAL(10, 2),
                billing_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (booking_id) REFERENCES Bookings(booking_id)
            )
        """
    }

    for ddl in tables.values():
        cursor.execute(ddl)

    # Insert default admin user if no staff exists
    cursor.execute("SELECT COUNT(*) FROM Staff")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO Staff (username, password, role)
            VALUES ('admin', 'admin123', 'admin')
        """)
        conn.commit()

    cursor.close()
    conn.close()

# ✅ Add this to allow imports from other files
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Jshreya%7",  # Same password as above
        database="HotelDB"
    )
