
from colbert.data import Queries
from colbert.infra import Run, RunConfig, ColBERTConfig
from colbert import Searcher



if __name__ == '__main__':
    with Run().context(RunConfig(nranks=1, experiment="lotte")):

        config = ColBERTConfig(
            root="experiments/lotte/indexes",
            softmaxsim=True,        # 🔥 use SoftMaxSim!
            softmax_lambda=25 # 
        )
        
        # Initialize the Searcher with the correct index path
        searcher = Searcher(index="lotte.nbits=2", config=config)

        # Load queries
        queries = Queries("data/lotte/writing/dev/questions.search.tsv")

        # Perform retrieval
        ranking = searcher.search_all(queries, k=105)
        
#        original_file = "experiments/lotte/indexes/lotte.nbits=2/lotte.ranking.tsv"
#        formatted_file = "experiments/lotte/indexes/lotte.nbits=2/lotte.ranking.formatted.tsv"
        # Save results
        ranking.save("experiments/lotte/indexes/lotte.nbits=2/lotte.ranking.tsv")
        
        print("Retrieval completed! Results saved in lotte.ranking.tsv")
