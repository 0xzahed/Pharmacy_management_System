import tkinter as tk
from tkinter import ttk, messagebox
from gui.connect import connect_db

class SalesBillApp:
    def __init__(self, parent, current_user=None):
        self.current_user = current_user
        self.root = parent

        # Database Connection
        try:
            self.con = connect_db()  # Establish the database connection
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to connect to the database: {str(e)}")
            self.con = None

        self.init_ui()  # Initialize the UI elements

    def init_ui(self):
        """Initialize the UI."""
        # Header Panel
        self.header_frame = tk.Frame(self.root, bg="#666666")
        self.header_frame.pack(fill=tk.X)
        tk.Label(self.header_frame, text="Sales Bill Form", font=("Tahoma", 24, "bold"), bg="#666666", fg="white").pack(pady=10)

        # Sale Information
        self.info_frame = tk.Frame(self.root, bg="#333333")
        self.info_frame.pack(fill=tk.X, padx=10, pady=10)

        # Drug Name Selection
        tk.Label(self.info_frame, text="Drug Name:", fg="white", bg="#333333").grid(row=0, column=0, padx=5, pady=5)
        self.drug_name_combo = ttk.Combobox(self.info_frame, state="readonly")
        self.drug_name_combo.grid(row=0, column=1, padx=5, pady=5)
        self.drug_name_combo.bind("<<ComboboxSelected>>", self.on_drug_selected)

        tk.Label(self.info_frame, text="Quantity:", fg="white", bg="#333333").grid(row=0, column=2, padx=5, pady=5)
        self.quantity_combo = ttk.Combobox(self.info_frame, values=[i for i in range(1, 41)], state="readonly")
        self.quantity_combo.grid(row=0, column=3, padx=5, pady=5)

        self.get_bill_button = tk.Button(self.info_frame, text="Get Bill", command=self.get_bill)
        self.get_bill_button.grid(row=0, column=4, padx=10, pady=5)

        # Table
        self.table_frame = tk.Frame(self.root, bg="#333333")
        self.table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(self.table_frame, columns=("Name", "Quantity", "Price", "Amount"), show="headings")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Price", text="Price")
        self.tree.heading("Amount", text="Amount")

        for col in ("Name", "Quantity", "Price", "Amount"):
            self.tree.column(col, anchor=tk.CENTER, width=100)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Total and Buttons
        self.total_frame = tk.Frame(self.root, bg="#333333")
        self.total_frame.pack(fill=tk.X, padx=10, pady=10)

        self.total_label = tk.Label(self.total_frame, text="Total: 00.0$", font=("Tahoma", 24), bg="#333333", fg="white")
        self.total_label.pack(side=tk.LEFT, padx=10)

        self.new_bill_button = tk.Button(self.total_frame, text="New Bill", command=self.new_bill)
        self.new_bill_button.pack(side=tk.RIGHT, padx=10)

        self.cancel_button = tk.Button(self.total_frame, text="Cancel", command=self.cancel_bill)
        self.cancel_button.pack(side=tk.RIGHT, padx=10)

        self.refresh_table()
        self.load_drug_names()

    def refresh_table(self):
        """Refresh the table to show all sales."""
        query = "SELECT * FROM sales"
        try:
            cursor = self.con.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()

            # Clear the table
            for row in self.tree.get_children():
                self.tree.delete(row)

            # Insert rows
            for row in rows:
                self.tree.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh table: {str(e)}")

    def load_drug_names(self):
        """Load drug names into the combo box."""
        query = "SELECT NAME FROM drugs"
        try:
            cursor = self.con.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()

            # Populate the drug name combo box
            drug_names = [row[0] for row in rows]
            self.drug_name_combo['values'] = drug_names
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load drug names: {str(e)}")

    def on_drug_selected(self, event):
        """Handle the event when a drug is selected."""
        drug_name = self.drug_name_combo.get()
        if drug_name:
            query = f"SELECT NAME, PRICE, QUANTITY FROM drugs WHERE NAME = '{drug_name}'"
            try:
                cursor = self.con.cursor()
                cursor.execute(query)
                drug = cursor.fetchone()
                if drug:
                    self.drug_info = drug
                else:
                    messagebox.showinfo("Error", "Drug not found.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to fetch drug info: {str(e)}")

    def get_bill(self):
        """Generate the sales bill."""
        quantity = self.quantity_combo.get()

        if not quantity or int(quantity) <= 0:
            messagebox.showwarning("Missing Information", "Please provide a valid quantity.")
            return

        if not hasattr(self, 'drug_info'):
            messagebox.showwarning("Missing Information", "Please select a drug.")
            return

        name, price, available_quantity = self.drug_info
        quantity = int(quantity)
        amount = float(price) * quantity

        # Check if enough stock is available
        if quantity > available_quantity:
            messagebox.showwarning("Insufficient Stock", "Not enough stock for this drug.")
            return

        # Insert sale into the database
        try:
            query = "INSERT INTO sales (NAME, QUANTITY, PRICE, AMOUNT) VALUES (%s, %s, %s, %s)"
            cursor = self.con.cursor()
            cursor.execute(query, (name, quantity, price, amount))
            self.con.commit()

            # Update the quantity of the drug in the database
            updated_quantity = available_quantity - quantity
            update_query = f"UPDATE drugs SET QUANTITY = {updated_quantity} WHERE NAME = '{name}'"
            cursor.execute(update_query)
            self.con.commit()

            self.refresh_table()
            self.calculate_total()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate bill: {str(e)}")

    def calculate_total(self):
        """Calculate the total amount from the sales table."""
        query = "SELECT SUM(AMOUNT) FROM sales"
        try:
            cursor = self.con.cursor()
            cursor.execute(query)
            total = cursor.fetchone()[0]
            self.total_label.config(text=f"Total: {total:.2f}$" if total else "Total: 00.0$")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to calculate total: {str(e)}")

    def new_bill(self):
        """Reset the sales bill."""
        query = "DELETE FROM sales"
        try:
            cursor = self.con.cursor()
            cursor.execute(query)
            self.con.commit()
            self.refresh_table()
            self.total_label.config(text="Total: 00.0$")
            self.quantity_combo.set("")
            self.drug_name_combo.set("")

            # Reload drug names after clearing the table
            self.load_drug_names()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to create new bill: {str(e)}")

    def cancel_bill(self):
        """Close the application."""
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SalesBillApp(root)
    root.mainloop()
