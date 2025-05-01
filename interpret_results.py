import jsonlines
from collections import defaultdict

# === CONFIG ===
qas_file = "data/lotte/writing/dev/qas.search.jsonl"
ranking_file = "experiments/lotte/retrieval_softmaxsim_lambda_10_log/dev/writing.search.ranking.tsv"
TOP_K = 5

# === Load ground-truth answer_pids ===
ground_truth = {}
queries = {}
with jsonlines.open(qas_file, "r") as reader:
    for item in reader:
        qid = int(item["qid"])
        ground_truth[qid] = set(item["answer_pids"])
        queries[qid] = item["query"]

# === Load rankings ===
rankings = defaultdict(list)
with open(ranking_file, "r") as f:
    for line in f:
        qid, pid, rank, score = line.strip().split("\t")
        qid = int(qid)
        pid = int(pid)
        rankings[qid].append(pid)

# === Analyze ===
success_cases = []
failure_cases = []

for qid, predicted_pids in rankings.items():
    top_k = predicted_pids[:TOP_K]
    relevant = ground_truth.get(qid, set())

    if any(pid in relevant for pid in top_k):
        success_cases.append((qid, queries[qid], top_k, relevant))
    else:
        failure_cases.append((qid, queries[qid], top_k, relevant))

# === Print examples ===
print("\n✅ SUCCESS CASE EXAMPLE:")
for qid, query, top_k, relevant in success_cases[:3]:
    print(f"QID {qid}: {query}")
    print(f"Top {TOP_K} Results: {top_k}")
    print(f"Relevant: {relevant}")
    print("-" * 40)

print("\n❌ FAILURE CASE EXAMPLE:")
for qid, query, top_k, relevant in failure_cases[:3]:
    print(f"QID {qid}: {query}")
    print(f"Top {TOP_K} Results: {top_k}")
    print(f"Relevant: {relevant}")
    print("-" * 40)
