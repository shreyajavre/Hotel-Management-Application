import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import tkinter as tk  # ✅ Needed for StringVar

def open_rooms_ui(conn):
    win = ttk.Toplevel()
    win.title("Manage Rooms")
    win.geometry("700x400")

    def load_rooms():
        for row in tree.get_children():
            tree.delete(row)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Rooms")
        for row in cursor.fetchall():
            tree.insert('', 'end', values=row)
        cursor.close()

    def add_room():
        number = room_number_entry.get()
        room_type = room_type_entry.get()
        status = status_var.get() == "Available"  # ✅ Convert to boolean
        price = price_entry.get()
        if number and room_type and price:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO Rooms (room_number, room_type, is_available, price_per_night) VALUES (%s, %s, %s, %s)",
                    (number, room_type, status, price)
                )
                conn.commit()
                cursor.close()
                load_rooms()
                clear_form() # ✅ Clear the input fields after adding
            except Exception as e:
                messagebox.showerror("Database Error", str(e))
        else:
            messagebox.showerror("Input Error", "All fields are required")

    def update_room():
        selected = tree.selection()
        if selected:
            room_id = tree.item(selected[0])['values'][0]
            number = room_number_entry.get()
            room_type = room_type_entry.get()
            status = status_var.get() == "Available"  # ✅ Convert to boolean
            price = price_entry.get()
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE Rooms SET room_number=%s, room_type=%s, is_available=%s, price_per_night=%s WHERE room_id=%s",
                    (number, room_type, status, price, room_id)
                )
                conn.commit()
                cursor.close()
                load_rooms()
                clear_form() # ✅ Clear the input fields after updating
            except Exception as e:
                messagebox.showerror("Database Error", str(e))
        else:
            messagebox.showerror("Selection Error", "Please select a room to update")

    def delete_room():
        selected = tree.selection()
        if selected:
            room_id = tree.item(selected[0])['values'][0]
            if messagebox.askyesno("Confirm", "Are you sure you want to delete this room?"): # ✅ Add confirmation
                try:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM Rooms WHERE room_id=%s", (room_id,))
                    conn.commit()
                    cursor.close()
                    load_rooms()
                    clear_form() # ✅ Clear the input fields after deleting
                except Exception as e:
                    messagebox.showerror("Database Error", str(e))
        else:
            messagebox.showerror("Selection Error", "Please select a room to delete")

    def on_select(event):
        selected = tree.selection()
        if selected:
            item = tree.item(selected[0])['values']
            room_number_entry.delete(0, 'end')
            room_number_entry.insert(0, item[1])
            room_type_entry.delete(0, 'end')
            room_type_entry.insert(0, item[2])
            status_var.set("Available" if item[3] else "Occupied")  # ✅ Reverse conversion
            price_entry.delete(0, 'end')
            price_entry.insert(0, item[4])

    def clear_form(): # ✅ Function to clear the input fields
        room_number_entry.delete(0, 'end')
        room_type_entry.delete(0, 'end')
        status_var.set("Available")
        price_entry.delete(0, 'end')

    # Form UI
    form = ttk.Frame(win)
    form.pack(pady=10)

    ttk.Label(form, text="Room No:").grid(row=0, column=0, padx=5, pady=5)
    room_number_entry = ttk.Entry(form)
    room_number_entry.grid(row=0, column=1, padx=5)

    ttk.Label(form, text="Type:").grid(row=0, column=2, padx=5, pady=5)
    room_type_entry = ttk.Entry(form)
    room_type_entry.grid(row=0, column=3, padx=5)

    ttk.Label(form, text="Status:").grid(row=1, column=0, padx=5, pady=5)
    status_var = tk.StringVar(value="Available") # ✅ Use StringVar for Combobox
    status_combo = ttk.Combobox(form, textvariable=status_var, values=["Available", "Occupied"]) # ✅ Use Combobox
    status_combo.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(form, text="Price:").grid(row=1, column=2, padx=5, pady=5)
    price_entry = ttk.Entry(form)
    price_entry.grid(row=1, column=3, padx=5)

    button_frame = ttk.Frame(form) # ✅ Frame to group buttons
    button_frame.grid(row=2, column=0, columnspan=4, pady=10)

    ttk.Button(button_frame, text="Add", command=add_room, bootstyle=SUCCESS).pack(side=LEFT, padx=5)
    ttk.Button(button_frame, text="Update", command=update_room, bootstyle=WARNING).pack(side=LEFT, padx=5)
    ttk.Button(button_frame, text="Delete", command=delete_room, bootstyle=DANGER).pack(side=LEFT, padx=5)
    ttk.Button(button_frame, text="Clear", command=clear_form, bootstyle=INFO).pack(side=LEFT, padx=5) # ✅ Add clear button

    tree = ttk.Treeview(win, columns=("ID", "Room No", "Type", "Available", "Price"), show="headings")
    for col in ("ID", "Room No", "Type", "Available", "Price"):
        tree.heading(col, text=col)
        tree.column(col, width=100)
    tree.pack(fill='both', expand=True)
    tree.bind("<<TreeviewSelect>>", on_select)

    load_rooms()
    win.mainloop()