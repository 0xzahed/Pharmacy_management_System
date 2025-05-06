import tkinter as tk
from tkinter import messagebox
from gui.connect import connect_db  # Import the database connection
from gui.Pharmacy import PharmacyApp  # Import the UserApp class

class LoginForm(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login Form")
        self.geometry("700x600")
        self.resizable(False, False)

        # Attempt to connect to the database
        try:
            self.conn = connect_db()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to connect to the database: {str(e)}")
            self.destroy()
            return

        # UI Elements for the Login Form
        tk.Label(self, text="Login Form", font=("Tahoma", 24, "bold")).pack(pady=10)
        tk.Label(self, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=5)

        tk.Label(self, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self, text="Login", command=self.validate_login).pack(pady=10)

    def validate_login(self):
        """
        Validate login credentials and open UserApp on success.
        """
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Validation Error", "Both fields are required!")
            return

        try:
            cursor = self.conn.cursor()
            query = "SELECT * FROM users WHERE NAME=%s AND PASSWORD=%s"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()

            if user:
                # Construct the current user dictionary
                current_user = {"id": user[0], "name": user[1]}  # Adjust based on your database schema
                messagebox.showinfo("Login Successful", f"Welcome {current_user['name']}!")
                self.open_user_app(current_user)
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def open_user_app(self, current_user):
        """
        Open the UserApp after successful login.
        """
        self.destroy()  
        root = tk.Tk()  
        app = PharmacyApp(root, )  
        root.mainloop()

if __name__ == "__main__":
    app = LoginForm()
    app.mainloop()
