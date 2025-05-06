import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

class WarningList(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Close to Expiration")
        self.geometry("600x400")

        # Main Frame
        main_frame = tk.Frame(self, bg="#333333")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Header Panel
        header_panel = tk.Frame(main_frame, bg="#666666")
        header_panel.pack(fill=tk.X, padx=10, pady=10)

        header_label = tk.Label(
            header_panel, 
            text="Close to Expiration", 
            font=("Tahoma", 24), 
            bg="#666666", 
            fg="white"
        )
        header_label.pack()

        # Table Panel
        table_panel = tk.Frame(main_frame, bg="#333333")
        table_panel.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Scrollable Table
        self.tree = ttk.Treeview(
            table_panel, 
            columns=("Name", "Barcode", "Expiry", "Price", "Quantity"), 
            show="headings"
        )
        self.tree.heading("Name", text="Name")
        self.tree.heading("Barcode", text="Barcode")
        self.tree.heading("Expiry", text="Expiry")
        self.tree.heading("Price", text="Price")
        self.tree.heading("Quantity", text="Quantity")

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scroll_y = ttk.Scrollbar(
            table_panel, orient=tk.VERTICAL, command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scroll_y.set)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        # Database Connection
        self.conn = self.connect_db()
        self.show_list()

    def connect_db(self):
        """Connect to MySQL database."""
        try:
            conn = mysql.connector.connect(
                host="localhost",        # Replace with your MySQL host
                user="root",             # Replace with your MySQL username
                password="",             # Replace with your MySQL password
                database="dbpharma"      # Replace with your database name
            )
            return conn
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Failed to connect to database: {str(e)}")
            self.destroy()

    def show_list(self):
        """Fetch and display drugs close to expiration."""
        try:
            cursor = self.conn.cursor()
            # Adjust the query to match your database schema
            query = """
                SELECT NAME, BARCODE, EXPIRY, SELLING_PRICE, QUANTITY 
                FROM drugs 
                WHERE DATE(EXPIRY) >= CURDATE() 
                  AND DATE(EXPIRY) <= DATE_ADD(CURDATE(), INTERVAL 7 DAY)
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            # Insert rows into the table
            for row in rows:
                self.tree.insert("", tk.END, values=row)

        except mysql.connector.Error as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    app = WarningList()
    app.mainloop()
