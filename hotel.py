import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from datetime import datetime

# ====== MySQL Connection ======
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Jshreya%7"  # Replace with your MySQL password
)
cursor = conn.cursor()

# ====== Create Database & Tables if not exist ======
cursor.execute("CREATE DATABASE IF NOT EXISTS HotelDB")
cursor.execute("USE HotelDB")

tables = {
    "Staff": """
        CREATE TABLE IF NOT EXISTS Staff (
            staff_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE,
            password VARCHAR(100)
        )
    """,
    "Customers": """
        CREATE TABLE IF NOT EXISTS Customers (
            customer_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            phone VARCHAR(15),
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

# Insert default staff user if none exists
cursor.execute("SELECT COUNT(*) FROM Staff")
if cursor.fetchone()[0] == 0:
    cursor.execute("INSERT INTO Staff (username, password) VALUES ('admin', 'admin123')")
    conn.commit()

# ====== GUI Logic ======
def launch_main_app():
    login_window.destroy()

    # ---- Main App Window ----
    root = tk.Tk()
    root.title("Hotel Management System")
    root.geometry("600x500")

    def add_customer():
        def submit():
            name = entry_name.get()
            phone = entry_phone.get()
            email = entry_email.get()
            cursor.execute("INSERT INTO Customers (name, phone, email) VALUES (%s, %s, %s)", (name, phone, email))
            conn.commit()
            messagebox.showinfo("Success", "Customer Added")
            top.destroy()

        top = tk.Toplevel(root)
        top.title("Add Customer")

        tk.Label(top, text="Name").grid(row=0, column=0)
        entry_name = tk.Entry(top)
        entry_name.grid(row=0, column=1)

        tk.Label(top, text="Phone").grid(row=1, column=0)
        entry_phone = tk.Entry(top)
        entry_phone.grid(row=1, column=1)

        tk.Label(top, text="Email").grid(row=2, column=0)
        entry_email = tk.Entry(top)
        entry_email.grid(row=2, column=1)

        tk.Button(top, text="Submit", command=submit).grid(row=3, columnspan=2, pady=10)

    def show_rooms():
        cursor.execute("SELECT * FROM Rooms WHERE is_available = TRUE")
        rooms = cursor.fetchall()

        top = tk.Toplevel(root)
        top.title("Available Rooms")

        tree = ttk.Treeview(top, columns=('Room ID', 'Number', 'Type', 'Available', 'Price'), show='headings')
        for col in tree["columns"]:
            tree.heading(col, text=col)
        for row in rooms:
            tree.insert('', tk.END, values=row)
        tree.pack(expand=True, fill='both')

    def book_room():
        def submit():
            cid = entry_cid.get()
            rid = entry_rid.get()
            checkin = entry_checkin.get()
            checkout = entry_checkout.get()

            cursor.execute("INSERT INTO Bookings (customer_id, room_id, check_in, check_out) VALUES (%s, %s, %s, %s)",
                        (cid, rid, checkin, checkout))
            cursor.execute("UPDATE Rooms SET is_available = FALSE WHERE room_id = %s", (rid,))
            conn.commit()
            messagebox.showinfo("Success", "Room Booked")
            top.destroy()

        top = tk.Toplevel(root)
        top.title("Book Room")

        tk.Label(top, text="Customer ID").grid(row=0, column=0)
        entry_cid = tk.Entry(top)
        entry_cid.grid(row=0, column=1)

        tk.Label(top, text="Room ID").grid(row=1, column=0)
        entry_rid = tk.Entry(top)
        entry_rid.grid(row=1, column=1)

        tk.Label(top, text="Check-in (YYYY-MM-DD)").grid(row=2, column=0)
        entry_checkin = tk.Entry(top)
        entry_checkin.grid(row=2, column=1)

        tk.Label(top, text="Check-out (YYYY-MM-DD)").grid(row=3, column=0)
        entry_checkout = tk.Entry(top)
        entry_checkout.grid(row=3, column=1)

        tk.Button(top, text="Submit", command=submit).grid(row=4, columnspan=2, pady=10)

    def generate_bill():
        def submit():
            bid = int(entry_bid.get())
            cursor.execute("SELECT check_in, check_out, room_id FROM Bookings WHERE booking_id = %s", (bid,))
            check_in, check_out, room_id = cursor.fetchone()
            days = (check_out - check_in).days
            cursor.execute("SELECT price_per_night FROM Rooms WHERE room_id = %s", (room_id,))
            rate = cursor.fetchone()[0]
            total = rate * days
            cursor.execute("INSERT INTO Billing (booking_id, total_amount) VALUES (%s, %s)", (bid, total))
            conn.commit()
            messagebox.showinfo("Bill Generated", f"Total: ₹{total:.2f}")
            top.destroy()

        top = tk.Toplevel(root)
        top.title("Generate Bill")

        tk.Label(top, text="Booking ID").grid(row=0, column=0)
        entry_bid = tk.Entry(top)
        entry_bid.grid(row=0, column=1)

        tk.Button(top, text="Generate", command=submit).grid(row=1, columnspan=2, pady=10)

    def generate_report():
        cursor.execute("""
            SELECT b.booking_id, c.name, r.room_number, b.check_in, b.check_out, bill.total_amount
            FROM Bookings b
            JOIN Customers c ON b.customer_id = c.customer_id
            JOIN Rooms r ON b.room_id = r.room_id
            JOIN Billing bill ON bill.booking_id = b.booking_id
        """)
        report = cursor.fetchall()

        top = tk.Toplevel(root)
        top.title("Report")

        tree = ttk.Treeview(top, columns=('Booking ID', 'Name', 'Room', 'Check-in', 'Check-out', 'Amount'), show='headings')
        for col in tree["columns"]:
            tree.heading(col, text=col)
        for row in report:
            tree.insert('', tk.END, values=row)
        tree.pack(expand=True, fill='both')

    def logout():
        root.destroy()
        show_login()

    # ---- Buttons ----
    tk.Button(root, text="➕ Add Customer", width=20, command=add_customer).pack(pady=10)
    tk.Button(root, text="📋 Show Available Rooms", width=20, command=show_rooms).pack(pady=10)
    tk.Button(root, text="🛏️ Book Room", width=20, command=book_room).pack(pady=10)
    tk.Button(root, text="🧾 Generate Bill", width=20, command=generate_bill).pack(pady=10)
    tk.Button(root, text="📊 Generate Report", width=20, command=generate_report).pack(pady=10)
    tk.Button(root, text="🔓 Logout", width=20, command=logout).pack(pady=10)

# ====== Login Window ======
def show_login():
    global login_window
    login_window = tk.Tk()
    login_window.title("Staff Login")
    login_window.geometry("300x200")

    tk.Label(login_window, text="Username").pack()
    entry_user = tk.Entry(login_window)
    entry_user.pack()

    tk.Label(login_window, text="Password").pack()
    entry_pass = tk.Entry(login_window, show="*")
    entry_pass.pack()

    def attempt_login():
        user = entry_user.get()
        pwd = entry_pass.get()
        cursor.execute("SELECT * FROM Staff WHERE username=%s AND password=%s", (user, pwd))
        result = cursor.fetchone()
        if result:
            launch_main_app()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    tk.Button(login_window, text="Login", command=attempt_login).pack(pady=10)
    login_window.mainloop()

# Start login window
show_login()