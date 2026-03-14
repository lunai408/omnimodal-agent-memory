#!/usr/bin/env python3
"""Interactive demo — query the multimodal agent memory."""

from app.agent import query_memory

EXAMPLE_QUERIES = [
    "What issue did the customer mention regarding pricing?",
    "What decisions were made in the pricing review meeting?",
    "Show me anything related to Globex Corp",
    "What does the product roadmap look like?",
    "What's the churn rate?",
]


def main() -> None:
    print("Omnimodal Agent Memory — Interactive Demo")
    print("=" * 50)
    print("\nExample queries:")
    for i, q in enumerate(EXAMPLE_QUERIES, 1):
        print(f"  {i}. {q}")
    print("\nType a query (or 'quit' to exit).\n")

    while True:
        try:
            user_input = input("Query> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if not user_input or user_input.lower() in ("quit", "exit", "q"):
            print("Bye!")
            break

        # Allow selecting an example by number
        if user_input.isdigit():
            idx = int(user_input) - 1
            if 0 <= idx < len(EXAMPLE_QUERIES):
                user_input = EXAMPLE_QUERIES[idx]
                print(f"  → {user_input}")

        print("\nSearching memory and generating answer...\n")
        response = query_memory(user_input)

        print("Sources:")
        for i, src in enumerate(response.sources, 1):
            desc = f" — {src.description}" if src.description else ""
            print(
                f"  [{i}] ({src.modality.value}) {src.source_file}{desc}  "
                f"(score: {src.score:.3f})"
            )

        print(f"\nAnswer:\n{response.answer}\n")
        print("-" * 50 + "\n")


if __name__ == "__main__":
    main()
