import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

SHOP = os.getenv("SHOPIFY_STORE")
CLIENT_ID = os.getenv("SHOPIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SHOPIFY_CLIENT_SECRET")


def get_access_token():
    url = f"https://{SHOP}/admin/oauth/access_token"

    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }

    response = requests.post(url, data=data)
    response.raise_for_status()

    return response.json()["access_token"]


def get_products(access_token):
    url = f"https://{SHOP}/admin/api/2026-07/graphql.json"

    query = """
    {
      products(first: 50) {
        nodes {
          id
          title
          status
          variants(first: 50) {
            nodes {
              id
              title
              price
              inventoryQuantity
            }
          }
        }
      }
    }
    """

    headers = {
        "X-Shopify-Access-Token": access_token,
        "Content-Type": "application/json"
    }

    response = requests.post(
        url,
        json={"query": query},
        headers=headers
    )

    response.raise_for_status()

    result = response.json()

    if "errors" in result:
        print("Shopify API error:")
        print(result["errors"])
        return []

    return result["data"]["products"]["nodes"]


def save_products(products):
    with open("products.json", "w", encoding="utf-8") as file:
        json.dump(products, file, indent=4)

    print(f"Saved {len(products)} products to products.json")

def get_discounts(access_token):
    url = f"https://{SHOP}/admin/api/2026-07/graphql.json"

    query = """
    {
      discountNodes(first: 20) {
        nodes {
          id
          discount {
            __typename

            ... on DiscountAutomaticBasic {
              title
              status
              summary
            }

            ... on DiscountAutomaticBxgy {
              title
              status
              summary
            }

            ... on DiscountCodeBasic {
              title
              status
              summary
            }

            ... on DiscountCodeBxgy {
              title
              status
              summary
            }
          }
        }
      }
    }
    """

    headers = {
        "X-Shopify-Access-Token": access_token,
        "Content-Type": "application/json"
    }

    response = requests.post(
        url,
        json={"query": query},
        headers=headers
    )

    response.raise_for_status()

    result = response.json()

    if "errors" in result:
        print("Shopify discount API error:")
        print(result["errors"])
        return

    discounts = result["data"]["discountNodes"]["nodes"]

    print(f"\nFound {len(discounts)} discounts:\n")

    for node in discounts:
        discount = node["discount"]

        if discount:
            print("Discount:", discount.get("title"))
            print("Type:", discount.get("__typename"))
            print("Status:", discount.get("status"))
            print("Summary:", discount.get("summary"))
            print("-" * 50)


if __name__ == "__main__":
    token = get_access_token()

    products = get_products(token)
    save_products(products)

    get_discounts(token)