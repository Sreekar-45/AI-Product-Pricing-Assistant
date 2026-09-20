import subprocess
import sys


def run_script(script_name):
    print(f"\nRunning {script_name}...\n")

    result = subprocess.run(
        [sys.executable, script_name],
        check=True
    )

    return result.returncode


def main():
    print("Refreshing Shopify product and discount data...")

    run_script("shopify_api.py")

    print("\nRebuilding RAG vector store...")

    run_script("rag.py")

    print("\nData refresh completed successfully.")


if __name__ == "__main__":
    main()