import tkinter as tk
from tkinter import messagebox
import requests

# ----------------- BACKEND -----------------

class Portfolio:
    def __init__(self):
        self.holdings = []
        self.prices = {}

    def add_crypto(self, crypto_id, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")

        for h in self.holdings:
            if h['id'] == crypto_id:
                h['amount'] += amount
                return

        self.holdings.append({"id": crypto_id, "amount": amount})

    def remove_crypto(self, crypto_id):
        self.holdings = [h for h in self.holdings if h['id'] != crypto_id]

    def update_amount(self, crypto_id, new_amount):
        for h in self.holdings:
            if h['id'] == crypto_id:
                h['amount'] = new_amount
                return
        raise ValueError("Crypto not found")

    def fetch_prices(self):
        if not self.holdings:
            raise ValueError("Portfolio empty")

        ids = ",".join([h["id"] for h in self.holdings])
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd"

        res = requests.get(url, timeout=10)
        res.raise_for_status()
        data = res.json()
        self.prices = {cid: data[cid]["usd"] for cid in data}

    def total_value(self):
        total = 0
        for h in self.holdings:
            total += h["amount"] * self.prices.get(h["id"], 0)
        return total

# ----------------- GUI -----------------

portfolio = Portfolio()

root = tk.Tk()
root.title("Crypto Portfolio Tracker")
root.geometry("600x450")

# ------------ INPUT FIELDS ------------

tk.Label(root, text="Crypto ID (bitcoin):").pack()
crypto_entry = tk.Entry(root)
crypto_entry.pack()

tk.Label(root, text="Amount:").pack()
amount_entry = tk.Entry(root)
amount_entry.pack()

# ------------ FUNCTIONS ------------

def add_crypto():
    try:
        cid = crypto_entry.get().strip().lower()
        amt = float(amount_entry.get())
        portfolio.add_crypto(cid, amt)
        messagebox.showinfo("Success", "Coin Added")
        show_portfolio()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def remove_crypto():
    cid = crypto_entry.get().strip().lower()
    portfolio.remove_crypto(cid)
    show_portfolio()
    messagebox.showinfo("Removed", "Coin Removed")

def update_crypto():
    try:
        cid = crypto_entry.get().strip().lower()
        amt = float(amount_entry.get())
        portfolio.update_amount(cid, amt)
        show_portfolio()
        messagebox.showinfo("Updated", "Amount Updated")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def fetch_prices():
    try:
        portfolio.fetch_prices()
        show_portfolio()
        messagebox.showinfo("Updated", "Prices Fetched")
    except Exception as e:
        messagebox.showerror("API Error", str(e))

def show_portfolio():
    display.delete("1.0", tk.END)

    if not portfolio.holdings:
        display.insert(tk.END, "Portfolio is empty\n")
        return

    for h in portfolio.holdings:
        price = portfolio.prices.get(h["id"], "N/A")
        value = h["amount"] * price if isinstance(price, float) else "N/A"
        display.insert(tk.END, f"{h['id']} | {h['amount']} | ${price} | ${value}\n")

    display.insert(tk.END, f"\nTotal Value: ${portfolio.total_value():.2f}")

# ------------ BUTTONS ------------

tk.Button(root, text="Add", width=15, command=add_crypto).pack(pady=4)
tk.Button(root, text="Remove", width=15, command=remove_crypto).pack(pady=4)
tk.Button(root, text="Update", width=15, command=update_crypto).pack(pady=4)
tk.Button(root, text="Fetch Live Prices", width=20, command=fetch_prices).pack(pady=4)

# ------------ DISPLAY ------------

display = tk.Text(root, height=12)
display.pack(pady=10)

root.mainloop()
