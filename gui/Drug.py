import tkinter as tk
from tkinter import ttk, messagebox
from gui.connect import connect_db
from datetime import datetime

class DrugApp:
    def __init__(self, parent, current_user=None):
        self.root = parent  # Use the parent frame for embedding
        self.current_user = current_user

        # Initialize database connection
        try:
            self.con = connect_db()
            self.cursor = self.con.cursor() 
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to connect to the database: {str(e)}")
            self.con = None
            self.cursor=None  # Handle missing connection gracefully

        self.init_ui()

    def init_ui(self):
        """Initialize the Drug Management UI."""
        # Header
        self.header_frame = tk.Frame(self.root, bg="#666666")
        self.header_frame.pack(fill=tk.X)
        tk.Label(
            self.header_frame,
            text="Drug Management Form",
            font=("Tahoma", 24, "bold"),
            bg="#666666",
            fg="white",
        ).pack(pady=10)

        # Main content for Drug Management
        self.details_frame = tk.Frame(self.root, bg="#333333")
        self.details_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(self.details_frame, text="Drug Name:", fg="white", bg="#333333").grid(row=0, column=0, padx=10, pady=5)
        self.name_entry = tk.Entry(self.details_frame)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.details_frame, text="Type:", fg="white", bg="#333333").grid(row=1, column=0, padx=10, pady=5)
        self.type_entry = tk.Entry(self.details_frame)
        self.type_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.details_frame, text="Dose:", fg="white", bg="#333333").grid(row=2, column=0, padx=10, pady=5)
        self.dose_entry = tk.Entry(self.details_frame)
        self.dose_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self.details_frame, text="Price:", fg="white", bg="#333333").grid(row=3, column=0, padx=10, pady=5)
        self.price_entry = tk.Entry(self.details_frame)
        self.price_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(self.details_frame, text="Quantity:", fg="white", bg="#333333").grid(row=4, column=0, padx=10, pady=5)
        self.quantity_entry = tk.Entry(self.details_frame)
        self.quantity_entry.grid(row=4, column=1, padx=10, pady=5)

        tk.Label(self.details_frame, text="Expiration Date (YYYY-MM-DD):", fg="white", bg="#333333").grid(row=5, column=0, padx=10, pady=5)
        self.expiration_entry = tk.Entry(self.details_frame)
        self.expiration_entry.grid(row=5, column=1, padx=10, pady=5)

        tk.Label(self.details_frame, text="Company Name:", fg="white", bg="#333333").grid(row=6, column=0, padx=10, pady=5)
        self.company_entry = tk.Entry(self.details_frame)
        self.company_entry.grid(row=6, column=1, padx=10, pady=5)

        # Buttons
        self.button_frame = tk.Frame(self.details_frame, bg="#333333")
        self.button_frame.grid(row=7, columnspan=2, pady=10)

        tk.Button(
            self.button_frame, text="Add Drug", command=self.add_drug, bg="lightgreen", width=15
        ).grid(row=0, column=0, padx=5)
        tk.Button(
            self.button_frame, text="Update Drug", command=self.update_drug, bg="lightblue", width=15
        ).grid(row=0, column=1, padx=5)
        tk.Button(
            self.button_frame, text="Delete Drug", command=self.delete_drug, bg="tomato", width=15
        ).grid(row=0, column=2, padx=5)
        tk.Button(
            self.button_frame, text="Clear Fields", command=self.clear_fields, bg="gray", width=15
        ).grid(row=0, column=3, padx=5)

        # Drug Table
        self.table_frame = tk.Frame(self.details_frame, bg="#444444")
        self.table_frame.grid(row=8, columnspan=2, pady=10)

        self.drug_table = ttk.Treeview(
            self.table_frame,
            columns=("Name", "Type", "Dose", "Price", "Quantity", "Expiration Date", "Company"),
            show="headings",
        )
        self.drug_table.heading("Name", text="Drug Name")
        self.drug_table.heading("Type", text="Type")
        self.drug_table.heading("Dose", text="Dose")
        self.drug_table.heading("Price", text="Price")
        self.drug_table.heading("Quantity", text="Quantity")
        self.drug_table.heading("Expiration Date", text="Expiration Date")
        self.drug_table.heading("Company", text="Company Name")

        for col in ("Name", "Type", "Dose", "Price", "Quantity", "Expiration Date", "Company"):
            self.drug_table.column(col, anchor=tk.CENTER, width=120)

        self.drug_table.pack(fill=tk.BOTH, expand=True)
        self.drug_table.bind("<ButtonRelease-1>", self.fill_form_from_table)

        self.load_drugs()

    def load_drugs(self):
        if not self.con:
            return
        query = "SELECT name, type, dose, price, quantity, expiration_date, company_name FROM drugs"
        try:
            
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            for row in self.drug_table.get_children():
                self.drug_table.delete(row)

            for row in rows:
                self.drug_table.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load drugs: {str(e)}")

    # Existing methods: add_drug, update_drug, delete_drug, clear_fields, fill_form_from_table
    def add_drug(self):
        """Add a new drug."""
        if not self.con:
            messagebox.showerror("Error", "Database connection is not established.")
            return

        name = self.name_entry.get()
        type_ = self.type_entry.get()
        dose = self.dose_entry.get()
        price = self.price_entry.get()
        quantity = self.quantity_entry.get()
        expiration_date = self.expiration_entry.get()
        company_name = self.company_entry.get()

        if not all([name, type_, dose, price, quantity, expiration_date, company_name]):
            messagebox.showwarning("Missing Information", "Please fill out all fields.")
            return
        query = "INSERT INTO drugs (name, type, dose, price, quantity, expiration_date, company_name)VALUES (%s, %s, %s, %s, %s, %s, %s)"
        
        try:
            
            cursor = self.con.cursor()
            cursor.execute(query, (name, type_, dose, price, quantity, expiration_date, company_name))
            self.con.commit()
            messagebox.showinfo("Success", "Drug added successfully!")
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add drug: {str(e)}")

    def update_drug(self):
        """Update an existing drug."""
        if not self.con:
            messagebox.showerror("Error", "Database connection is not established.")
            return

        # Fetch the data from the form
        name = self.name_entry.get().strip()
        type_ = self.type_entry.get().strip()
        dose = self.dose_entry.get().strip()
        price = self.price_entry.get().strip()
        quantity = self.quantity_entry.get().strip()
        expiration_date = self.expiration_entry.get().strip()
        company_name = self.company_entry.get().strip()

        # Validate all fields are filled
        if not all([name, type_, dose, price, quantity, expiration_date, company_name]):
            messagebox.showwarning("Missing Information", "Please fill out all fields.")
            return

        try:
            # Execute the update query
            query = """
            UPDATE drugs 
            SET type = %s, dose = %s, price = %s, quantity = %s, expiration_date = %s, company_name = %s 
            WHERE name = %s
            """
            self.cursor.execute(
                query, (type_, dose, price, quantity, expiration_date, company_name, name)
            )
            self.con.commit()

            # Check if any rows were updated
            if self.cursor.rowcount == 0:
                messagebox.showerror("Error", f"No drug found with the name '{name}'")
            else:
                messagebox.showinfo("Success", f"Drug '{name}' updated successfully!")
                self.clear_fields()
                self.load_drugs()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update drug: {str(e)}")

    def delete_drug(self):
        """Delete a drug."""
        if not self.con:
            messagebox.showerror("Error", "Database connection is not established.")
            return

        name = self.name_entry.get().strip()

        # Validate that the drug name is provided
        if not name:
            messagebox.showwarning("Missing Information", "Please enter the drug name to delete.")
            return

        try:
            # Execute the delete query
            query = "DELETE FROM drugs WHERE name = %s"
            self.cursor.execute(query, (name,))
            self.con.commit()

            # Check if any rows were deleted
            if self.cursor.rowcount == 0:
                messagebox.showerror("Error", f"No drug found with the name '{name}'")
            else:
                messagebox.showinfo("Success", f"Drug '{name}' deleted successfully!")
                self.clear_fields()
                self.load_drugs()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete drug: {str(e)}")

    def clear_fields(self):
        """Clear input fields."""
        self.name_entry.delete(0, tk.END)
        self.type_entry.delete(0, tk.END)
        self.dose_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.expiration_entry.delete(0, tk.END)
        self.company_entry.delete(0, tk.END)

    def fill_form_from_table(self, event):
        """Fill the form fields from the selected table row."""
        selected_row = self.drug_table.focus()
        row_data = self.drug_table.item(selected_row, "values")
        if row_data:
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, row_data[0])
            self.type_entry.delete(0, tk.END)
            self.type_entry.insert(0, row_data[1])
            self.dose_entry.delete(0, tk.END)
            self.dose_entry.insert(0, row_data[2])
            self.price_entry.delete(0, tk.END)
            self.price_entry.insert(0, row_data[3])
            self.quantity_entry.delete(0, tk.END)
            self.quantity_entry.insert(0, row_data[4])
            self.expiration_entry.delete(0, tk.END)
            self.expiration_entry.insert(0, row_data[5])
            self.company_entry.delete(0, tk.END)
            self.company_entry.insert(0, row_data[6])


if __name__ == "__main__":
    root = tk.Tk()
    app = DrugApp(root)
    root.mainloop()
