import ast

def convert_ranking_format(input_file, output_file):
    """
    Convert a ranking file with array format to individual entries,
    ensuring that the best documents across all variations are kept.
    """
    # Dictionary to store the best score for each document per query
    best_scores = {}
    
    print(f"Processing file: {input_file}")
    print("Reading and parsing data...")
    
    # First pass: Find the best score for each document
    with open(input_file, 'r') as infile:
        for line in infile:
            # Split the line into columns
            parts = line.strip().split('\t')
            if len(parts) >= 4:  # Has at least 4 columns
                query_id = parts[0]
                try:
                    # Try to parse the doc array and score array
                    doc_array = ast.literal_eval(parts[1])
                    score_array = ast.literal_eval(parts[3])
                    
                    # Record the scores for each document
                    if query_id not in best_scores:
                        best_scores[query_id] = {}
                    
                    for doc_id, score in zip(doc_array, score_array):
                        doc_id = str(doc_id)  # Convert to string for consistency
                        if doc_id not in best_scores[query_id] or score > best_scores[query_id][doc_id]:
                            best_scores[query_id][doc_id] = score
                except (SyntaxError, ValueError) as e:
                    print(f"Error parsing line: {e}")
                    continue
    
    print(f"Found {len(best_scores)} unique queries")
    total_docs = sum(len(docs) for docs in best_scores.values())
    print(f"Total unique documents: {total_docs}")
    
    print(f"Writing formatted results to: {output_file}")
    
    # Second pass: Write the results in sorted order
    with open(output_file, 'w') as outfile:
        for query_id, doc_scores in best_scores.items():
            # Sort by score (descending)
            sorted_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
            
            # Write individual entries
            for rank, (doc_id, score) in enumerate(sorted_docs, 1):
                outfile.write(f"{query_id}\t{doc_id}\t{rank}\t{score}\n")
    
    print("Conversion complete!")

# Specify the input and output file paths manually
#input_file = "/home/stu2/s0/js1186/IR_Project/ColBERT/experiments/lotte/retrieval_lotte/2025-04/25/10.52.21/experiments/lotte/indexes/lotte.nbits=2/lotte.ranking.tsv"
#input_file = "/home/stu2/s0/js1186/IR_Project/ColBERT/experiments/lotte/retrieval_lotte/2025-04/25/12.09.15/experiments/lotte/indexes/lotte.nbits=2/lotte.ranking.tsv"
input_file = "/home/stu2/s0/js1186/IR_Project/ColBERT/experiments/lotte/retrieval_lotte/2025-04/25/12.47.53/experiments/lotte/indexes/lotte.nbits=2/lotte.ranking.tsv"
output_file = "/home/stu2/s0/js1186/IR_Project/ColBERT/experiments/lotte/retrieval_lotte/2025-04/25/10.52.21/experiments/lotte/indexes/lotte.nbits=2/lotte.ranking1.formatted.tsv"

# Convert the file
convert_ranking_format(input_file, output_file)

print("\nYou can view the results with:")
print(f"head -n 10 {output_file}")
