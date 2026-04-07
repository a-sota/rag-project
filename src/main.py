from retrieve import Retriever
from generate import Generator


def main():
    retriever = Retriever()
    generator = Generator()

    while True:
        query = input("質問を入力してください: ").strip()
        if query.lower() in {"exit", "quit"}:
            break

        results = retriever.search(query, top_k=3)

        print("\n--- 検索結果 ---")
        for i, result in enumerate(results, start=1):
            print(f"[{i}] score={result['score']:.4f}")
            print(result["document"]["text"])
            print()

        answer = generator.answer(query, results)

        print("--- 生成回答 ---")
        print(answer)
        print()


if __name__ == "__main__":
    main()