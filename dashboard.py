# dashboard.py
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from ui.customers_ui import open_customers_ui
from ui.staff_ui import open_staff_ui
from ui.rooms_ui import open_rooms_ui
from ui.bookings_ui import open_bookings_ui
from ui.billing_ui import open_billing_ui

def open_dashboard(conn, username, role):
    app = ttk.Window(themename="flatly")
    app.title(f"Dashboard - {role.title()} ({username})")
    app.geometry("600x400")

    ttk.Label(app, text=f"Welcome, {username}!", font=("Helvetica", 16, "bold")).pack(pady=20)

    def open_ui(name):
        if name == "Manage Customers":
            open_customers_ui(conn)
        elif name == "Manage Staff":
            open_staff_ui(conn)
        elif name == "Manage Rooms":
            open_rooms_ui(conn)
        elif name == "Manage Bookings":
            open_bookings_ui(conn)
        elif name == "View Billing":
            open_billing_ui(conn)
        else:
            messagebox.showinfo("Info", f"{name} feature coming soon!")

    btn_frame = ttk.Frame(app)
    btn_frame.pack(pady=10)

    if role == "admin":
        buttons = ["Manage Staff", "Manage Customers", "Manage Rooms", "Manage Bookings", "View Billing"]
    elif role == "receptionist":
        buttons = ["Manage Customers", "Manage Rooms", "Manage Bookings"]
    elif role == "accountant":
        buttons = ["View Billing"]
    else:
        buttons = []

    for name in buttons:
        ttk.Button(btn_frame, text=name, bootstyle=INFO, width=25,
                   command=lambda n=name: open_ui(n)).pack(pady=5)

    def logout():
        conn.close()
        app.destroy()

    ttk.Button(app, text="Logout", bootstyle=DANGER, command=logout).pack(pady=20)
    app.mainloop()