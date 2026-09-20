import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_answer(question, retrieved_documents, verified_product_info):
    context = "\n".join(
        document["text"]
        for document in retrieved_documents
    )

    prompt = f"""
You are an AI Product and Pricing Assistant for a Shopify store.

Answer the user's question using ONLY the verified product information
and retrieved context provided below.

Retrieved product context:
{context}

Verified product information:
{verified_product_info}

User question:
{question}

Rules:
- Do not invent products, variants, prices, discounts, or inventory.
- Use the verified product information for price and inventory.
- If the requested quantity exceeds inventory, clearly say that it cannot be fulfilled.
- If the product is out of stock, clearly say it is out of stock.
- Give a concise natural-language answer in 1-2 sentences.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content.strip()