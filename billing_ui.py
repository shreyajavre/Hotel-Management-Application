# ui/billing_ui.py
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox

def open_billing_ui(conn):
    win = ttk.Toplevel()
    win.title("Manage Billing")
    win.geometry("750x400")

    def load_billing():
        for row in tree.get_children():
            tree.delete(row)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Billing")
        for row in cursor.fetchall():
            tree.insert('', 'end', values=row)
        cursor.close()

    def add_billing():
        booking_id = booking_entry.get()
        amount = amount_entry.get()
        status = status_entry.get()
        date = date_entry.get()
        if booking_id and amount and status and date:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO Billing (booking_id, amount, status, date_issued) VALUES (%s, %s, %s, %s)",
                               (booking_id, amount, status, date))
                conn.commit()
                load_billing()
            except Exception as e:
                messagebox.showerror("Error", str(e))
            cursor.close()
        else:
            messagebox.showerror("Input Error", "All fields are required")

    def update_billing():
        selected = tree.selection()
        if selected:
            billing_id = tree.item(selected[0])['values'][0]
            booking_id = booking_entry.get()
            amount = amount_entry.get()
            status = status_entry.get()
            date = date_entry.get()
            cursor = conn.cursor()
            cursor.execute("UPDATE Billing SET booking_id=%s, amount=%s, status=%s, date_issued=%s WHERE billing_id=%s",
                           (booking_id, amount, status, date, billing_id))
            conn.commit()
            cursor.close()
            load_billing()
        else:
            messagebox.showerror("Selection Error", "Please select a billing record to update")

    def delete_billing():
        selected = tree.selection()
        if selected:
            billing_id = tree.item(selected[0])['values'][0]
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Billing WHERE billing_id=%s", (billing_id,))
            conn.commit()
            cursor.close()
            load_billing()
        else:
            messagebox.showerror("Selection Error", "Please select a billing record to delete")

    def on_select(event):
        selected = tree.selection()
        if selected:
            item = tree.item(selected[0])['values']
            booking_entry.delete(0, 'end')
            booking_entry.insert(0, item[1])
            amount_entry.delete(0, 'end')
            amount_entry.insert(0, item[2])
            status_entry.delete(0, 'end')
            status_entry.insert(0, item[3])
            date_entry.delete(0, 'end')
            date_entry.insert(0, item[4])

    form = ttk.Frame(win)
    form.pack(pady=10)

    ttk.Label(form, text="Booking ID:").grid(row=0, column=0, padx=5, pady=5)
    booking_entry = ttk.Entry(form)
    booking_entry.grid(row=0, column=1, padx=5)

    ttk.Label(form, text="Amount:").grid(row=0, column=2, padx=5, pady=5)
    amount_entry = ttk.Entry(form)
    amount_entry.grid(row=0, column=3, padx=5)

    ttk.Label(form, text="Status:").grid(row=1, column=0, padx=5, pady=5)
    status_entry = ttk.Entry(form)
    status_entry.grid(row=1, column=1, padx=5)

    ttk.Label(form, text="Date (YYYY-MM-DD):").grid(row=1, column=2, padx=5, pady=5)
    date_entry = ttk.Entry(form)
    date_entry.grid(row=1, column=3, padx=5)

    ttk.Button(form, text="Add", command=add_billing, bootstyle=SUCCESS).grid(row=2, column=0, pady=10)
    ttk.Button(form, text="Update", command=update_billing, bootstyle=WARNING).grid(row=2, column=1)
    ttk.Button(form, text="Delete", command=delete_billing, bootstyle=DANGER).grid(row=2, column=2)

    tree = ttk.Treeview(win, columns=("ID", "Booking ID", "Amount", "Status", "Date"), show="headings")
    for col in ("ID", "Booking ID", "Amount", "Status", "Date"):
        tree.heading(col, text=col)
        tree.column(col, width=130)
    tree.pack(fill='both', expand=True)
    tree.bind("<<TreeviewSelect>>", on_select)

    load_billing()
    win.mainloop()