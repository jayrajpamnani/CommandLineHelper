from src.utils.rag_manager import RAGManager

def test_rag():
    rag = RAGManager()
    
    test_queries = [
        "list all files in current directory",
        "show disk usage",
        "find python files",
        "show last lines of a file",
        "search for a word in files"
    ]
    
    for query in test_queries:
        print(f"\n{'='*80}")
        print(f"Query: {query}")
        print('='*80)
        
        similar_examples = rag.find_similar_examples(query)
        
        print("\nSimilar examples found:")
        for ex in similar_examples:
            print(f"\nNatural Language: {ex['nl']}")
            print(f"Bash Command: {ex['bash']}")
            print(f"Similarity Score: {ex['similarity']:.2f}")

if __name__ == "__main__":
    test_rag() 