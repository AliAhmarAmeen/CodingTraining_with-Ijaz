import tkinter as tk
from tkinter import ttk, messagebox
import requests

# Dummy product data
products = [
    {"name": "Product 1", "price": 10.0},
    {"name": "Product 2", "price": 20.0},
    {"name": "Product 3", "price": 30.0},
    {"name": "Product 4", "price": 40.0},
    {"name": "Product 5", "price": 50.0},
]

# Currency API endpoint and key
API_URL = "https://api.exchangerate-api.com/v4/latest/USD"

class EcommerceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini E-Commerce App")
        self.root.geometry("600x600")
        self.root.resizable(False, False)

        # Initialize exchange rates
        self.exchange_rates = self.get_exchange_rates()

        # Selected currency
        self.selected_currency = tk.StringVar(value="USD")

        # UI Elements
        self.create_widgets()

    def create_widgets(self):
        # Header Label
        header = tk.Label(self.root, text="E-Commerce App", font=("Arial", 16, "bold"))
        header.pack(pady=10)

        # Product list label
        tk.Label(self.root, text="Products", font=("Arial", 14)).pack()

        # Treeview Frame (for centering)
        tree_frame = tk.Frame(self.root)
        tree_frame.pack(pady=10)

        # Product list
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("Name", "Price"),
            show="headings",
            height=8
        )
        self.tree.heading("Name", text="Product Name")
        self.tree.heading("Price", text="Price")
        self.tree.column("Name", width=200, anchor="center")
        self.tree.column("Price", width=100, anchor="center")
        self.tree.pack()

        # Populate product data
        self.populate_product_list("USD")

        # Searchable Dropdown for Currency
        tk.Label(self.root, text="Select Currency:", font=("Arial", 12)).pack(pady=5)

        dropdown_frame = tk.Frame(self.root)
        dropdown_frame.pack()

        # Search Entry
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(dropdown_frame, textvariable=self.search_var, font=("Arial", 12), width=30)
        self.search_entry.grid(row=0, column=0, padx=5)
        self.search_entry.bind("<KeyRelease>", self.update_currency_list)

        # Frame for Listbox and Scrollbar
        listbox_frame = tk.Frame(dropdown_frame)
        listbox_frame.grid(row=1, column=0, padx=5)

        # Currency Listbox with Scrollbar
        self.currency_listbox = tk.Listbox(listbox_frame, height=8, width=30)
        self.currency_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        # Scrollbar
        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.currency_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.currency_listbox.yview)

        # Listbox selection binding
        self.currency_listbox.bind("<<ListboxSelect>>", self.on_currency_select)

        # Populate listbox with currencies
        self.update_currency_list()

        # Checkout Button
        self.checkout_button = tk.Button(
            self.root, text="Checkout", command=self.checkout, font=("Arial", 12)
        )
        self.checkout_button.pack(pady=20)

    def get_exchange_rates(self):
        try:
            response = requests.get(API_URL)
            data = response.json()
            return data["rates"]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch exchange rates: {e}")
            return {"USD": 1.0}  # Fallback to USD only

    def populate_product_list(self, currency):
        # Clear existing data
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Insert updated data
        for product in products:
            price = product["price"] * self.exchange_rates.get(currency, 1.0)
            self.tree.insert("", "end", values=(product["name"], f"{price:.2f} {currency}"))

    def update_currency_list(self, event=None):
        # Filter currencies based on search
        search_text = self.search_var.get().lower()
        matching_currencies = [
            currency for currency in self.exchange_rates.keys() if search_text in currency.lower()
        ]

        # Update the listbox
        self.currency_listbox.delete(0, tk.END)
        for currency in matching_currencies:
            self.currency_listbox.insert(tk.END, currency)

    def on_currency_select(self, event=None):
        # Get the selected currency
        selection = self.currency_listbox.curselection()
        if selection:
            currency = self.currency_listbox.get(selection[0])
            self.selected_currency.set(currency)
            self.populate_product_list(currency)

    def checkout(self):
        currency = self.selected_currency.get()
        if currency not in self.exchange_rates:
            messagebox.showwarning("Warning", "Invalid currency selected!")
            return

        # Calculate total price in the selected currency
        total_price_usd = sum(product["price"] for product in products)
        exchange_rate = self.exchange_rates[currency]
        total_price_converted = total_price_usd * exchange_rate

        # Display total price
        messagebox.showinfo(
            "Checkout",
            f"Total Price:\n"
            f"{total_price_usd:.2f} USD = {total_price_converted:.2f} {currency}",
        )

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = EcommerceApp(root)
    root.mainloop()
