# login.py
import mysql.connector
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from db_setup import initialize_database

def show_login():
    initialize_database()

    login_success = {"conn": None, "username": None, "role": None}

    app = ttk.Window(themename="cosmo")
    app.title("Hotel Management Login")
    app.geometry("400x300")

    ttk.Label(app, text="Login", font=("Helvetica", 20, "bold")).pack(pady=20)

    frm = ttk.Frame(app)
    frm.pack(pady=10)

    ttk.Label(frm, text="Username:").grid(row=0, column=0, sticky=W, padx=5, pady=5)
    username_entry = ttk.Entry(frm)
    username_entry.grid(row=0, column=1, padx=5)

    ttk.Label(frm, text="Password:").grid(row=1, column=0, sticky=W, padx=5, pady=5)
    password_entry = ttk.Entry(frm, show="*")
    password_entry.grid(row=1, column=1, padx=5)

    def attempt_login():
        username = username_entry.get()
        password = password_entry.get()

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Jshreya%7",
                database="HotelDB"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT role FROM Staff WHERE username=%s AND password=%s", (username, password))
            result = cursor.fetchone()

            if result:
                role = result[0]
                login_success["conn"] = conn
                login_success["username"] = username
                login_success["role"] = role
                app.destroy()
            else:
                messagebox.showerror("Login Failed", "Invalid username or password")
                conn.close()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))

    ttk.Button(app, text="Login", bootstyle=PRIMARY, command=attempt_login).pack(pady=10)
    app.mainloop()

    return login_success["conn"], login_success["username"], login_success["role"]
