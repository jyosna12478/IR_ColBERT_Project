from colbert import ColBERT

# Load the model directly from 'checkpoints/'
colbert = ColBERT.from_pretrained("checkpoints/")

print("ColBERT model loaded successfully!")
