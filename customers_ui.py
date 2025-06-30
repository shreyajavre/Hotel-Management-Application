# ui/customers_ui.py
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox

def open_customers_ui(conn):
    win = ttk.Toplevel()
    win.title("Manage Customers")
    win.geometry("700x400")

    def load_customers():
        for row in tree.get_children():
            tree.delete(row)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Customers")
        for row in cursor.fetchall():
            tree.insert('', 'end', values=row)
        cursor.close()

    def add_customer():
        name = name_entry.get()
        contact = contact_entry.get()
        email = email_entry.get()
        if name and contact and email:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Customers (name, contact, email) VALUES (%s, %s, %s)",
                           (name, contact, email))
            conn.commit()
            cursor.close()
            load_customers()
        else:
            messagebox.showerror("Input Error", "All fields are required")

    def update_customer():
        selected = tree.selection()
        if selected:
            customer_id = tree.item(selected[0])['values'][0]
            name = name_entry.get()
            contact = contact_entry.get()
            email = email_entry.get()
            cursor = conn.cursor()
            cursor.execute("UPDATE Customers SET name=%s, contact=%s, email=%s WHERE customer_id=%s",
                           (name, contact, email, customer_id))
            conn.commit()
            cursor.close()
            load_customers()
        else:
            messagebox.showerror("Selection Error", "Please select a customer to update")

    def delete_customer():
        selected = tree.selection()
        if selected:
            customer_id = tree.item(selected[0])['values'][0]
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Customers WHERE customer_id=%s", (customer_id,))
            conn.commit()
            cursor.close()
            load_customers()
        else:
            messagebox.showerror("Selection Error", "Please select a customer to delete")

    def on_select(event):
        selected = tree.selection()
        if selected:
            item = tree.item(selected[0])['values']
            name_entry.delete(0, 'end')
            name_entry.insert(0, item[1])
            contact_entry.delete(0, 'end')
            contact_entry.insert(0, item[2])
            email_entry.delete(0, 'end')
            email_entry.insert(0, item[3])

    # Form
    form = ttk.Frame(win)
    form.pack(pady=10)

    ttk.Label(form, text="Name:").grid(row=0, column=0, padx=5, pady=5)
    name_entry = ttk.Entry(form)
    name_entry.grid(row=0, column=1, padx=5)

    ttk.Label(form, text="Contact:").grid(row=0, column=2, padx=5, pady=5)
    contact_entry = ttk.Entry(form)
    contact_entry.grid(row=0, column=3, padx=5)

    ttk.Label(form, text="Email:").grid(row=1, column=0, padx=5, pady=5)
    email_entry = ttk.Entry(form)
    email_entry.grid(row=1, column=1, padx=5)

    ttk.Button(form, text="Add", command=add_customer, bootstyle=SUCCESS).grid(row=2, column=0, pady=10)
    ttk.Button(form, text="Update", command=update_customer, bootstyle=WARNING).grid(row=2, column=1)
    ttk.Button(form, text="Delete", command=delete_customer, bootstyle=DANGER).grid(row=2, column=2)

    # Treeview
    tree = ttk.Treeview(win, columns=("ID", "Name", "Contact", "Email"), show="headings")
    for col in ("ID", "Name", "Contact", "Email"):
        tree.heading(col, text=col)
        tree.column(col, width=150)
    tree.pack(fill='both', expand=True)
    tree.bind("<<TreeviewSelect>>", on_select)

    load_customers()
    win.mainloop()
