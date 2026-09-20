import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


def load_products():
    with open("products.json", "r", encoding="utf-8") as file:
        return json.load(file)


def create_documents(products):
    documents = []

    for product in products:
        product_title = product["title"]

        for variant in product["variants"]["nodes"]:
            variant_title = variant["title"]
            price = variant["price"]
            inventory = variant["inventoryQuantity"]

            document = (
                f"Product: {product_title}. "
                f"Variant: {variant_title}. "
                f"Price: {price} USD. "
                f"Inventory: {inventory} units."
            )

            documents.append({
                "text": document,
                "product": product_title,
                "variant": variant_title,
                "price": price,
                "inventory": inventory
            })

    return documents


def create_vector_store(documents):
    print("Loading embedding model...")

    model = SentenceTransformer("all-MiniLM-L6-v2")

    texts = [document["text"] for document in documents]

    embeddings = model.encode(
        texts,
        convert_to_numpy=True
    ).astype("float32")

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    return model, index

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
if __name__ == "__main__":
    products = load_products()

    documents = create_documents(products)

    print(f"Created {len(documents)} RAG documents.")

    model, index = create_vector_store(documents)
    faiss.write_index(index, "product_index.faiss")

    with open("rag_documents.json", "w", encoding="utf-8") as file:
        json.dump(documents, file, indent=2)

    print(f"Embedding dimension: {index.d}")
    print(f"Vectors stored: {index.ntotal}")