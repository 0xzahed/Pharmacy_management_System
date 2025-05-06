import tkinter as tk
from tkinter import ttk, messagebox
from gui.connect import connect_db  # Ensure this is correctly imported

class UserApp:
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
        """Initialize the user management UI."""
        # Header
        self.header_frame = tk.Frame(self.root, bg="#666666")
        self.header_frame.pack(fill=tk.X)
        tk.Label(
            self.header_frame,
            text="User Management Form",
            font=("Tahoma", 24, "bold"),
            bg="#666666",
            fg="white",
        ).pack(pady=10)

        # User Details
        self.details_frame = tk.Frame(self.root, bg="#333333")
        self.details_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(self.details_frame, text="User ID:", fg="white", bg="#333333").grid(row=0, column=0, padx=5, pady=5)
        self.id_entry = tk.Entry(self.details_frame)
        self.id_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.details_frame, text="User Name:", fg="white", bg="#333333").grid(row=1, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(self.details_frame)
        self.name_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.details_frame, text="DOB (YYYY-MM-DD):", fg="white", bg="#333333").grid(row=2, column=0, padx=5, pady=5)
        self.dob_entry = tk.Entry(self.details_frame)
        self.dob_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.details_frame, text="Address:", fg="white", bg="#333333").grid(row=3, column=0, padx=5, pady=5)
        self.address_text = tk.Text(self.details_frame, height=3, width=30)
        self.address_text.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(self.details_frame, text="Phone:", fg="white", bg="#333333").grid(row=4, column=0, padx=5, pady=5)
        self.phone_entry = tk.Entry(self.details_frame)
        self.phone_entry.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(self.details_frame, text="Salary:", fg="white", bg="#333333").grid(row=5, column=0, padx=5, pady=5)
        self.salary_entry = tk.Entry(self.details_frame)
        self.salary_entry.grid(row=5, column=1, padx=5, pady=5)

        tk.Label(self.details_frame, text="Password:", fg="white", bg="#333333").grid(row=6, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(self.details_frame, show="*")
        self.password_entry.grid(row=6, column=1, padx=5, pady=5)

        # Buttons
        self.button_frame = tk.Frame(self.root, bg="#333333")
        self.button_frame.pack(fill=tk.X, padx=10, pady=10)

        self.add_button = tk.Button(self.button_frame, text="Add User", command=self.add_user)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.update_button = tk.Button(self.button_frame, text="Update User", command=self.update_user)
        self.update_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = tk.Button(self.button_frame, text="Delete User", command=self.delete_user)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = tk.Button(self.button_frame, text="Clear", command=self.clear_fields)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        # User Table
        self.table_frame = tk.Frame(self.root, bg="#333333")
        self.table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.user_table = ttk.Treeview(
            self.table_frame,
            columns=("ID", "Name", "DOB", "Address", "Phone", "Salary"),
            show="headings",
        )
        self.user_table.heading("ID", text="ID")
        self.user_table.heading("Name", text="Name")
        self.user_table.heading("DOB", text="DOB")
        self.user_table.heading("Address", text="Address")
        self.user_table.heading("Phone", text="Phone")
        self.user_table.heading("Salary", text="Salary")

        for col in ("ID", "Name", "DOB", "Address", "Phone", "Salary"):
            self.user_table.column(col, anchor=tk.CENTER, width=100)

        self.user_table.pack(fill=tk.BOTH, expand=True)
        self.user_table.bind("<ButtonRelease-1>", self.fill_form_from_table)

        self.load_users()

    def load_users(self):
        """Load users into the table."""
        if not self.con:
            return  # Skip loading if the connection is not established

        query = "SELECT ID, NAME, DOB, ADDRESS, PHONE, SALARY FROM users"
        try:
            cursor = self.con.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in self.user_table.get_children():
                self.user_table.delete(row)
            for row in rows:
                self.user_table.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load users: {str(e)}")

    def add_user(self):
        """Add a new user."""
        user_id = self.id_entry.get()
        name = self.name_entry.get()
        dob = self.dob_entry.get()
        address = self.address_text.get("1.0", tk.END).strip()
        phone = self.phone_entry.get()
        salary = self.salary_entry.get()
        password = self.password_entry.get()

        if not user_id or not name or not dob or not address or not phone or not salary or not password:
            messagebox.showwarning("Missing Information", "Please complete all fields!")
            return

        query = "INSERT INTO users (ID, NAME, DOB, ADDRESS, PHONE, SALARY, PASSWORD) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        try:
            cursor = self.con.cursor()
            cursor.execute(query, (user_id, name, dob, address, phone, salary, password))
            self.con.commit()
            messagebox.showinfo("Success", "User added successfully!")
            self.load_users()
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add user: {str(e)}")

    def update_user(self):
        """Update user details."""
        user_id = self.id_entry.get()
        name = self.name_entry.get()
        dob = self.dob_entry.get()
        address = self.address_text.get("1.0", tk.END).strip()
        phone = self.phone_entry.get()
        salary = self.salary_entry.get()

    # Validate input fields
        if not user_id or not name or not dob or not address or not phone or not salary:
            messagebox.showwarning("Missing Information", "Please complete all fields!")
            return

    # Debug: Print values to check if they're correct
        print(f"Updating User - ID: {user_id}, Name: {name}, DOB: {dob}, Address: {address}, Phone: {phone}, Salary: {salary}")

        query = "UPDATE users SET NAME=%s, DOB=%s, ADDRESS=%s, PHONE=%s, SALARY=%s WHERE ID=%s"
        try:
            cursor = self.con.cursor()
            rows_affected = cursor.execute(query, (name, dob, address, phone, salary, user_id))
            self.con.commit()

            # Check if the update was successful
            if cursor.rowcount == 0:
                messagebox.showwarning("Update Failed", f"No user found with ID: {user_id}")
            else:
                messagebox.showinfo("Success", "User updated successfully!")
                self.load_users()  # Refresh the table
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update user: {str(e)}")



    def delete_user(self):
        """Delete a user."""
        user_id = self.id_entry.get()
        if not user_id:
            messagebox.showwarning("Missing Information", "Please enter the User ID to delete!")
            return

        query = "DELETE FROM users WHERE ID=%s"
        try:
            cursor = self.con.cursor()
            cursor.execute(query, (user_id,))
            self.con.commit()
            messagebox.showinfo("Success", "User deleted successfully!")
            self.load_users()
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete user: {str(e)}")

    def clear_fields(self):
        """Clear all input fields."""
        self.id_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.dob_entry.delete(0, tk.END)
        self.address_text.delete("1.0", tk.END)
        self.phone_entry.delete(0, tk.END)
        self.salary_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

    def fill_form_from_table(self, event):
        """Fill form fields from the selected table row."""
        selected_row = self.user_table.focus()
        row_data = self.user_table.item(selected_row, "values")
        if row_data:
            self.id_entry.delete(0, tk.END)
            self.id_entry.insert(0, row_data[0])
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, row_data[1])
            self.dob_entry.delete(0, tk.END)
            self.dob_entry.insert(0, row_data[2])
            self.address_text.delete("1.0", tk.END)
            self.address_text.insert("1.0", row_data[3])
            self.phone_entry.delete(0, tk.END)
            self.phone_entry.insert(0, row_data[4])
            self.salary_entry.delete(0, tk.END)
            self.salary_entry.insert(0, row_data[5])

if __name__ == "__main__":
    root = tk.Tk()
    app = UserApp(root)
    root.mainloop()
