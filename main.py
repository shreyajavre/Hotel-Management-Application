# main.py
from login import show_login
from db_setup import get_connection, initialize_database
from dashboard import open_dashboard

if __name__ == "__main__":
    # Ensure database and tables are created
    initialize_database()

    # Show login screen and get session info
    conn, username, role = show_login()

    # Only proceed if login was successful
    if conn and username and role:
        open_dashboard(conn, username, role)
