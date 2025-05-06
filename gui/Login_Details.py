import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

class LoginDetailsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Details")
        self.root.geometry("620x503")
        self.root.resizable(False, False)

        # Connect to database
        self.con = self.get_db_connection()

        # Header Panel
        self.header_frame = tk.Frame(self.root, bg="#666666")
        self.header_frame.pack(fill=tk.X)

        self.title_label = tk.Label(self.header_frame, text="Login Details Form", font=("Tahoma", 24, "bold"), bg="#666666", fg="white")
        self.title_label.pack(pady=10)

        # Filters Panel
        self.filters_frame = tk.Frame(self.root, bg="#333333")
        self.filters_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(self.filters_frame, text="User Name:", bg="#333333", fg="white").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.username_combo = ttk.Combobox(self.filters_frame, state="readonly")
        self.username_combo.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.filters_frame, text="Login Date:", bg="#333333", fg="white").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.day_combo = ttk.Combobox(self.filters_frame, values=["Day:"] + [f"{i:02}" for i in range(1, 32)], state="readonly")
        self.day_combo.grid(row=0, column=3, padx=5, pady=5)
        self.month_combo = ttk.Combobox(self.filters_frame, values=["Month:"] + [f"{i:02}" for i in range(1, 13)], state="readonly")
        self.month_combo.grid(row=0, column=4, padx=5, pady=5)
        self.year_combo = ttk.Combobox(self.filters_frame, values=["Year:"] + [str(i) for i in range(2016, 2041)], state="readonly")
        self.year_combo.grid(row=0, column=5, padx=5, pady=5)

        self.username_combo.bind("<<ComboboxSelected>>", self.filter_login_details)
        self.day_combo.bind("<<ComboboxSelected>>", self.filter_login_details)
        self.month_combo.bind("<<ComboboxSelected>>", self.filter_login_details)
        self.year_combo.bind("<<ComboboxSelected>>", self.filter_login_details)

        # Table Panel
        self.table_frame = tk.Frame(self.root, bg="#333333")
        self.table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(self.table_frame, columns=("Name", "Type", "Date", "Time"), show="headings")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Time", text="Time")

        for col in ("Name", "Type", "Date", "Time"):
            self.tree.column(col, anchor=tk.CENTER, width=120)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Load initial data
        self.fill_username()
        self.load_login_details()

    def get_db_connection(self):
        try:
            return mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="dbpharma"
            )
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error connecting to database: {str(e)}")
            return None

    def fill_username(self):
        try:
            cursor = self.con.cursor()
            cursor.execute("SELECT NAME FROM users")
            rows = cursor.fetchall()
            self.username_combo["values"] = ["User Name:"] + [row[0] for row in rows]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load usernames: {str(e)}")

    def load_login_details(self, query=None):
        if not query:
            query = "SELECT NAME, TYPE, DATE, TIME FROM login"

        try:
            cursor = self.con.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()

            # Clear the table
            for row in self.tree.get_children():
                self.tree.delete(row)

            # Insert rows into the table
            for row in rows:
                self.tree.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load login details: {str(e)}")

    def filter_login_details(self, event):
        username = self.username_combo.get()
        day = self.day_combo.get()
        month = self.month_combo.get()
        year = self.year_combo.get()

        query = "SELECT NAME, TYPE, DATE, TIME FROM login WHERE 1=1"
        if username != "User Name:":
            query += f" AND NAME='{username}'"
        if day != "Day:" and month != "Month:" and year != "Year:":
            query += f" AND DATE='{day}-{month}-{year}'"

        self.load_login_details(query)

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginDetailsApp(root)
    root.mainloop()
