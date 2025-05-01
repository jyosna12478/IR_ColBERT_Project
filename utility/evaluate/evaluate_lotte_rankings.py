import argparse
from collections import defaultdict
import jsonlines
import os
import sys
import math

def evaluate_dataset(query_type, dataset, split, k, data_rootdir, rankings_rootdir):
    data_path = os.path.join(data_rootdir, dataset, split)
    rankings_path = os.path.join(
        rankings_rootdir, split, f"{dataset}.{query_type}.ranking.tsv"
    )
    if not os.path.exists(rankings_path):
        print(f"[query_type={query_type}, dataset={dataset}] Success@{k}: ???")
        return
    rankings = defaultdict(list)
    with open(rankings_path, "r") as f:
        for line in f:
            items = line.strip().split("\t")
            qid, pid, rank = items[:3]
            qid = int(qid)
            pid = int(pid)
            rank = int(rank)
            rankings[qid].append(pid)
            assert rank == len(rankings[qid])

    success = 0
    total_recall = 0.0
    total_ndcg = 0.0
    qas_path = os.path.join(data_path, f"qas.{query_type}.jsonl")

    num_total_qids = 0
    with jsonlines.open(qas_path, mode="r") as f:
        for line in f:
            qid = int(line["qid"])
            num_total_qids += 1
            if qid not in rankings:
                print(f"WARNING: qid {qid} not found in {rankings_path}!", file=sys.stderr)
                continue
            answer_pids = set(line["answer_pids"])
            retrieved_pids = rankings[qid][:k]
       
            #@success@5
            if len(set(retrieved_pids).intersection(answer_pids)) > 0:
                success += 1


           #RECALL @ k
            recall = len(set(retrieved_pids).intersection(answer_pids)) / len(answer_pids)
            total_recall += recall

            #NDCG @ k
            dcg = 0.0
            for idx, pid in enumerate(retrieved_pids):
                if pid in answer_pids:
                    dcg += 1.0 / (math.log2(idx + 2))

            ideal_dcg = 0.0
            ideal_relevant = min(len(answer_pids), k)
            for i in range(ideal_relevant):
                ideal_dcg += 1.0 / (math.log2(i + 2))

            ndcg = dcg / ideal_dcg if ideal_dcg > 0 else 0.0
            total_ndcg += ndcg


    print(
        f"[query_type={query_type}, dataset={dataset}] "
        f"Success@{k}: {success / num_total_qids * 100:.1f} | "
        f"Recall@{k}: {total_recall / num_total_qids * 100:.1f} | "
        f"NDCG@{k}: {total_ndcg / num_total_qids * 100:.1f}"
    )


def main(args):
    for query_type in ["search", "forum"]:
        for dataset in [
            "writing",
        ]:
            evaluate_dataset(
                query_type,
                dataset,
                args.split,
                args.k,
                args.data_dir,
                args.rankings_dir,
            )
        print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LoTTE evaluation script")
    parser.add_argument("--k", type=int, default=5, help="Success@k")
    parser.add_argument(
        "-s", "--split", choices=["dev", "test"], required=True, help="Split"
    )
    parser.add_argument(
        "-d", "--data_dir", type=str, required=True, help="Path to LoTTE data directory"
    )
    parser.add_argument(
        "-r",
        "--rankings_dir",
        type=str,
        required=True,
        help="Path to LoTTE rankings directory",
    )
    args = parser.parse_args()
    main(args)
