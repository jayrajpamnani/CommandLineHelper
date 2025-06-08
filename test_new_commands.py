from src.utils.rag_manager import RAGManager

def test_new_commands():
    rag = RAGManager()
    
    test_queries = [
        "move my document.txt to the Documents folder",
        "show me the file permissions",
        "find the largest files in my home directory",
        "compare two text files side by side",
        "create a symbolic link to python3",
        "find empty directories",
        "show the first 10 lines of my log file",
        "sort my data file alphabetically",
        "count words in my document",
        "replace all instances of old with new in my file",
        "show lines with error in my log",
        "display file with line numbers",
        "convert text to uppercase",
        "extract second column from my csv",
        "show system uptime",
        "display CPU information",
        "show mounted drives",
        "list USB devices",
        "show kernel version",
        "display memory usage by process"
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
    test_new_commands() 