import tkinter as tk
from tkinter import ttk, messagebox
from gui.connect import connect_db  # Ensure the database connection is correctly imported

class DrugListApp:
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
        # Header Panel
        self.header_frame = tk.Frame(self.root, bg="#666666")
        self.header_frame.pack(fill=tk.X)

        self.title_label = tk.Label(self.header_frame, text="Drug List", font=("Tahoma", 24, "bold"), bg="#666666", fg="white")
        self.title_label.pack(pady=10)

        # Sorting Panel
        self.sort_frame = tk.Frame(self.root, bg="#333333")
        self.sort_frame.pack(fill=tk.X, padx=10, pady=10)

        self.sort_label = tk.Label(self.sort_frame, text="Sort By: ", font=("Tahoma", 12), bg="#333333", fg="white")
        self.sort_label.pack(side=tk.LEFT, padx=10)

        self.sort_combobox = ttk.Combobox(self.sort_frame, state="readonly", values=["Select", "Name", "Type", "Expiration"])
        self.sort_combobox.current(0)
        self.sort_combobox.pack(side=tk.LEFT, padx=10)

        self.sort_combobox.bind("<<ComboboxSelected>>", self.sort_drugs)

        # Table Panel
        self.table_frame = tk.Frame(self.root, bg="#333333")
        self.table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(
            self.table_frame, 
            columns=("Name", "Type", "Price", "Quantity", "Expiration", "Company"), 
            show="headings"
        )
        self.tree.heading("Name", text="Name")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Price", text="Price")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Expiration", text="Expiration")
        self.tree.heading("Company", text="Company")

        for col in ("Name", "Type", "Price", "Quantity", "Expiration", "Company"):
            self.tree.column(col, anchor=tk.CENTER, width=120)

        self.tree.pack(fill=tk.BOTH, expand=True)

        self.load_drug_list()

    def load_drug_list(self):
        query = "SELECT NAME, TYPE, PRICE, QUANTITY, expiration_date, COMPANY_NAME FROM drugs"
        try:
            cursor = self.con.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()

            # Clear the table
            for row in self.tree.get_children():
                self.tree.delete(row)

            # Insert data into the table
            for row in rows:
                self.tree.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load drugs: {str(e)}")

    def sort_drugs(self, event):
        sort_option = self.sort_combobox.get()
        if sort_option == "Name":
            query = "SELECT NAME, TYPE, PRICE, QUANTITY, EXPIRY, COMPANY_NAME FROM drugs ORDER BY NAME"
        elif sort_option == "Type":
            query = "SELECT NAME, TYPE, PRICE, QUANTITY, EXPIRY, COMPANY_NAME FROM drugs ORDER BY TYPE"
        elif sort_option == "Expiration":
            query = "SELECT NAME, TYPE, PRICE, QUANTITY, EXPIRY, COMPANY_NAME FROM drugs ORDER BY EXPIRY DESC"
        else:
            self.load_drug_list()
            return

        try:
            cursor = self.con.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()

            # Clear the table
            for row in self.tree.get_children():
                self.tree.delete(row)

            # Insert sorted data into the table
            for row in rows:
                self.tree.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to sort drugs: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DrugListApp(root)
    root.mainloop()
