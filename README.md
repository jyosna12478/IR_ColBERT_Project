# ColBERT with SoftMaxSim Experiment

This repository includes modified ColBERT code to support a new aggregation method called **SoftMaxSim**, along with scripts for indexing, retrieval, and evaluation on the LoTTE dataset.

---

## 🔧 Setup

Make sure to install the required dependencies and activate your environment:

```bash
conda activate colbert_env
```

---

## 📦 Indexing

To build an index using ColBERT representations of passages:

```bash
python index_lotte.py
```

This script builds a FAISS index on the LoTTE writing dataset. Make sure to specify the checkpoint and experiment name inside the script.

---

## 🔍 Retrieval

To perform retrieval with either MaxSim (default) or SoftMaxSim:

```bash
python retrieval_lotte.py --softmax True
```

Use `--softmax True` to enable SoftMaxSim scoring. Set it to `False` to use the original MaxSim.

---

## 📊 Evaluation

To evaluate the retrieval results using Success@5, Recall@10, and NDCG@10:

```bash
python utility/evaluate/evaluate_lotte_rankings.py --split dev --k 5 --data_dir data/lotte --rankings_dir experiments/lotte/retrieval_softmaxsim_lambda_10_log/
```

This command computes the metrics for the search queries on the LoTTE writing dev set. Make sure the `writing.search.ranking.tsv` file is present under the correct folder structure.

---

## 📁 Folder Structure

- `index_lotte.py` → builds the index
- `retrieval_lotte.py` → runs retrieval with MaxSim or SoftMaxSim
- `utility/evaluate/evaluate_lotte_rankings.py` → computes Success@k, Recall@k, and NDCG@k
- `data/lotte/` → contains the LoTTE dataset files
- `experiments/lotte/` → stores index and retrieval outputs

---

Feel free to fork or cite if this helps your research!
