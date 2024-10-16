import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
from collections import defaultdict
from datetime import datetime
import matplotlib.pyplot as plt
import calendar
from matplotlib.widgets import Button
import matplotlib

# File to store account details
ACCOUNTS_FILE = "accounts.json"

def load_accounts():
    if os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, "r") as file:
            try:
                accounts = json.load(file)
                if isinstance(accounts, dict):  # Ensure it's a dictionary
                    return accounts
                else:
                    return {}
            except json.JSONDecodeError:
                return {}
    else:
        return {}

def save_accounts(accounts):
    with open(ACCOUNTS_FILE, "w") as file:
        json.dump(accounts, file, indent=4)

def create_account_window():
    window = tk.Toplevel()
    window.title("Create Account")

    tk.Label(window, text="Username:").grid(row=0, column=0)
    username_entry = tk.Entry(window)
    username_entry.grid(row=0, column=1)

    tk.Label(window, text="Password:").grid(row=1, column=0)
    password_entry = tk.Entry(window, show="*")
    password_entry.grid(row=1, column=1)

    tk.Label(window, text="Confirm Password:").grid(row=2, column=0)
    confirm_password_entry = tk.Entry(window, show="*")
    confirm_password_entry.grid(row=2, column=1)

    tk.Label(window, text="Password Hint:").grid(row=3, column=0)
    hint_entry = tk.Entry(window)
    hint_entry.grid(row=3, column=1)

    tk.Label(window, text="Starting Budget:").grid(row=4, column=0)
    budget_entry = tk.Entry(window)
    budget_entry.grid(row=4, column=1)

    def create_account():
        username = username_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()
        password_hint = hint_entry.get()
        budget = budget_entry.get()

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        if not password_hint:
            messagebox.showerror("Error", "Password hint cannot be empty!")
            return

        accounts = load_accounts()

        if username in accounts:
            messagebox.showerror("Error", "Account with this username already exists!")
            return

        accounts[username] = {
            "Password": password,
            "Password Hint": password_hint,
            "Budget": float(budget),
            "Expenses": []
        }

        save_accounts(accounts)
        messagebox.showinfo("Success", "Account created successfully!")
        window.destroy()

    tk.Button(window, text="Create Account", command=create_account).grid(row=5, columnspan=2)
    
def login_window():
    window = tk.Toplevel()
    window.title("Log In")

    # Set window size
    window.geometry('300x150')  # Set width and height for the login window

    # Get screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate position x and y coordinates to center the window
    position_x = int((screen_width / 2) - (300 / 2))  # 300 is the width of the window
    position_y = int((screen_height / 2) - (150 / 2))  # 150 is the height of the window

    # Set the geometry of the window to the new coordinates
    window.geometry(f"+{position_x}+{position_y}")

    tk.Label(window, text="Username:").grid(row=0, column=0)
    username_entry = tk.Entry(window)
    username_entry.grid(row=0, column=1)

    tk.Label(window, text="Password:").grid(row=1, column=0)
    password_entry = tk.Entry(window, show="*")
    password_entry.grid(row=1, column=1)

    hint_button = None  # Initialize hint_button variable

    def show_hint():
        username = username_entry.get()
        accounts = load_accounts()
        if username in accounts:
            hint = accounts[username]["Password Hint"]
            messagebox.showinfo("Password Hint", f"Hint: {hint}")
        else:
            messagebox.showerror("Error", "Username not found!")

    def on_username_change(*args):
        nonlocal hint_button  # Use nonlocal to access the hint_button variable
        username = username_entry.get()
        accounts = load_accounts()
        if username in accounts:
            if not hint_button:  # If hint_button is not already created
                hint_button = tk.Button(window, text="Show Hint", command=show_hint)
                hint_button.grid(row=2, column=0, columnspan=2, pady=5)
        else:
            if hint_button:  # If hint_button exists, remove it
                hint_button.grid_forget()
                hint_button = None  # Reset the hint_button variable

    username_entry.bind("<KeyRelease>", on_username_change)  # Bind key release event to username entry

    def login():
        username = username_entry.get()
        password = password_entry.get()

        accounts = load_accounts()

        if username in accounts and accounts[username]["Password"] == password:
            messagebox.showinfo("Success", f"Welcome, {username}!")
            window.destroy()
            open_dashboard(username)
        else:
            if username in accounts:
                messagebox.showerror("Error", "Invalid password!")
            else:
                messagebox.showerror("Error", "Invalid username!")

    tk.Button(window, text="Log In", command=login).grid(row=3, columnspan=2, pady=5)

def open_dashboard(username):
    window = tk.Toplevel()
    window.title("Dashboard")

    # Set window size
    window.geometry('250x300')  # Set width and height for the dashboard window

    # Get screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate position x and y coordinates to center the window
    position_x = int((screen_width / 2) - (250 / 2))  # 400 is the width of the window
    position_y = int((screen_height / 2) - (300 / 2))  # 300 is the height of the window

    # Set the geometry of the window to the new coordinates
    window.geometry(f"+{position_x}+{position_y}")

    # Display welcome message
    tk.Label(window, text=f"Welcome, {username}!", font=("Helvetica", 16)).pack(pady=10)

    # Buttons for different functionalities
    tk.Button(window, text="Add Expense", command=lambda: add_expense(username)).pack(pady=5)
    tk.Button(window, text="Add Budget", command=lambda: add_budget(username)).pack(pady=5)
    tk.Button(window, text="Expense List", command=lambda: view_expense_list(username)).pack(pady=5)
    tk.Button(window, text="View Budget", command=lambda: view_budget(username)).pack(pady=5)
    tk.Button(window, text="View Report", command=lambda: view_report(username)).pack(pady=5)  # The "View Report" button
    tk.Button(window, text="Exit", command=window.destroy).pack(pady=5)

def add_expense(username):
    window = tk.Toplevel()
    window.title("Add Expense")

    tk.Label(window, text="Expense Name:").grid(row=0, column=0)
    name_entry = tk.Entry(window)
    name_entry.grid(row=0, column=1)

    tk.Label(window, text="Expense Amount:").grid(row=1, column=0)
    amount_entry = tk.Entry(window)
    amount_entry.grid(row=1, column=1)

    tk.Label(window, text="Expense Category:").grid(row=2, column=0)
    
    # Dropdown for category selection or new entry
    def update_categories():
        category_combobox['values'] = tuple(set(exp["category"] for exp in accounts[username]["Expenses"]))

    accounts = load_accounts()
    existing_categories = list(set(exp["category"] for exp in accounts[username]["Expenses"]))
    
    category_combobox = ttk.Combobox(window, values=existing_categories)
    category_combobox.grid(row=2, column=1)
    category_combobox.set("Select or add category")

    tk.Label(window, text="Date (YYYY-MM-DD):").grid(row=3, column=0)
    
    # Automatically set to current date
    current_date = datetime.now().strftime("%Y-%m-%d")
    date_entry = tk.Entry(window)
    date_entry.insert(0, current_date)  # Auto-fill with current date
    date_entry.grid(row=3, column=1)

    def save_expense():
        name = name_entry.get()
        amount = float(amount_entry.get())
        category = category_combobox.get()
        date = date_entry.get()

        accounts = load_accounts()

        if amount > accounts[username]["Budget"]:
            messagebox.showerror("Error", "Not enough budget to cover this expense!")
            return

        if not category:
            messagebox.showerror("Error", "Please select or enter a valid category!")
            return

        accounts[username]["Expenses"].append({"name": name, "amount": amount, "category": category, "date": date})
        accounts[username]["Budget"] -= amount  # Deduct the expense amount from the budget
        save_accounts(accounts)
        messagebox.showinfo("Success", "Expense added successfully!")
        window.destroy()

    tk.Button(window, text="Save Expense", command=save_expense).grid(row=4, columnspan=2)

def add_budget(username):
    window = tk.Toplevel()
    window.title("Add Budget")

    tk.Label(window, text="Amount to Add:").grid(row=0, column=0)
    amount_entry = tk.Entry(window)
    amount_entry.grid(row=0, column=1)

    def save_budget():
        amount = float(amount_entry.get())
        accounts = load_accounts()
        accounts[username]["Budget"] += amount
        save_accounts(accounts)
        messagebox.showinfo("Success", "Budget updated successfully!")
        window.destroy()

    tk.Button(window, text="Add Budget", command=save_budget).grid(row=1, columnspan=2)

def view_expense_list(username):
    accounts = load_accounts()
    expenses = accounts[username]["Expenses"]

    if not expenses:
        messagebox.showinfo("No Data", "No expenses recorded.")
        return

    # Group expenses by month and year
    monthly_expenses = defaultdict(list)
    for expense in expenses:
        date_str = expense.get("date", "")
        if date_str:
            expense_date = datetime.strptime(date_str, "%Y-%m-%d")
            month = expense_date.month
            year = expense_date.year
            monthly_expenses[(year, month)].append(expense)

    # Get the current month and year
    current_date = datetime.now()
    current_month = current_date.month
    current_year = current_date.year

    # Create the window to display the expenses
    window = tk.Toplevel()
    window.title("Expense List")

    list_frame = tk.Frame(window)
    list_frame.pack(fill=tk.BOTH, expand=True, pady=10)

    label_month_year = tk.Label(window, text="", font=("Helvetica", 14))
    label_month_year.pack(pady=5)

    def update_expense_list(selected_year, selected_month):
        """Update the displayed expenses for the selected month and year."""
        for widget in list_frame.winfo_children():
            widget.destroy()  # Clear the previous expense list

        month_name = calendar.month_name[selected_month]
        label_month_year.config(text=f"{month_name} {selected_year}")

        if (selected_year, selected_month) in monthly_expenses:
            for expense in monthly_expenses[(selected_year, selected_month)]:
                category = expense.get('category', 'No Category')
                date = expense.get('date', 'No Date')
                amount = expense['amount']
                name = expense['name']
                tk.Label(list_frame, text=f"{name} - ${amount:.2f} (Category: {category}, Date: {date})").pack()
        else:
            tk.Label(list_frame, text="No expenses for this month.").pack()

    def navigate_month(offset):
        """Navigate to the previous or next month."""
        nonlocal current_year, current_month
        current_month += offset
        if current_month < 1:
            current_month = 12
            current_year -= 1
        elif current_month > 12:
            current_month = 1
            current_year += 1
        update_expense_list(current_year, current_month)

    # Initial list
    update_expense_list(current_year, current_month)

    # Create "Previous" and "Next" buttons for navigation
    button_frame = tk.Frame(window)
    button_frame.pack(pady=5)

    btn_prev = tk.Button(button_frame, text="Previous", command=lambda: navigate_month(-1))
    btn_prev.pack(side=tk.LEFT, padx=10)

    btn_next = tk.Button(button_frame, text="Next", command=lambda: navigate_month(1))
    btn_next.pack(side=tk.RIGHT, padx=10)

    window.mainloop()

def view_budget(username):
    accounts = load_accounts()
    budget = accounts[username]["Budget"]
    messagebox.showinfo("Current Budget", f"Your current budget is: £{budget:.2f}")

def view_report(username):
    accounts = load_accounts()
    expenses = accounts[username]["Expenses"]

    if not expenses:
        messagebox.showinfo("No Data", "No expenses to show in the report.")
        return

    # Group expenses by month and category
    monthly_expenses = defaultdict(lambda: defaultdict(float))
    for expense in expenses:
        date_str = expense.get("date", "")
        if date_str:
            expense_date = datetime.strptime(date_str, "%Y-%m-%d")
            month = expense_date.month
            year = expense_date.year
            category = expense.get("category", "Uncategorized")
            monthly_expenses[(year, month)][category] += expense["amount"]

    # Get the current month and year
    current_date = datetime.now()
    current_month = current_date.month
    current_year = current_date.year

    fig, ax = plt.subplots(figsize=(6, 6))
    plt.subplots_adjust(left=0.3, right=0.7)  # Adjust plot to make space for buttons

    def update_chart(selected_year, selected_month):
        """Update pie chart with expenses for the selected month and year."""
        ax.clear()
        month_name = calendar.month_name[selected_month]
        title = f"Expense Report for {username} - {month_name} {selected_year}"

        if (selected_year, selected_month) in monthly_expenses:
            expense_categories = monthly_expenses[(selected_year, selected_month)]
            categories = list(expense_categories.keys())
            amounts = list(expense_categories.values())

            # Define custom labels with category name and amount spent underneath
            labels = [f'{category}\n(${amount:.2f})' for category, amount in zip(categories, amounts)]

            ax.pie(amounts, labels=labels, startangle=140)
            ax.set_title(title)

            # Add the current month's name to the top-right corner
            ax.text(1.1, 1.05, month_name, horizontalalignment='right', fontsize=12, color='blue')

            ax.axis('equal')  # Equal aspect ratio ensures that pie chart is drawn as a circle.
        else:
            ax.text(0.5, 0.5, f"No expenses for {month_name} {selected_year}", 
                    horizontalalignment='center', verticalalignment='center', fontsize=12)
        plt.draw()

    def navigate_month(event, offset):
        """Navigate to the previous or next month."""
        nonlocal current_year, current_month
        current_month += offset
        if current_month < 1:
            current_month = 12
            current_year -= 1
        elif current_month > 12:
            current_month = 1
            current_year += 1
        update_chart(current_year, current_month)

    # Initial chart
    update_chart(current_year, current_month)

    # Create "Previous" and "Next" buttons on the chart
    ax_prev = plt.axes([0.1, 0.45, 0.1, 0.05])  # Left button (previous)
    ax_next = plt.axes([0.8, 0.45, 0.1, 0.05])  # Right button (next)
    
    btn_prev = Button(ax_prev, 'Previous')
    btn_next = Button(ax_next, 'Next')

    # Bind buttons to navigation functions
    btn_prev.on_clicked(lambda event: navigate_month(event, -1))
    btn_next.on_clicked(lambda event: navigate_month(event, 1))

    plt.show()

def main():
    root = tk.Tk()
    root.title("Expense Tracker")

    tk.Button(root, text="Log In", command=login_window).pack(pady=10)
    tk.Button(root, text="Create Account", command=create_account_window).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()