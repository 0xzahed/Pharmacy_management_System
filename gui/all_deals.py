import tkinter as tk
from tkinter import ttk, messagebox
from gui.connect import connect_db  # Ensure the database connection is correctly imported


class AllDealApp:
    def __init__(self, parent):
        # Create a frame within the provided parent (display_frame in PharmacyApp)
        self.parent = parent
        self.frame = tk.Frame(self.parent, bg="#444444")
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Title
        tk.Label(
            self.frame,
            text="All Deals",
            font=("Tahoma", 18, "bold"),
            bg="#444444",
            fg="white",
        ).pack(pady=10)

        # Table for displaying deals
        self.table_frame = tk.Frame(self.frame, bg="#333333")
        self.table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Define the treeview to display data
        self.tree = ttk.Treeview(
            self.table_frame,
            columns=("ID", "Name", "Quantity", "Cost", "Amount", "Purchase Date"),
            show="headings",
        )
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Cost", text="Cost Price")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Purchase Date", text="Purchase Date")

        # Set column widths and alignment
        for col in ("ID", "Name", "Quantity", "Cost", "Amount", "Purchase Date"):
            self.tree.column(col, anchor=tk.CENTER, width=120)

        self.tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Load data from the database
        self.load_all_deals()

    def load_all_deals(self):
        """Fetch and display all deal data from the database."""
        try:
            conn = connect_db()  # Connect to the database
            cursor = conn.cursor()

            # Query to fetch data from the 'purchases' table
            query = "SELECT id, name, quantity, cost, amount, purchase_date FROM purchases"
            cursor.execute(query)
            rows = cursor.fetchall()

            # Clear existing data in the table
            for row in self.tree.get_children():
                self.tree.delete(row)

            # Insert new data into the table
            for row in rows:
                self.tree.insert("", tk.END, values=row)

            conn.close()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load data: {str(e)}")


# Example of how the AllDealApp is used in your PharmacyApp
class PharmacyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pharmacy Management System")
        self.root.geometry("1220x607")
        self.root.resizable(False, False)

        self.current_user = {"name": "Admin"}

        self.init_header()
        self.init_body()

    def init_header(self):
        self.header_frame = tk.Frame(self.root, bg="#666666")
        self.header_frame.pack(fill=tk.X)
        tk.Label(self.header_frame, text="Pharmacy Management System", font=("Tahoma", 24, "bold"), bg="#666666", fg="white").pack(side=tk.LEFT, padx=20)
        tk.Label(self.header_frame, text=f"Logged in as: {self.current_user['name']}", font=("Tahoma", 12), bg="#666666", fg="white").pack(side=tk.RIGHT, padx=20)

    def init_body(self):
        self.body_frame = tk.Frame(self.root, bg="#333333")
        self.body_frame.pack(fill=tk.BOTH, expand=True)

        self.button_frame = tk.Frame(self.body_frame, bg="#444444")
        self.button_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.all_deals_button = tk.Button(self.button_frame, text="All Deals", command=self.open_all_deals, width=20, height=2, bg="lightblue", fg="black")
        self.all_deals_button.pack(pady=5)

        # Add other buttons as needed

    def open_all_deals(self):
        """Load the AllDealApp into the display frame."""
        self.clear_display()
        AllDealApp(self.body_frame)

    def clear_display(self):
        for widget in self.body_frame.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = PharmacyApp(root)
    root.mainloop()
