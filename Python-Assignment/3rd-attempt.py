import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, simpledialog
import requests
from datetime import datetime, timedelta

# Your API key and base URL for the currency API
API_KEY = "fca_live_GdR82iAVj8ureJfnvmKEcGr2RQhJubKUfqux9Oco"  # Replace with your actual API key
BASE_URL = "https://api.freecurrencyapi.com/v1/"

class CurrencyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")
        self.root.geometry("500x400")

        self.create_frames()
        self.create_page1()

        # Fetch available currencies when the app starts
        self.available_currencies = self.get_available_currencies()

    def create_frames(self):
        self.frame1 = ttk.Frame(self.root)
        self.frame1.pack(pady=20)

    def create_page1(self):
        # Label for Base Currency
        self.base_currency_label = ttk.Label(self.frame1, text="Base Currency", font=("Helvetica", 12))
        self.base_currency_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        # Base Currency Entry (Search functionality for base currency)
        self.base_currency_entry = ttk.Entry(self.frame1, font=("Helvetica", 12))
        self.base_currency_entry.grid(row=1, column=0, padx=10, pady=5)
        self.base_currency_entry.bind("<KeyRelease>", self.update_suggestions_base)

        # Label for Target Currency
        self.target_currency_label = ttk.Label(self.frame1, text="Target Currency", font=("Helvetica", 12))
        self.target_currency_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # Target Currency Entry (Search functionality for target currency)
        self.target_currency_entry = ttk.Entry(self.frame1, font=("Helvetica", 12))
        self.target_currency_entry.grid(row=1, column=1, padx=10, pady=5)
        self.target_currency_entry.bind("<KeyRelease>", self.update_suggestions_target)

        # Result Label
        self.result_label = ttk.Label(self.frame1, text="Result: ", font=("Helvetica", 12))
        self.result_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Entry for Amount
        self.amount_entry = ttk.Entry(self.frame1, text="Entry for Amount: ", font=("Helvetica", 12))
        self.amount_entry.grid(row=3, column=0, padx=10, pady=5)

        # Convert Button (Using tk.Button instead of ttk.Button)
        self.convert_button = tk.Button(self.frame1, text="Convert", command=self.convert_currency, width=20, font=("Helvetica", 12))
        self.convert_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        # History Button (Using tk.Button instead of ttk.Button)
        self.history_button = tk.Button(self.frame1, text="View Historical Rates", command=self.view_historical_data, width=20, font=("Helvetica", 12))
        self.history_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        # Search for Currency Button (Using tk.Button instead of ttk.Button)
        self.search_button = tk.Button(self.frame1, text="Search Currency", command=self.search_currency, width=20, font=("Helvetica", 12))
        self.search_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        # Rate Notifications Button (Using tk.Button instead of ttk.Button)
        self.notification_button = tk.Button(self.frame1, text="Set Rate Notifications", command=self.set_rate_notification, width=20, font=("Helvetica", 12))
        self.notification_button.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

        # Suggestions Listbox for Base Currency
        self.suggestions_base = tk.Listbox(self.frame1, height=5, font=("Helvetica", 12))
        self.suggestions_base.grid(row=2, column=0, padx=10, pady=10)
        self.suggestions_base.grid_forget()  # Hide initially
        self.suggestions_base.bind("<Double-1>", self.on_select_base)

        # Suggestions Listbox for Target Currency
        self.suggestions_target = tk.Listbox(self.frame1, height=5, font=("Helvetica", 12))
        self.suggestions_target.grid(row=2, column=1, padx=10, pady=10)
        self.suggestions_target.grid_forget()  # Hide initially
        self.suggestions_target.bind("<Double-1>", self.on_select_target)

    def get_exchange_rate(self, base_currency, target_currency):
        url = f"{BASE_URL}latest"
        params = {
            "apikey": API_KEY,
            "base_currency": base_currency,
            "symbols": target_currency
        }
        response = requests.get(url, params=params)
        data = response.json()
        if response.status_code == 200:
            return data["data"][target_currency]
        else:
            messagebox.showerror("Error", "Unable to fetch exchange rate.")
            return None

    def get_available_currencies(self):
        url = f"{BASE_URL}currencies"
        params = {
            "apikey": API_KEY,
        }
        response = requests.get(url, params=params)
        data = response.json()
        if response.status_code == 200:
            return list(data["data"].keys())
        else:
            messagebox.showerror("Error", "Unable to fetch available currencies.")
            return []

    def convert_currency(self):
        base_currency = self.base_currency_entry.get().upper()
        target_currency = self.target_currency_entry.get().upper()
        amount = self.amount_entry.get()

        if not amount:
            messagebox.showerror("Input Error", "Please enter an amount.")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Input Error", "Amount must be a valid number.")
            return

        rate = self.get_exchange_rate(base_currency, target_currency)

        if rate:
            result = amount * rate
            self.result_label.config(text=f"Result: {result:.2f} {target_currency}")

    def update_suggestions_base(self, event):
        search_term = self.base_currency_entry.get().upper()
        self.update_suggestions(search_term, self.suggestions_base)

    def update_suggestions_target(self, event):
        search_term = self.target_currency_entry.get().upper()
        self.update_suggestions(search_term, self.suggestions_target)

    def update_suggestions(self, search_term, suggestions_listbox):
        suggestions_listbox.delete(0, tk.END)  # Clear previous suggestions
        matched_currencies = [currency for currency in self.available_currencies if search_term in currency]

        for currency in matched_currencies:
            suggestions_listbox.insert(tk.END, currency)

        if matched_currencies:
            suggestions_listbox.grid()
        else:
            suggestions_listbox.grid_forget()

    def on_select_base(self, event):
        # Logic to handle selection from the base currency suggestions
        selected_currency = self.suggestions_base.get(self.suggestions_base.curselection())
        self.base_currency_entry.delete(0, tk.END)
        self.base_currency_entry.insert(0, selected_currency)
        self.suggestions_base.grid_forget()  # Hide suggestions after selection

    def on_select_target(self, event):
        # Logic to handle selection from the target currency suggestions
        selected_currency = self.suggestions_target.get(self.suggestions_target.curselection())
        self.target_currency_entry.delete(0, tk.END)
        self.target_currency_entry.insert(0, selected_currency)
        self.suggestions_target.grid_forget()  # Hide suggestions after selection

    def view_historical_data(self):
        base_currency = self.base_currency_entry.get().upper()
        target_currency = self.target_currency_entry.get().upper()

        # Get historical data (example: 30 days ago)
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

        url = f"{BASE_URL}historical"
        params = {
            "apikey": API_KEY,
            "base_currency": base_currency,
            "symbols": target_currency,
            "start_date": start_date,
            "end_date": end_date
        }

        response = requests.get(url, params=params)
        data = response.json()

        if response.status_code == 200:
            historical_rates = data['data']
            historical_data = f"Rates from {start_date} to {end_date}:\n"
            for date, rates in historical_rates.items():
                historical_data += f"{date}: {rates[target_currency]:.2f} {target_currency}\n"
            messagebox.showinfo("Historical Data", historical_data)
        else:
            messagebox.showerror("Error", "Unable to fetch historical data.")

    def search_currency(self):
        search_term = simpledialog.askstring("Search Currency", "Enter currency code (e.g., USD, EUR):")
        if search_term:
            # Show the exchange rate for the search term
            rate = self.get_exchange_rate("USD", search_term.upper())
            if rate:
                messagebox.showinfo("Currency Search", f"1 USD = {rate:.2f} {search_term.upper()}")
            else:
                messagebox.showerror("Error", "Currency not found.")

    def set_rate_notification(self):
        target_rate = simpledialog.askfloat("Set Rate Notification", "Enter the exchange rate you want to be notified about:")
        if target_rate:
            messagebox.showinfo("Rate Notification", f"You will be notified when the exchange rate reaches {target_rate:.2f}.")
            
if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyApp(root)
    root.mainloop()
