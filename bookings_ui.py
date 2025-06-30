# ui/bookings_ui.py
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import datetime

def open_bookings_ui(conn):
    win = ttk.Toplevel()
    win.title("Manage Bookings")
    win.geometry("750x400")

    def load_bookings():
        for row in tree.get_children():
            tree.delete(row)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Bookings")
        for row in cursor.fetchall():
            tree.insert('', 'end', values=row)
        cursor.close()

    def add_booking():
        customer_id = customer_entry.get()
        room_id = room_entry.get()
        checkin = checkin_entry.get()
        checkout = checkout_entry.get()
        if customer_id and room_id and checkin and checkout:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO Bookings (customer_id, room_id, check_in_date, check_out_date) VALUES (%s, %s, %s, %s)",
                               (customer_id, room_id, checkin, checkout))
                conn.commit()
                load_bookings()
            except Exception as e:
                messagebox.showerror("Error", str(e))
            cursor.close()
        else:
            messagebox.showerror("Input Error", "All fields are required")

    def update_booking():
        selected = tree.selection()
        if selected:
            booking_id = tree.item(selected[0])['values'][0]
            customer_id = customer_entry.get()
            room_id = room_entry.get()
            checkin = checkin_entry.get()
            checkout = checkout_entry.get()
            cursor = conn.cursor()
            cursor.execute("UPDATE Bookings SET customer_id=%s, room_id=%s, check_in_date=%s, check_out_date=%s WHERE booking_id=%s",
                           (customer_id, room_id, checkin, checkout, booking_id))
            conn.commit()
            cursor.close()
            load_bookings()
        else:
            messagebox.showerror("Selection Error", "Please select a booking to update")

    def delete_booking():
        selected = tree.selection()
        if selected:
            booking_id = tree.item(selected[0])['values'][0]
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Bookings WHERE booking_id=%s", (booking_id,))
            conn.commit()
            cursor.close()
            load_bookings()
        else:
            messagebox.showerror("Selection Error", "Please select a booking to delete")

    def on_select(event):
        selected = tree.selection()
        if selected:
            item = tree.item(selected[0])['values']
            customer_entry.delete(0, 'end')
            customer_entry.insert(0, item[1])
            room_entry.delete(0, 'end')
            room_entry.insert(0, item[2])
            checkin_entry.delete(0, 'end')
            checkin_entry.insert(0, item[3])
            checkout_entry.delete(0, 'end')
            checkout_entry.insert(0, item[4])

    form = ttk.Frame(win)
    form.pack(pady=10)

    ttk.Label(form, text="Customer ID:").grid(row=0, column=0, padx=5, pady=5)
    customer_entry = ttk.Entry(form)
    customer_entry.grid(row=0, column=1, padx=5)

    ttk.Label(form, text="Room ID:").grid(row=0, column=2, padx=5, pady=5)
    room_entry = ttk.Entry(form)
    room_entry.grid(row=0, column=3, padx=5)

    ttk.Label(form, text="Check-in Date (YYYY-MM-DD):").grid(row=1, column=0, padx=5, pady=5)
    checkin_entry = ttk.Entry(form)
    checkin_entry.grid(row=1, column=1, padx=5)

    ttk.Label(form, text="Check-out Date (YYYY-MM-DD):").grid(row=1, column=2, padx=5, pady=5)
    checkout_entry = ttk.Entry(form)
    checkout_entry.grid(row=1, column=3, padx=5)

    ttk.Button(form, text="Add", command=add_booking, bootstyle=SUCCESS).grid(row=2, column=0, pady=10)
    ttk.Button(form, text="Update", command=update_booking, bootstyle=WARNING).grid(row=2, column=1)
    ttk.Button(form, text="Delete", command=delete_booking, bootstyle=DANGER).grid(row=2, column=2)

    tree = ttk.Treeview(win, columns=("ID", "Customer ID", "Room ID", "Check-in", "Check-out"), show="headings")
    for col in ("ID", "Customer ID", "Room ID", "Check-in", "Check-out"):
        tree.heading(col, text=col)
        tree.column(col, width=130)
    tree.pack(fill='both', expand=True)
    tree.bind("<<TreeviewSelect>>", on_select)

    load_bookings()
    win.mainloop()