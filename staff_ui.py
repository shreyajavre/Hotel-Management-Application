# ui/staff_ui.py
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox

# Updated to accept connection from outside
def open_staff_ui(conn):
    win = ttk.Toplevel()
    win.title("Manage Staff")
    win.geometry("750x400")

    def load_data():
        for row in tree.get_children():
            tree.delete(row)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Staff")
        for row in cursor.fetchall():
            tree.insert('', END, values=row)
        cursor.close()

    def add_staff():
        username, password, role = username_entry.get(), password_entry.get(), role_entry.get()
        if username and password and role:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Staff (username, password, role) VALUES (%s, %s, %s)",
                           (username, password, role))
            conn.commit()
            cursor.close()
            load_data()
        else:
            messagebox.showerror("Input Error", "All fields are required")

    def update_staff():
        selected = tree.selection()
        if selected:
            item = tree.item(selected[0])['values']
            sid = item[0]
            username, password, role = username_entry.get(), password_entry.get(), role_entry.get()
            cursor = conn.cursor()
            cursor.execute("UPDATE Staff SET username=%s, password=%s, role=%s WHERE staff_id=%s",
                           (username, password, role, sid))
            conn.commit()
            cursor.close()
            load_data()
        else:
            messagebox.showerror("Selection Error", "Select a staff member to update")

    def delete_staff():
        selected = tree.selection()
        if selected:
            sid = tree.item(selected[0])['values'][0]
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Staff WHERE staff_id=%s", (sid,))
            conn.commit()
            cursor.close()
            load_data()
        else:
            messagebox.showerror("Selection Error", "Select a staff member to delete")

    def on_select(event):
        selected = tree.selection()
        if selected:
            item = tree.item(selected[0])['values']
            username_entry.delete(0, END)
            username_entry.insert(0, item[1])
            password_entry.delete(0, END)
            password_entry.insert(0, item[2])
            role_entry.delete(0, END)
            role_entry.insert(0, item[3])

    # Form UI
    form = ttk.Frame(win)
    form.pack(pady=10)

    ttk.Label(form, text="Username:").grid(row=0, column=0, padx=5, pady=5)
    username_entry = ttk.Entry(form)
    username_entry.grid(row=0, column=1, padx=5)

    ttk.Label(form, text="Password:").grid(row=0, column=2, padx=5, pady=5)
    password_entry = ttk.Entry(form, show="*")
    password_entry.grid(row=0, column=3, padx=5)

    ttk.Label(form, text="Role:").grid(row=1, column=0, padx=5, pady=5)
    role_entry = ttk.Entry(form)
    role_entry.grid(row=1, column=1, padx=5)

    btn_frame = ttk.Frame(win)
    btn_frame.pack(pady=10)
    ttk.Button(btn_frame, text="Add", command=add_staff, bootstyle=SUCCESS).pack(side=LEFT, padx=5)
    ttk.Button(btn_frame, text="Update", command=update_staff, bootstyle=WARNING).pack(side=LEFT, padx=5)
    ttk.Button(btn_frame, text="Delete", command=delete_staff, bootstyle=DANGER).pack(side=LEFT, padx=5)

    tree = ttk.Treeview(win, columns=("ID", "Username", "Password", "Role"), show="headings")
    for col in ("ID", "Username", "Password", "Role"):
        tree.heading(col, text=col)
        tree.column(col, width=120)
    tree.pack(fill=BOTH, expand=True, pady=10)
    tree.bind("<<TreeviewSelect>>", on_select)

    load_data()
    win.mainloop()
