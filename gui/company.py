import tkinter as tk
from tkinter import messagebox, ttk
from gui.connect import connect_db  # Import the database connection

class CompanyApp:
    def __init__(self, parent, current_user=None):
        self.current_user = current_user
        self.root = parent

        try:
            self.con = connect_db()  # Establish the database connection
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to connect to the database: {str(e)}")
            self.con = None  # Set to None if connection fails

        self.init_ui()

    def init_ui(self):
        """Initialize the UI."""
        # Header
        self.header_frame = tk.Frame(self.root, bg="#333333")
        self.header_frame.pack(fill=tk.X)

        tk.Label(
            self.header_frame,
            text="Company Management Form",
            font=("Tahoma", 24, "bold"),
            bg="#333333",
            fg="white",
        ).pack(pady=10)

        # Input Panel
        self.panel2 = tk.Frame(self.root, bg="#666666")
        self.panel2.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # Add Column Names for Labels
        column_names = ["Company Name", "Company Address", "Company Phone"]
        for i, column_name in enumerate(column_names):
            label = tk.Label(self.panel2, text=column_name + ":", fg="white", bg="#666666", font=("Tahoma", 12, "bold"))
            label.grid(row=i, column=0, sticky=tk.W, pady=5)

        # Input Fields
        self.name = tk.Entry(self.panel2, font=("Tahoma", 12))
        self.name.grid(row=0, column=1, padx=10, pady=5)

        self.address = tk.Text(self.panel2, height=4, width=30, font=("Tahoma", 12))
        self.address.grid(row=1, column=1, padx=10, pady=5)

        self.phone = tk.Entry(self.panel2, font=("Tahoma", 12))
        self.phone.grid(row=2, column=1, padx=10, pady=5)

        # Buttons Panel
        self.panel3 = tk.Frame(self.panel2, bg="#666666")
        self.panel3.grid(row=3, column=1, pady=10)

        self.btn_save = tk.Button(self.panel3, text="Save Info", command=self.save_info, font=("Tahoma", 12, "bold"))
        self.btn_save.pack(side=tk.LEFT, padx=5)

        self.btn_update = tk.Button(self.panel3, text="Update Info", command=self.update_info, font=("Tahoma", 12, "bold"))
        self.btn_update.pack(side=tk.LEFT, padx=5)

        self.btn_delete = tk.Button(self.panel3, text="Delete Info", command=self.delete_info, font=("Tahoma", 12, "bold"))
        self.btn_delete.pack(side=tk.LEFT, padx=5)

        self.btn_clear = tk.Button(self.panel3, text="Clear", command=self.clear, font=("Tahoma", 12, "bold"))
        self.btn_clear.pack(side=tk.LEFT, padx=5)

        # Table Panel with Scrollable List of Companies
        self.panel4 = tk.Frame(self.root, bg="#333333")
        self.panel4.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)

        self.canvas = tk.Canvas(self.panel4, bg="#333333")
        self.scrollbar = ttk.Scrollbar(self.panel4, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill="y")

        self.scrollable_frame = tk.Frame(self.canvas, bg="#333333")
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Create Table with Column Names
        self.create_table()

        self.load_companies()

    def create_table(self):
        """Create column headers for the company list table."""
        columns = ["Company Name", "Company Address", "Company Phone"]
        
        # Column headers (with labels at the top)
        for col, column_name in enumerate(columns):
            label = tk.Label(self.scrollable_frame, text=column_name, fg="white", bg="#333333", font=("Tahoma", 12, "bold"))
            label.grid(row=0, column=col, padx=10, pady=5, sticky=tk.W)

    def load_companies(self):
        """Load companies from the database."""
        try:
            cursor = self.con.cursor()
            cursor.execute("SELECT NAME, ADDRESS, PHONE FROM company")
            rows = cursor.fetchall()

            # Clear table before loading
            for widget in self.scrollable_frame.winfo_children():
                widget.grid_forget()

            # Reload headers
            self.create_table()

            # Insert new data into the table
            for row_idx, row in enumerate(rows, 1):
                self.add_company_to_table(row, row_idx)

            # Update scrollable region
            self.scrollable_frame.update_idletasks()
            self.canvas.config(scrollregion=self.canvas.bbox("all"))

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load companies: {str(e)}")

    def add_company_to_table(self, row, row_idx):
        """Helper function to add a company row to the table."""
        name_label = tk.Label(self.scrollable_frame, text=row[0], fg="white", bg="#333333", font=("Tahoma", 12))
        name_label.grid(row=row_idx, column=0, padx=10, pady=5)

        address_label = tk.Label(self.scrollable_frame, text=row[1], fg="white", bg="#333333", font=("Tahoma", 12))
        address_label.grid(row=row_idx, column=1, padx=10, pady=5)

        phone_label = tk.Label(self.scrollable_frame, text=row[2], fg="white", bg="#333333", font=("Tahoma", 12))
        phone_label.grid(row=row_idx, column=2, padx=10, pady=5)

    def save_info(self):
        """Save company information."""
        name = self.name.get()
        address = self.address.get("1.0", tk.END).strip()
        phone = self.phone.get()

        if not name or not address or not phone:
            messagebox.showwarning("Validation Error", "Please complete all fields!")
            return

        try:
            cursor = self.con.cursor()
            query = "INSERT INTO company (NAME, ADDRESS, PHONE) VALUES (%s, %s, %s)"
            cursor.execute(query, (name, address, phone))
            self.con.commit()
            messagebox.showinfo("Success", "Company information saved successfully!")
            self.load_companies()
            self.clear()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save company: {str(e)}")

    def update_info(self):
        """Update company information."""
        name = self.name.get()
        address = self.address.get("1.0", tk.END).strip()
        phone = self.phone.get()

        if not name:
            messagebox.showwarning("Validation Error", "Please enter the company name to update!")
            return

        if not address or not phone:
            messagebox.showwarning("Validation Error", "Please complete all fields!")
            return

        try:
            cursor = self.con.cursor()
            query = "UPDATE company SET ADDRESS = %s, PHONE = %s WHERE NAME = %s"
            cursor.execute(query, (address, phone, name))
            if cursor.rowcount == 0:
                messagebox.showwarning("Update Error", f"No company found with name '{name}'.")
            else:
                self.con.commit()
                messagebox.showinfo("Success", "Company information updated successfully!")
                self.load_companies()
            self.clear()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update company: {str(e)}")

    def delete_info(self):
        """Delete company information."""
        name = self.name.get()

        if not name:
            messagebox.showwarning("Validation Error", "Please enter the company name to delete!")
            return

        try:
            cursor = self.con.cursor()
            query = "DELETE FROM company WHERE NAME = %s"
            cursor.execute(query, (name,))
            self.con.commit()
            messagebox.showinfo("Success", "Company information deleted successfully!")
            self.load_companies()
            self.clear()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete company: {str(e)}")

    def clear(self):
        """Clear input fields."""
        self.name.delete(0, tk.END)
        self.address.delete("1.0", tk.END)
        self.phone.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = CompanyApp(root)
    root.mainloop()
