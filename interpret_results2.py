import jsonlines
from collections import defaultdict

# === Paths ===
qas_path = "data/lotte/writing/dev/qas.search.jsonl"
softmax_ranking_path = "experiments/lotte/retrieval_softmaxsim_lambda_20_log/dev/writing.search.ranking.tsv"
maxsim_ranking_path = "experiments/lotte/retrieval_lotte/2025-03/24/17.26.03/dev/writing.search.ranking.tsv"

# === Load relevance data ===
qid_to_answers = {}
with jsonlines.open(qas_path, mode='r') as reader:
    for obj in reader:
        qid_to_answers[int(obj['qid'])] = set(obj['answer_pids'])

# === Load rankings ===
def load_rankings(path):
    rankings = defaultdict(list)
    with open(path, 'r') as f:
        for line in f:
            qid, pid, rank, *_ = line.strip().split('\t')
            rankings[int(qid)].append(int(pid))
    return rankings

softmax_rankings = load_rankings(softmax_ranking_path)
maxsim_rankings = load_rankings(maxsim_ranking_path)

# === Analyze top-5 SoftMaxSim results ===
print("✅ SUCCESS CASE EXAMPLES:")
shown_success = 0
shown_failure = 0
MAX_EXAMPLES = 600  # updated from 3 to 20

for qid, retrieved in softmax_rankings.items():
    top5 = retrieved[:5]
    relevant = qid_to_answers[qid]
    has_relevant = len(set(top5).intersection(relevant)) > 0

    if has_relevant and shown_success < MAX_EXAMPLES:
        print(f"QID {qid}: Top 5 Results (SoftMaxSim): {top5}")
        print(f"Top 5 Results (MaxSim): {maxsim_rankings[qid][:5]}")
        print(f"Relevant: {relevant}")
        print("-" * 40)
        shown_success += 1

print("\n❌ FAILURE CASE EXAMPLES:")
for qid, retrieved in softmax_rankings.items():
    top5 = retrieved[:5]
    relevant = qid_to_answers[qid]
    has_relevant = len(set(top5).intersection(relevant)) > 0

    if not has_relevant and shown_failure < MAX_EXAMPLES:
        print(f"QID {qid}: Top 5 Results (SoftMaxSim): {top5}")
        print(f"Top 5 Results (MaxSim): {maxsim_rankings[qid][:5]}")
        print(f"Relevant: {relevant}")
        print("-" * 40)
        shown_failure += 1
