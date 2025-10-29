
import json
from rag.pipeline import RAGPipeline
from eval.rouge_utils import rouge_l

def run_eval(eval_file: str):
    pipe = RAGPipeline()
    results = []
    with open(eval_file, "r", encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            qid = row["qid"]
            q   = row["question"]
            gold= row["gold"]

            ans = pipe.run(q)

            score_rougeL = rouge_l(ans, gold)
            ok_len = len(ans.split()) > 20

            results.append({
                "qid": qid,
                "rougeL": score_rougeL,
                "long_enough": ok_len
            })

    for r in results:
        print(r)

if __name__ == "__main__":
    run_eval("eval/evalset.example.jsonl")
