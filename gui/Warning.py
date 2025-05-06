import tkinter as tk
from tkinter import messagebox
from gui.connect import connect_db 

class WarningApp:
    def __init__(self, parent, current_user=None):
        self.current_user = current_user
        self.root = parent  # Use the parent frame for embedding

        try:
            self.con = connect_db()  # Establish the database connection
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to connect to the database: {str(e)}")
            self.con = None  # Set to None if connection fails

        self.init_ui()  # Explicitly call the UI initializer

    def init_ui(self):
        """Initialize the Warning UI."""
        # Header Panel
        self.header_frame = tk.Frame(self.root, bg="#666666")
        self.header_frame.pack(fill=tk.X)
        tk.Label(
            self.header_frame,
            text="Warning Form",
            font=("Tahoma", 24, "bold"),
            bg="#666666",
            fg="white",
        ).pack(pady=10)

        # Main Panel
        self.main_frame = tk.Frame(self.root, bg="#333333", bd=2, relief=tk.SOLID)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(
            self.main_frame,
            text="Warning:",
            font=("Tahoma", 36),
            fg="red",
            bg="#333333",
        ).grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)

        tk.Label(
            self.main_frame,
            text="You have some medicines which are",
            font=("Tahoma", 12),
            bg="#333333",
            fg="white",
        ).grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)

        self.warning_label = tk.Label(
            self.main_frame,
            text="Close to Expire",  # Example warning type
            font=("Tahoma", 12),
            bg="#333333",
            fg="yellow",
        )
        self.warning_label.grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)

        # Buttons
        self.button_frame = tk.Frame(self.main_frame, bg="#333333")
        self.button_frame.grid(row=3, column=1, sticky=tk.E, padx=10, pady=5)

        self.show_list_button = tk.Button(
            self.button_frame, text="Show List", command=self.show_warning_list
        )
        self.show_list_button.pack(side=tk.LEFT, padx=5)

        self.cancel_button = tk.Button(
            self.button_frame, text="Cancel", command=self.close_window
        )
        self.cancel_button.pack(side=tk.LEFT, padx=5)

    def show_warning_list(self):
        """Show the warning list (placeholder)."""
        messagebox.showinfo("Warning List", "This functionality will show the list of warnings.")
        # Add additional functionality if needed.

    def close_window(self):
        """Close the warning window."""
        self.root.destroy()

if __name__ == "__main__":
    # Example usage
    root = tk.Tk()
    app = WarningApp(root, current_user="Admin")
    root.mainloop()
