import json


def load_products():
    with open("products.json", "r", encoding="utf-8") as file:
        return json.load(file)


def search_products(query, products):
    stop_words = {
        "the", "is", "a", "an", "do", "you",
        "have", "what", "how", "much", "does",
        "for", "in", "of", "and", "please"
    }

    query_words = [
        word.strip(".,?!:;()[]{}\"'")
        for word in query.lower().split()
        if word.strip(".,?!:;()[]{}\"'") not in stop_words
        and not word.strip(".,?!:;()[]{}\"'").isdigit()
        ]

    matches = []

    for product in products:
        title = product["title"].lower()

        product_score = 0

        # Product title matching
        for word in query_words:
            if word in title:
                product_score += 2

        # Variant matching
        for variant in product["variants"]["nodes"]:
            variant_title = variant["title"].lower()

            for word in query_words:
                if word in variant_title:
                    product_score += 3

        if product_score > 0:
            matches.append((product_score, product))

    matches.sort(key=lambda item: item[0], reverse=True)

    # Return only the strongest matches
    if not matches:
        return []

    highest_score = matches[0][0]

    return [
        product
        for score, product in matches
        if score == highest_score
    ]


if __name__ == "__main__":
    products = load_products()

    results = search_products(
        "complete snowboard ice",
        products
    )

    for product in results:
        print(product["title"])