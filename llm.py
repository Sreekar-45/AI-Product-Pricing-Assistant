import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_answer(question, product_data):
    prompt = f"""
You are a helpful Shopify product assistant.

Answer the customer's question using ONLY the verified product information below.

Product information:
{product_data}

Customer question:
{question}

Rules:
- Do not invent products, prices, discounts, or inventory.
- Use the provided price and inventory information exactly.
- Give a concise natural answer in 1-2 sentences.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": "You are a concise Shopify product assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    answer = generate_answer(
        "What is the price of the Complete Snowboard?",
        {
            "product": "The Complete Snowboard",
            "variant": "Ice",
            "price": "699.95",
            "inventory": 10
        }
    )

    print(answer)