import re
from retrieval import load_products, search_products
from pricing import compute_price, check_inventory
from llm import generate_answer


def find_variant(product, query):
    query_words = set(
        word.strip(".,?!:;()[]{}\"'")
        for word in query.lower().split()
    )

    variants = product["variants"]["nodes"]

    # If the product has only one variant, use it
    if len(variants) == 1:
        return variants[0]

    # For products with multiple variants, match the variant name
    for variant in variants:
        variant_title = variant["title"].lower().strip()

        if variant_title in query_words:
            return variant

    return None

def build_product_info(product, variant, quantity=1):
    price = float(variant["price"])
    inventory = variant["inventoryQuantity"]

    # The active Shopify discount:
    # 30% off The Complete Snowboard (Ice), minimum quantity 3.
    discount_percent = 0
    minimum_quantity = 1

    if (
        product["title"] == "The Complete Snowboard"
        and variant["title"] == "Ice"
    ):
        discount_percent = 30
        minimum_quantity = 3

    pricing = compute_price(
        price,
        discount_percent,
        quantity,
        minimum_quantity,
        currency="INR"
    )

    return {
        "product": product["title"],
        "variant": variant["title"],
        "inventory": inventory,
        "availability": check_inventory(inventory),
        "pricing": pricing
    }


def main():
    products = load_products()

    print("AI Product & Pricing Assistant")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("You: ")

        if question.lower() == "exit":
            print("Goodbye!")
            break

        results = search_products(question, products)

        if not results:
            print("Assistant: I couldn't find a matching product.\n")
            continue

        product = results[0]
        variant = find_variant(product, question)

        quantity_match = re.search(r"\b(\d+)\b", question)
        quantity = int(quantity_match.group(1)) if quantity_match else 1

        product_info = build_product_info(
            product,
            variant,
            quantity
        )

        answer = generate_answer(
            question,
            product_info
        )

        print("Assistant:", answer)
        print()


if __name__ == "__main__":
    main()