AI Product & Pricing Assistant for Shopify

A lightweight AI-powered commerce assistant that retrieves product information from Shopify, validates inventory and pricing using deterministic Python logic, and generates natural-language answers using an LLM.

FEATURES

- Shopify Admin API integration
- Product and variant retrieval
- Inventory availability checking
- USD to INR currency conversion
- Quantity-based pricing
- Discount calculation
- Keyword-based product retrieval
- LLM-based natural-language responses
- Interactive terminal chatbot

ARCHITECTURE

User Question
    |
    v
Product Retrieval
    |
    v
Variant Selection
    |
    v
Inventory Validation
    |
    v
Price and Discount Calculation
    |
    v
LLM Response Generation
    |
    v
Natural-Language Answer

The LLM does not calculate prices or inventory. Python validates the Shopify data and performs the pricing calculations before the LLM generates the final response.

TECHNOLOGIES

- Python
- Shopify Admin GraphQL API
- Requests
- Groq API
- Python-dotenv
- Forex-Python
- JSON
- Git and GitHub

PROJECT STRUCTURE

AI-Product-Pricing-Assistant/
|-- main.py
|-- shopify_api.py
|-- retrieval.py
|-- pricing.py
|-- llm.py
|-- products.json
|-- requirements.txt
|-- .gitignore
|-- readme.md

SETUP

1. Clone the repository

git clone https://github.com/Sreekar-45/AI-Product-Pricing-Assistant.git
cd AI-Product-Pricing-Assistant

2. Create a virtual environment

python -m venv venv

3. Activate the virtual environment on Windows

venv\Scripts\activate

4. Install dependencies

pip install -r requirements.txt

5. Configure environment variables

Create a .env file containing:

SHOPIFY_STORE=your-store.myshopify.com
SHOPIFY_CLIENT_ID=your-client-id
SHOPIFY_CLIENT_SECRET=your-client-secret
GROQ_API_KEY=your-groq-api-key

Never commit .env or API credentials to GitHub.

6. Fetch Shopify product data

python shopify_api.py

This retrieves product, variant, price, and inventory information and stores it locally in products.json.

7. Run the assistant

python main.py

Example:

You: What is the price of 3 Complete Snowboard Ice?

Assistant: The 3-unit bundle of "The Complete Snowboard - Ice" is ₹140,929.71 (30% off the original ₹201,328.16). There are 10 units available.

DESIGN PRINCIPLE

The system separates business logic from language generation.

Python handles:
- Product retrieval
- Variant selection
- Inventory validation
- Currency conversion
- Discount calculation

The LLM handles:
- Natural-language response generation

This reduces the risk of generating incorrect product, pricing, or inventory information.

SCOPE

This project intentionally uses lightweight keyword-based retrieval rather than embeddings or a vector database.

Voice input, text-to-speech, multi-turn memory, deployment, and vector databases are outside the current scope.

AUTHOR

Sai Sreekar Reddy P

GitHub:
https://github.com/Sreekar-45