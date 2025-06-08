import json
from pathlib import Path
from typing import List, Dict, Any
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import os
import logging
import shutil

logger = logging.getLogger(__name__)

class RAGManager:
    def __init__(self, examples_file: str = None):
        if examples_file is None:
            # Use absolute path based on project root
            project_root = Path(__file__).parent.parent.parent.resolve()
            examples_file = project_root / 'src' / 'data' / 'command_examples.json'
        self.examples_file = Path(examples_file)
        
        # Ensure examples file exists
        if not self.examples_file.exists():
            raise FileNotFoundError(f"Examples file not found at {self.examples_file}")
            
        self.examples = self._load_examples()
        
        # Create data directory and chroma_db subdirectory
        self.data_dir = Path("data")
        self.chroma_dir = self.data_dir / "chroma_db"
        self.data_dir.mkdir(exist_ok=True)
        self.chroma_dir.mkdir(exist_ok=True)
        
        # Initialize ChromaDB with proper error handling
        try:
            logger.info("Initializing ChromaDB...")
            self.chroma_client = chromadb.PersistentClient(path=str(self.chroma_dir))
            logger.info("ChromaDB initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {str(e)}")
            # Clean up and retry
            if self.chroma_dir.exists():
                shutil.rmtree(self.chroma_dir)
            self.chroma_dir.mkdir(exist_ok=True)
            self.chroma_client = chromadb.PersistentClient(path=str(self.chroma_dir))
        
        # Initialize Sentence Transformer
        try:
            logger.info("Loading Sentence Transformer model...")
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("Sentence Transformer model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load Sentence Transformer model: {str(e)}")
            raise
        
        # Create or get collection with error handling
        try:
            self.collection = self.chroma_client.get_or_create_collection(
                name="command_examples",
                metadata={"hnsw:space": "cosine"}
            )
            logger.info("Collection created/retrieved successfully")
        except Exception as e:
            logger.error(f"Failed to create/retrieve collection: {str(e)}")
            raise
        
        # Initialize or update the vector database
        self._initialize_or_update_vector_db()
    
    def _load_examples(self) -> List[Dict[str, str]]:
        """Load examples from JSON file."""
        try:
            with open(self.examples_file, 'r') as f:
                data = json.load(f)
            if not isinstance(data, dict) or 'examples' not in data:
                raise ValueError("Invalid examples file format")
            return data['examples']
        except Exception as e:
            logger.error(f"Failed to load examples: {str(e)}")
            raise
    
    def _initialize_or_update_vector_db(self):
        """Initialize or update the vector database with examples."""
        logger.info("Initializing/updating vector database...")
        
        try:
            # Get current examples from the database
            current_count = self.collection.count()
            logger.info(f"Current examples in database: {current_count}")
            
            if current_count == 0:
                # Initialize the database
                self._add_examples_to_db(self.examples)
                logger.info(f"Initialized database with {len(self.examples)} examples")
            else:
                # Update the database with new examples
                self._update_database()
        except Exception as e:
            logger.error(f"Failed to initialize/update vector database: {str(e)}")
            # If there's an error, try to reset the database
            if self.chroma_dir.exists():
                shutil.rmtree(self.chroma_dir)
            self.chroma_dir.mkdir(exist_ok=True)
            self.collection = self.chroma_client.get_or_create_collection(
                name="command_examples",
                metadata={"hnsw:space": "cosine"}
            )
            self._add_examples_to_db(self.examples)
    
    def _add_examples_to_db(self, examples: List[Dict[str, str]]):
        """Add examples to the vector database."""
        try:
            # Prepare data for batch insertion
            ids = [str(i) for i in range(len(examples))]
            documents = [ex['nl'] for ex in examples]
            metadatas = [{"bash_command": ex['bash']} for ex in examples]
            
            # Get embeddings
            logger.info("Generating embeddings...")
            embeddings = self.embedding_model.encode(documents)
            
            # Add to collection
            self.collection.add(
                ids=ids,
                embeddings=embeddings.tolist(),
                documents=documents,
                metadatas=metadatas
            )
            logger.info(f"Added {len(examples)} examples to database")
        except Exception as e:
            logger.error(f"Failed to add examples to database: {str(e)}")
            raise
    
    def _update_database(self):
        """Update the database with new examples."""
        try:
            # Get all current examples from the database
            current_examples = self.collection.get()
            current_nl = set(current_examples['documents'])
            
            # Find new examples
            new_examples = [
                ex for ex in self.examples 
                if ex['nl'] not in current_nl
            ]
            
            if new_examples:
                logger.info(f"Found {len(new_examples)} new examples to add")
                # Add new examples with IDs continuing from the last one
                start_id = len(current_examples['ids'])
                self._add_examples_to_db(new_examples)
            else:
                logger.info("No new examples to add")
        except Exception as e:
            logger.error(f"Failed to update database: {str(e)}")
            raise
    
    def find_similar_examples(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Find similar examples based on the input query."""
        try:
            # Get query embedding
            query_embedding = self.embedding_model.encode(query)
            
            # Search in collection
            results = self.collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=top_k
            )
            
            similar_examples = []
            for i in range(len(results['documents'][0])):
                similar_examples.append({
                    'nl': results['documents'][0][i],
                    'bash': results['metadatas'][0][i]['bash_command'],
                    'similarity': float(results['distances'][0][i])
                })
                
            return similar_examples
        except Exception as e:
            logger.error(f"Failed to find similar examples: {str(e)}")
            return []
    
    def get_relevant_context(self, query: str) -> str:
        """Get relevant context from similar examples."""
        try:
            similar_examples = self.find_similar_examples(query)
            
            if not similar_examples:
                return "No similar examples found."
            
            context = "Here are some similar examples:\n\n"
            for ex in similar_examples:
                context += f"Natural Language: {ex['nl']}\n"
                context += f"Bash Command: {ex['bash']}\n"
                context += f"Similarity: {ex['similarity']:.2f}\n\n"
                
            return context
        except Exception as e:
            logger.error(f"Failed to get relevant context: {str(e)}")
            return "Error retrieving similar examples."
    
    def add_new_example(self, nl: str, bash: str):
        """Add a new example to both the JSON file and vector database."""
        try:
            # Add to JSON file
            self.examples.append({"nl": nl, "bash": bash})
            with open(self.examples_file, 'w') as f:
                json.dump({"examples": self.examples}, f, indent=4)
            
            # Add to vector database
            self._add_examples_to_db([{"nl": nl, "bash": bash}])
            logger.info(f"Added new example: {nl} -> {bash}")
        except Exception as e:
            logger.error(f"Failed to add new example: {str(e)}")
            raise 