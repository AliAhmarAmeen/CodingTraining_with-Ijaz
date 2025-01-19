import tkinter as tk
from tkinter import ttk, messagebox
import requests

API_KEY = "fca_live_GdR82iAVj8ureJfnvmKEcGr2RQhJubKUfqux9Oco"  # Replace with your FreeCurrencyAPI key
BASE_URL = "https://api.freecurrencyapi.com/v1/"

products = [
    {"name": "Product 1", "price": 10.0},
    {"name": "Product 2", "price": 20.0},
    {"name": "Product 3", "price": 30.0},
    {"name": "Product 4", "price": 40.0},
    {"name": "Product 5", "price": 50.0},
]

class CurrencyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")
        self.root.geometry("400x400")
        
        self.selected_currency = tk.StringVar()
        self.product_price = tk.StringVar()
        self.currencies = []

        self.create_widgets()
        self.load_currencies()

    def create_widgets(self):
        # Product Selection
        tk.Label(self.root, text="Select Product").pack(pady=10)
        self.product_combobox = ttk.Combobox(
            self.root, values=[product["name"] for product in products], state="readonly"
        )
        self.product_combobox.pack()
        self.product_combobox.bind("<<ComboboxSelected>>", self.update_price)

        # Price Label
        tk.Label(self.root, text="Price").pack(pady=10)
        self.price_label = tk.Label(self.root, textvariable=self.product_price, font=("Arial", 14))
        self.price_label.pack()

        # Currency Selection
        tk.Label(self.root, text="Select Currency").pack(pady=10)

        # Frame for Currency List and Scrollbar
        frame = tk.Frame(self.root)
        frame.pack(pady=10)
        scrollbar = ttk.Scrollbar(frame, orient="vertical")
        self.currency_listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, height=10)
        scrollbar.config(command=self.currency_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.currency_listbox.pack(side="left", fill="both", expand=True)
        self.currency_listbox.bind("<<ListboxSelect>>", self.convert_price)

    def load_currencies(self):
        """Load currency list from API."""
        try:
            response = requests.get(f"{BASE_URL}currencies", params={"apikey": API_KEY})
            response.raise_for_status()
            data = response.json()["data"]
            self.currencies = list(data.keys())
            for currency in self.currencies:
                self.currency_listbox.insert(tk.END, currency)
        except requests.RequestException as e:
            messagebox.showerror("Error", f"Failed to fetch currencies: {e}")

    def update_price(self, event):
        """Update product price when a new product is selected."""
        selected_product = self.product_combobox.get()
        for product in products:
            if product["name"] == selected_product:
                self.product_price.set(f"${product['price']}")
                break

    def convert_price(self, event):
        """Convert product price to the selected currency."""
        try:
            selected_currency = self.currency_listbox.get(self.currency_listbox.curselection())
            selected_product = self.product_combobox.get()

            if not selected_product or not selected_currency:
                return

            for product in products:
                if product["name"] == selected_product:
                    original_price = product["price"]
                    break

            response = requests.get(
                f"{BASE_URL}latest", params={"apikey": API_KEY, "currencies": selected_currency}
            )
            response.raise_for_status()
            rates = response.json()["data"]
            converted_price = original_price * rates[selected_currency]
            self.product_price.set(f"{converted_price:.2f} {selected_currency}")
        except requests.RequestException as e:
            messagebox.showerror("Error", f"Failed to convert currency: {e}")
        except IndexError:
            messagebox.showerror("Error", "Please select a currency!")

if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyApp(root)
    root.mainloop()
