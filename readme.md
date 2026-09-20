# AI Product & Pricing Assistant for Shopify

An AI-powered commerce assistant that combines **Shopify product data, Retrieval-Augmented Generation (RAG), deterministic pricing and inventory validation, Voice AI, and Text-to-Speech** to answer product-related customer questions.

The system retrieves relevant Shopify product information using semantic search, validates pricing and inventory using Python, and then uses an LLM to generate a natural-language response.

---

## Key Features

- Shopify Admin GraphQL API integration
- Product and variant retrieval
- Automatic inventory retrieval
- Automatic Shopify discount retrieval
- Dynamic discount detection
- USD to INR price conversion
- Quantity-based price calculation
- Inventory validation
- Semantic product retrieval using embeddings
- FAISS vector database
- Retrieval-Augmented Generation (RAG)
- Groq LLM response generation
- Voice input using Whisper
- Text-to-Speech using pyttsx3
- Interactive text and voice modes
- Automatic Shopify data and RAG refresh

---

## System Architecture

```text
                    Shopify Store
                         |
                         v
              Shopify Admin GraphQL API
                         |
                         v
             products.json / discounts.json
                         |
                         v
                  RAG Document Creation
                         |
                         v
              Sentence Transformer Model
                         |
                         v
                    FAISS Index
                         |
                         |
User Question ----------+
      |
      v
 Text Input / Voice Input
      |          |
      |       Whisper
      |          |
      +----------+
           |
           v
    Semantic Retrieval
           |
           v
    Relevant Product Data
           |
           v
 Product / Variant Selection
           |
           v
 Price + Discount + Inventory
     Deterministic Validation
           |
           v
       Groq LLM
           |
           v
 Natural-Language Answer
           |
           v
     Text / TTS Output