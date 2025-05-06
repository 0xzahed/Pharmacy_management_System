import tkinter as tk
from tkinter import messagebox
from gui.User import UserApp
from gui.Drug import DrugApp
from gui.Sales_Bill import SalesBillApp
from gui.connect import connect_db
from gui.company import CompanyApp
from gui.all_deals import AllDealApp
from gui.Almost_Finish import AlmostFinishApp
from gui.Drug_List import DrugListApp
from gui.Buy_Drug import BuyDrugApp

class PharmacyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pharmacy Management System (Administration)")
        self.root.geometry("1700x750")
        self.root.resizable(False, False)

        self.current_user = {"name": "Admin"}  # Placeholder for logged-in user

        # Initialize Header, Body, and Footer
        self.init_header()
        self.init_body()
        self.init_footer()

    def init_header(self):
        self.header_frame = tk.Frame(self.root, bg="#666666")
        self.header_frame.pack(fill=tk.X)

        tk.Label(
            self.header_frame,
            text="Pharmacy Management System",
            font=("Tahoma", 24, "bold"),
            bg="#666666",
            fg="white",
        ).pack(side=tk.LEFT, padx=20)

        tk.Label(
            self.header_frame,
            text=f"Logged in as: {self.current_user['name']}",
            font=("Tahoma", 12),
            bg="#666666",
            fg="white",
        ).pack(side=tk.RIGHT, padx=20)

    def init_body(self):
        self.body_frame = tk.Frame(self.root, bg="#333333")
        self.body_frame.pack(fill=tk.BOTH, expand=True)

        self.button_frame = tk.Frame(self.body_frame, bg="#444444")
        self.button_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # Define buttons for each module
        button_texts = [
            ("Manage Users", self.manage_users),
            ("Manage Drugs", self.manage_drugs),
            ("Drug List", self.show_drug_list), 
            ("Company Information", self.manage_companies),
            ("Buy Drug", self.open_buy_drug_app),
            ("All Deals", self.show_all_deals),
            ("Almost Finished Drugs", self.almost_finish),
            ("Sales Bill", self.open_sales_bill_form),
            ("Logout", self.logout),
        ]

        for text, command in button_texts:
            tk.Button(
                self.button_frame,
                text=text,
                command=command,
                width=20,
                height=2,
                bg="lightblue",
                fg="black",
            ).pack(pady=5)

        self.display_frame = tk.Frame(self.body_frame, bg="#444444")
        self.display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    def init_footer(self):
        self.footer_frame = tk.Frame(self.root, bg="#666666")
        self.footer_frame.pack(side=tk.BOTTOM, fill=tk.X)

    def clear_display(self):
        """Clear all widgets in the display frame."""
        for widget in self.display_frame.winfo_children():
            widget.destroy()

    # Button Handlers
    def manage_users(self):
        """Load UserApp into display_frame."""
        self.clear_display()
        try:
            UserApp(self.display_frame, current_user=self.current_user)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load User Management: {str(e)}")

    def manage_drugs(self):
        """Load DrugApp into display_frame."""
        self.clear_display()
        try:
            DrugApp(self.display_frame,current_user=self.current_user)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load Drug Management: {str(e)}")

    def open_sales_bill_form(self):
        """Load the SalesBillApp into display_frame."""
        self.clear_display()
        try:
            SalesBillApp(self.display_frame)  # Embedding SalesBillApp inside the display frame
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load Sales Bill form: {str(e)}")
    def manage_companies(self):
            """Load CompanyApp into display_frame."""
            self.clear_display()
            try:
                CompanyApp(self.display_frame)  # Initialize CompanyApp in display_frame
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load Company Management: {str(e)}")
    def show_all_deals(self):
        """Clear the display frame and load All Deals."""
        self.clear_display()
        try:
            AllDealApp(self.display_frame)  # Pass the display frame as the parent
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load All Deals: {str(e)}")
    def open_buy_drug_app(self):
        """Load the BuyDrugApp into display_frame."""
        self.clear_display()
        try:
            BuyDrugApp(self.display_frame)  # Pass display_frame for embedding the app
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load Buy Drug App: {str(e)}")

    def almost_finish(self):
        """Load AlmostFinishApp into display_frame."""
        self.clear_display()
        try:
            AlmostFinishApp(self.display_frame)  # Pass display_frame as the parent
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load Almost Finished Drugs: {str(e)}")

    def show_drug_list(self):
        """Load the Drug List App."""
        self.clear_display()
        try:
            DrugListApp(self.display_frame)  # Correctly instantiate DrugListApp with the display frame
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load Drug List: {str(e)}")

    def logout(self):
        """Logout the user and return to login screen."""
        result = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if result:
            self.root.destroy()
            # Restart Login Form
            login_root = tk.Tk()
            login_root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = PharmacyApp(root)
    root.mainloop()
