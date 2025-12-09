import json

class Portfolio:
    def __init__(self):
        self.holdings = []  # List of dicts: [{'id': 'bitcoin', 'amount': 1.0}, ...]
        self.prices = {}  # Dict to cache prices: {'bitcoin': 50000.0, ...}

    def add_crypto(self, crypto_id, amount):
        """Add a cryptocurrency to the portfolio."""
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        # Check if already exists, if so, update amount
        for holding in self.holdings:
            if holding['id'] == crypto_id:
                holding['amount'] += amount
                return
        self.holdings.append({'id': crypto_id, 'amount': amount})

    def remove_crypto(self, crypto_id):
        """Remove a cryptocurrency from the portfolio."""
        self.holdings = [h for h in self.holdings if h['id'] != crypto_id]

    def update_amount(self, crypto_id, new_amount):
        """Update the amount of a cryptocurrency."""
        if new_amount <= 0:
            raise ValueError("Amount must be positive.")
        for holding in self.holdings:
            if holding['id'] == crypto_id:
                holding['amount'] = new_amount
                return
        raise ValueError(f"Cryptocurrency {crypto_id} not in portfolio.")

    def fetch_prices(self):
        """Fetch current prices for all holdings using CoinGecko API."""
        if not self.holdings:
            return
        ids = [h['id'] for h in self.holdings]
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={','.join(ids)}&vs_currencies=usd"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raises HTTPError for bad responses
            data = response.json()
            self.prices = {crypto_id: data[crypto_id]['usd'] for crypto_id in ids if crypto_id in data}
        except requests.exceptions.RequestException as e:
            print(f"Error fetching prices: {e}")
            self.prices = {}  # Reset prices on error
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            self.prices = {}

    def calculate_value(self):
        """Calculate the total value of the portfolio."""
        total = 0.0
        for holding in self.holdings:
            crypto_id = holding['id']
            amount = holding['amount']
            price = self.prices.get(crypto_id, 0.0)
            total += amount * price
        return total

    def display_portfolio(self):
        """Display the portfolio holdings and total value."""
        if not self.holdings:
            print("Portfolio is empty.")
            return
        print("Portfolio Holdings:")
        for holding in self.holdings:
            crypto_id = holding['id']
            amount = holding['amount']
            price = self.prices.get(crypto_id, 'N/A')
            value = amount * price if isinstance(price, (int, float)) else 'N/A'
            print(f"  {crypto_id}: {amount} units @ ${price} each = ${value}")
        total_value = self.calculate_value()
        print(f"Total Portfolio Value: ${total_value:.2f}")

def main():
    portfolio = Portfolio()
    while True:
        print("\nPortfolio Tracker Menu:")
        print("1. Add Cryptocurrency")
        print("2. Remove Cryptocurrency")
        print("3. Update Amount")
        print("4. Fetch Prices and Display Portfolio")
        print("5. Exit")
        choice = input("Choose an option: ").strip()
        
        if choice == '1':
            crypto_id = input("Enter cryptocurrency ID (e.g., bitcoin): ").strip().lower()
            try:
                amount = float(input("Enter amount: "))
                portfolio.add_crypto(crypto_id, amount)
                print(f"Added {amount} of {crypto_id}.")
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == '2':
            crypto_id = input("Enter cryptocurrency ID to remove: ").strip().lower()
            portfolio.remove_crypto(crypto_id)
            print(f"Removed {crypto_id}.")
        elif choice == '3':
            crypto_id = input("Enter cryptocurrency ID: ").strip().lower()
            try:
                new_amount = float(input("Enter new amount: "))
                portfolio.update_amount(crypto_id, new_amount)
                print(f"Updated {crypto_id} to {new_amount}.")
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == '4':
            portfolio.fetch_prices()
            portfolio.display_portfolio()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()