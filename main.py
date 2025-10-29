
import argparse
from rag.pipeline import RAGPipeline

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--top_k", type=int, default=None,
                        help="override Config.TOP_K for this session")
    args = parser.parse_args()

    pipe = RAGPipeline()

    print("PubChem RAG assistant (academic, safety-aware). Ctrl+C to exit.\n")
    while True:
        try:
            user_q = input(">>> ").strip()
            if not user_q:
                continue
            ans = pipe.run(user_q, top_k=args.top_k)
            print("\n" + ans + "\n")
        except KeyboardInterrupt:
            print("\n[Session ended]\n")
            break

if __name__ == "__main__":
    main()
