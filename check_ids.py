def check_unique_docids():
    """
    Extract and count unique document IDs from the collection.tsv file
    """
    collection_path = "data/lotte/writing/dev/collection.tsv"
    
    # Set to store unique doc IDs
    unique_docids = set()
    
    # Read the collection file
    with open(collection_path, 'r') as file:
        for line in file:
            parts = line.strip().split('\t')
            if len(parts) >= 1:
                docid = parts[0]
                unique_docids.add(docid)
    
    print(f"Total unique document IDs: {len(unique_docids)}")
    print(f"Sample document IDs (first 10): {list(unique_docids)[:10]}")
    
    # Check if your top documents are in the collection
    top_docs_in_results = [39414, 9032, 94914, 99641, 6755]  # From your ranking results
    for doc in top_docs_in_results:
        if str(doc) in unique_docids:
            print(f"Document ID {doc} is in the collection ✓")
        else:
            print(f"Document ID {doc} is NOT in the collection ✗")

# Run the function
check_unique_docids()
