import tkinter as tk
from tkinter import ttk, messagebox
from gui.connect import connect_db  # Ensure the database connection is correctly imported

class AlmostFinishApp:
    def __init__(self, parent, current_user=None):
        self.current_user = current_user
        self.root = parent  # Use the parent frame for embedding

        try:
            self.con = connect_db()  # Establish the database connection
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to connect to the database: {str(e)}")
            self.con = None  # Set to None if connection fails

        self.init_ui()  # Initialize the UI elements

    def init_ui(self):
        """Initialize the UI."""
        # Panel 1: Main container
        self.panel1 = tk.Frame(self.root, bg="#333333")
        self.panel1.pack(fill=tk.BOTH, expand=True)

        # Panel 2: Header
        self.panel2 = tk.Frame(self.panel1, bg="#666666")
        self.panel2.pack(fill=tk.X)

        self.label1 = tk.Label(
            self.panel2,
            text="Almost Finished Drugs",
            font=("Tahoma", 24, "bold"),
            bg="#666666",
            fg="white"
        )
        self.label1.pack(pady=10)

        # Panel 3: Table container
        self.panel3 = tk.Frame(self.panel1, bg="#333333", bd=1, relief=tk.SOLID)
        self.panel3.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)

        self.scrollbar = tk.Scrollbar(self.panel3, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.table = ttk.Treeview(
            self.panel3,
            columns=("Name", "Type", "Company", "Price", "Remaining_Quantity"),
            show='headings',
            yscrollcommand=self.scrollbar.set
        )
        self.scrollbar.config(command=self.table.yview)

        # Define table columns
        self.table.heading("Name", text="Name")
        self.table.heading("Type", text="Type")
        self.table.heading("Company", text="Company")
        self.table.heading("Price", text="Price")
        self.table.heading("Remaining_Quantity", text="Remaining Quantity")

        self.table.column("Name", anchor=tk.CENTER, width=100)
        self.table.column("Type", anchor=tk.CENTER, width=100)
        self.table.column("Company", anchor=tk.CENTER, width=100)
        self.table.column("Price", anchor=tk.CENTER, width=100)
        self.table.column("Remaining_Quantity", anchor=tk.CENTER, width=150)

        self.table.pack(fill=tk.BOTH, expand=True)

        # Load data from the database
        self.show_list()

    def show_list(self):
        """Load drugs with quantity less than 10 from the database."""
        if not self.con:
            return

        try:
            cursor = self.con.cursor()

            # Correct SQL query to match the database schema
            sql = """
            SELECT NAME, TYPE, COMPANY_NAME, PRICE, QUANTITY 
            FROM drugs 
            WHERE QUANTITY < 10
            """
            cursor.execute(sql)
            rows = cursor.fetchall()

            # Clear the table
            for row in self.table.get_children():
                self.table.delete(row)

            # Insert rows into the table
            for row in rows:
                self.table.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = AlmostFinishApp(root)
    root.mainloop()
