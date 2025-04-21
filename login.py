import tkinter as tk
from tkinter import messagebox, filedialog
import json

# Function to save the profile as JSON
def save_profile(username, email):
    profile_data = {"name": username, "email": email}
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
    if file_path:
        try:
            with open(file_path, 'w') as f:
                json.dump(profile_data, f)
            messagebox.showinfo("Profile Saved", "Profile has been saved successfully.")
            return file_path
        except Exception as e:
            messagebox.showerror("Error", f"Error saving profile: {e}")
    return None

# Function to load the profile from the saved JSON file
def load_profile_from_json(file_path):
    try:
        with open(file_path, 'r') as f:
            profile_data = json.load(f)
            return profile_data
    except Exception as e:
        messagebox.showerror("Error", f"Error loading profile: {e}")
    return None

# Function to handle the login process
def login(username_entry, password_entry, profile_file_path):
    username = username_entry.get()
    password = password_entry.get()

    profile_data = load_profile_from_json(profile_file_path)
    if profile_data:
        if profile_data.get("name") == username and profile_data.get("email") == password:
            messagebox.showinfo("Login Successful", "Welcome to the Smart Portfolio Generator!")
            login_window.destroy()
            open_main_app()
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password.")
    else:
        messagebox.showerror("Error", "Could not load profile. Please try again.")

# Function to open the main application
def open_main_app():
    import gui  # This imports your main app
    gui.run()   # Assumes you have a run() method in gui.py

# Function to create the profile window
def create_profile():
    profile_window = tk.Tk()
    profile_window.title("Create Profile")
    profile_window.geometry("400x300")

    tk.Label(profile_window, text="Enter Username:").pack(pady=10)
    username_entry = tk.Entry(profile_window)
    username_entry.pack(pady=5)

    tk.Label(profile_window, text="Enter Email:").pack(pady=10)
    email_entry = tk.Entry(profile_window)
    email_entry.pack(pady=5)

    def save_and_open_login():
        username = username_entry.get()
        email = email_entry.get()
        profile_file_path = save_profile(username, email)
        if profile_file_path:
            profile_window.destroy()
            open_login_window(profile_file_path)

    save_button = tk.Button(profile_window, text="Save Profile", command=save_and_open_login)
    save_button.pack(pady=20)

    # Start main loop here
    profile_window.mainloop()

# Function to open the login window
def open_login_window(profile_file_path):
    global login_window
    login_window = tk.Tk()
    login_window.title("Login")
    login_window.geometry("400x300")

    tk.Label(login_window, text="Username:").pack(pady=10)
    username_entry = tk.Entry(login_window)
    username_entry.pack(pady=5)

    tk.Label(login_window, text="Password:").pack(pady=10)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack(pady=5)

    login_button = tk.Button(
        login_window,
        text="Login",
        command=lambda: login(username_entry, password_entry, profile_file_path)
    )
    login_button.pack(pady=20)

    login_window.mainloop()

# Start the profile creation process
create_profile()
