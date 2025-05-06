import sys
import os

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui.login import LoginForm

def main():
    """Entry point for the application."""
    try:
        print("Starting the application...")  # Debugging information
        app = LoginForm()  # Initialize the LoginForm
        app.mainloop()  # Start the Tkinter main event loop
    except Exception as e:
        print(f"An error occurred: {e}")  # Log errors
        import tkinter as tk
        tk.messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    main()
