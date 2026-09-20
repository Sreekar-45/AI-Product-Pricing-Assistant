from forex_python.converter import CurrencyRates
currency_rates = CurrencyRates()
def usd_to_inr(amount):
    rate = currency_rates.get_rate("USD", "INR")
    return amount * rate
def compute_price(base_price, discount_percent=0, quantity=1, minimum_quantity=1, currency="INR"):
    # Convert Shopify USD unit price to INR
    unit_price_inr = usd_to_inr(base_price)

    # Calculate total price before discount
    original_total = unit_price_inr * quantity

    # Apply discount to the total only if minimum quantity is reached
    if discount_percent > 0 and quantity >= minimum_quantity:
        discount_amount = original_total * (discount_percent / 100)
        final_price = original_total - discount_amount
    else:
        discount_amount = 0
        final_price = original_total

    return {
        "unit_price": round(unit_price_inr, 2),
        "original_price": round(original_total, 2),
        "discount_percent": discount_percent if quantity >= minimum_quantity else 0,
        "discount_amount": round(discount_amount, 2),
        "final_price": round(final_price, 2),
        "quantity": quantity,
        "currency": currency
    }


def check_inventory(inventory_quantity):
    if inventory_quantity <= 0:
        return "Out of stock"

    return f"{inventory_quantity} units available"

if __name__ == "__main__":
    print("Currency conversion:")
    print("USD 100 =", round(usd_to_inr(100), 2), "INR")

    print("\nQuantity 1:")
    print(compute_price(699.95, 30, quantity=1, minimum_quantity=3))

    print("\nQuantity 3:")
    print(compute_price(699.95, 30, quantity=3, minimum_quantity=3))

    print("\nInventory:")
    print(check_inventory(10))
    print(check_inventory(0))