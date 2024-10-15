import tkinter as tk
from tkinter import messagebox
import random

# Sample user profiles with their secret codes
user_profiles = {}
secret_colors = ['red', 'green', 'blue', 'yellow', 'orange']

class RegistrationApp:
    def __init__(self, master):
        self.master = master
        master.title("Registration")

        self.label = tk.Label(master, text="Register")
        self.label.pack()

        self.username_label = tk.Label(master, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(master)
        self.username_entry.pack()

        self.password_label = tk.Label(master, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(master, show='*')
        self.password_entry.pack()

        self.register_button = tk.Button(master, text="Register", command=self.register_user)
        self.register_button.pack()

    def register_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        secret_color = random.choice(secret_colors)

        if username in user_profiles:
            messagebox.showerror("Error", "Username already exists.")
            return

        user_profiles[username] = {'password': password, 'secret_color': secret_color}
        messagebox.showinfo("Success", "Registered successfully!")

        # Display the secret color button
        self.secret_color_button = tk.Button(self.master, text="Secret Color", bg=secret_color)
        self.secret_color_button.pack(pady=10)

        # Message instructing to click to go to the login window
        self.instruction_label = tk.Label(self.master, text="Click here to go to login", fg="blue", cursor="hand2")
        self.instruction_label.pack(pady=10)
        self.instruction_label.bind("<Button-1>", lambda e: self.open_login_window())

    def open_login_window(self):
        # Destroy the registration window
        self.master.destroy()  # Close the registration window
        login_root = tk.Tk()
        LoginApp(login_root)

class LoginApp:
    def __init__(self, master):
        self.master = master
        master.title("Login")

        self.label = tk.Label(master, text="Login")
        self.label.pack()

        self.username_label = tk.Label(master, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(master)
        self.username_entry.pack()

        self.password_label = tk.Label(master, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(master, show='*')
        self.password_entry.pack()

        self.login_button = tk.Button(master, text="Login", command=self.login_user)
        self.login_button.pack()

    def login_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in user_profiles and user_profiles[username]['password'] == password:
            self.master.destroy()
            self.open_bulb_selection_window(username)
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def open_bulb_selection_window(self, username):
        bulb_root = tk.Tk()
        BulbSelectionApp(bulb_root, username)

class BulbSelectionApp:
    def __init__(self, master, username):
        self.master = master
        self.username = username
        master.title("Challenge Response Selection")

        self.label = tk.Label(master, text="Select your secret color:")
        self.label.pack()

        self.selected_bulb = tk.StringVar()  # Variable to hold the selected color

        # Creating radio buttons for bulb colors
        for bulb_color in secret_colors:
            rb = tk.Radiobutton(master, text=bulb_color.capitalize(), variable=self.selected_bulb,
                                value=bulb_color, indicatoron=0, bg=bulb_color, width=20)
            rb.pack(pady=5)

        self.verify_button = tk.Button(master, text="Verify", command=self.verify_bulb)
        self.verify_button.pack(pady=20)

    def verify_bulb(self):
        selected_color = self.selected_bulb.get()
        expected_color = user_profiles[self.username]['secret_color']

        # Debugging output
        print(f"Selected Color: {selected_color}")
        print(f"Expected Color: {expected_color}")

        if selected_color == expected_color:
            messagebox.showinfo("Success", "You have successfully logged in!")
        else:
            messagebox.showerror("Error", "Authentication Failed...")

if __name__ == "__main__":
    root = tk.Tk()
    app = RegistrationApp(root)
    root.mainloop()
