import tkinter as tk
from tkinter import ttk, messagebox
from gui.connect import connect_db  # Ensure this import works correctly


class BuyDrugApp:
    def __init__(self, parent, current_user=None):
        self.current_user = current_user
        self.root = parent  # Use the parent frame for embedding
        self.frame = tk.Frame(self.root, bg="#444444")  # Create a frame to embed widgets
        self.frame.pack(fill=tk.BOTH, expand=True)  # Ensure it's packed correctly

        try:
            self.con = connect_db()  # Establish the database connection
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to connect to the database: {str(e)}")
            self.con = None  # Set to None if connection fails

        self.init_ui()  # Initialize the UI elements

    def init_ui(self):
        """Initialize the UI."""
        # Header
        self.header_frame = tk.Frame(self.frame, bg="#666666")
        self.header_frame.pack(fill=tk.X)
        self.title_label = tk.Label(self.header_frame, text="Buy Drug Form", font=("Tahoma", 24, "bold"), bg="#666666", fg="white")
        self.title_label.pack(pady=10)

        # Input Fields
        self.panel = tk.Frame(self.frame, bg="#333333")
        self.panel.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Input labels and fields
        self.name_label = tk.Label(self.panel, text="Drug Name:", font=("Tahoma", 12), fg="white", bg="#333333")
        self.name_label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        self.name_entry = tk.Entry(self.panel, font=("Tahoma", 12))
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        # Other fields...
        self.quantity_label = tk.Label(self.panel, text="Quantity:", font=("Tahoma", 12), fg="white", bg="#333333")
        self.quantity_label.grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        self.quantity_entry = ttk.Combobox(self.panel, values=list(range(1, 41)), state="readonly", font=("Tahoma", 12))
        self.quantity_entry.grid(row=1, column=1, padx=10, pady=5)

        self.cost_label = tk.Label(self.panel, text="Cost Price:", font=("Tahoma", 12), fg="white", bg="#333333")
        self.cost_label.grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        self.cost_entry = tk.Entry(self.panel, font=("Tahoma", 12))
        self.cost_entry.grid(row=2, column=1, padx=10, pady=5)

        self.amount_label = tk.Label(self.panel, text="Amount:", font=("Tahoma", 12), fg="white", bg="#333333")
        self.amount_label.grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        self.amount_entry = tk.Entry(self.panel, font=("Tahoma", 12))
        self.amount_entry.grid(row=3, column=1, padx=10, pady=5)

        # Buttons Panel
        self.button_frame = tk.Frame(self.frame, bg="#333333")
        self.button_frame.pack(fill=tk.X, padx=10, pady=10)

        self.make_deal_button = tk.Button(self.button_frame, text="Make a Deal", command=self.make_deal, font=("Tahoma", 12, "bold"))
        self.make_deal_button.pack(side=tk.LEFT, padx=10)
        self.update_button = tk.Button(self.button_frame, text="Update", command=self.update_deal, font=("Tahoma", 12, "bold"))
        self.update_button.pack(side=tk.LEFT, padx=10)
        self.delete_button = tk.Button(self.button_frame, text="Delete", command=self.delete_deal, font=("Tahoma", 12, "bold"))
        self.delete_button.pack(side=tk.LEFT, padx=10)
        self.clear_button = tk.Button(self.button_frame, text="Clear", command=self.clear_fields, font=("Tahoma", 12, "bold"))
        self.clear_button.pack(side=tk.LEFT, padx=10)

        self.cancel_button = tk.Button(self.button_frame, text="Cancel", command=self.cancel_deal, font=("Tahoma", 12, "bold"))
        self.cancel_button.pack(side=tk.LEFT, padx=10)

    def make_deal(self):
        name = self.name_entry.get()
        quantity = self.quantity_entry.get()
        cost = self.cost_entry.get()
        amount = self.amount_entry.get()

        if not name or not quantity or not cost or not amount:
            messagebox.showerror("Error", "Please complete all fields.")
            return

        try:
            connection = connect_db()
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO purchases (NAME, QUANTITY, COST, AMOUNT) VALUES (%s, %s, %s, %s)",
                (name, quantity, cost, amount)
            )
            connection.commit()
            connection.close()
            messagebox.showinfo("Success", "Deal made successfully.")
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def update_deal(self):
        name = self.name_entry.get()
        if not name:
            messagebox.showerror("Error", "Please enter a drug name to update.")
            return
        # Add logic for updating the deal in the database

    def delete_deal(self):
        name = self.name_entry.get()
        if not name:
            messagebox.showerror("Error", "Please enter a drug name to delete.")
            return
        # Add logic for deleting the deal in the database

    def clear_fields(self):
        self.name_entry.delete(0, tk.END)
        self.quantity_entry.set("")
        self.cost_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)

    def cancel_deal(self):
        self.root.destroy()


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

        self.buy_drug_button = tk.Button(self.button_frame, text="Buy Drug", command=self.open_buy_drug, width=20, height=2, bg="lightblue", fg="black")
        self.buy_drug_button.pack(pady=5)

    def open_buy_drug(self):
        """Load the BuyDrugApp into the display frame."""
        self.clear_display()
        BuyDrugApp(self.body_frame)

    def clear_display(self):
        for widget in self.body_frame.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = PharmacyApp(root)
    root.mainloop()
