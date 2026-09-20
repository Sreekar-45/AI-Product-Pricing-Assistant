import json
import re

import faiss
from sentence_transformers import SentenceTransformer

from pricing import compute_price, check_inventory
from llm import generate_answer
from voice_input import listen
from tts import speak

def load_rag_documents():
    with open("rag_documents.json", "r", encoding="utf-8") as file:
        return json.load(file)


def load_vector_store():
    return faiss.read_index("product_index.faiss")


def load_embedding_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


def search_rag(query, model, index, documents, top_k=3):
    query_embedding = model.encode(
        [query],
        convert_to_numpy=True
    ).astype("float32")

    distances, indices = index.search(query_embedding, top_k)

    results = []

    for distance, index_position in zip(distances[0], indices[0]):
        if index_position == -1:
            continue

        result = documents[index_position].copy()
        result["similarity_distance"] = float(distance)

        results.append(result)

    return results


def extract_quantity(question):
    quantity_match = re.search(r"\b(\d+)\b", question)

    if quantity_match:
        return int(quantity_match.group(1))

    return 1


def find_best_result(results, question):
    question_lower = question.lower()

    # Prefer an exact product or variant name when it appears in the question.
    for result in results:
        product_name = result["product"].lower()
        variant_name = result["variant"].lower()

        if (
            product_name in question_lower
            or variant_name in question_lower
        ):
            return result

    return results[0] if results else None


def build_verified_product_info(result, quantity):
    base_price = float(result["price"])
    inventory = int(result["inventory"])

    discount_percent = 0
    minimum_quantity = 1

    try:
        with open("discounts.json", "r", encoding="utf-8") as file:
            discounts = json.load(file)
    
        for discount in discounts:
            if discount["status"] != "ACTIVE":
                continue
    
            summary = discount.get("summary") or ""
    
            if (
                result["product"] in summary
                and result["variant"] in summary
            ):
                percent_match = re.search(r"(\d+)%", summary)
                quantity_match = re.search(
                    r"Minimum quantity of (\d+)",
                    summary
                )
    
                if percent_match:
                    discount_percent = int(percent_match.group(1))
    
                if quantity_match:
                    minimum_quantity = int(quantity_match.group(1))
    
                break
    
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    pricing = compute_price(
        base_price,
        discount_percent,
        quantity,
        minimum_quantity,
        currency="INR"
    )

    if inventory <= 0:
        availability = "Out of stock"
    elif quantity > inventory:
        availability = (
            f"Only {inventory} units are available. "
            f"The requested quantity of {quantity} cannot be fulfilled."
        )
    else:
        availability = f"{inventory} units available"

    return {
        "product": result["product"],
        "variant": result["variant"],
        "inventory": inventory,
        "availability": availability,
        "pricing": pricing
    }


def main():
    print("Loading RAG system...")

    documents = load_rag_documents()
    index = load_vector_store()
    model = load_embedding_model()

    print("RAG system ready.\n")

    print("AI Product & Pricing Assistant")
    print("Type 'exit' to quit.\n")

    while True:
        mode = input("Choose mode (text/voice/exit): ").strip().lower()
        if mode == "exit":
            print("Goodbye!")
            break

        if mode == "voice":
            question = listen()
            print("You:", question)
        else:
            question = input("You: ").strip()
        
        if question.lower() == "exit":
            print("Goodbye!")
            break

        if not question:
            continue

        # Step 1: Semantic retrieval
        retrieved_documents = search_rag(
            question,
            model,
            index,
            documents,
            top_k=3
        )

        if not retrieved_documents:
            print("Assistant: I couldn't find a matching product.\n")
            continue

        # Step 2: Select the most relevant retrieved product
        best_result = find_best_result(
            retrieved_documents,
            question
        )

        if best_result is None:
            print("Assistant: I couldn't find a matching product.\n")
            continue

        # Step 3: Extract requested quantity
        quantity = extract_quantity(question)

        # Step 4: Deterministic price + inventory verification
        verified_product_info = build_verified_product_info(
            best_result,
            quantity
        )

        # Step 5: Generate natural-language response using retrieved context
        answer = generate_answer(
            question,
            retrieved_documents,
            verified_product_info
        )

        print("Assistant:", answer)
        if mode == "voice":
            speak(answer)
        print()


if __name__ == "__main__":
    main()