import os
import shutil
import logging
from pathlib import Path
from rag_manager import RAGManager
import chromadb
from chromadb.config import Settings

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def reinitialize_rag():
    """Reinitialize the RAG system by cleaning up and recreating the vector database."""
    try:
        # Get the project root directory
        project_root = Path(__file__).parent.parent.parent.resolve()
        data_dir = project_root / "data"
        chroma_dir = data_dir / "chroma_db"
        
        # Clean up existing ChromaDB data
        if chroma_dir.exists():
            logger.info("Cleaning up existing ChromaDB data...")
            shutil.rmtree(chroma_dir)
        
        # Create fresh directories
        data_dir.mkdir(exist_ok=True)
        chroma_dir.mkdir(exist_ok=True)
        
        # Initialize ChromaDB with persistence
        logger.info("Initializing ChromaDB with persistence...")
        chroma_client = chromadb.PersistentClient(path=str(chroma_dir))
        
        # Reinitialize RAG manager
        logger.info("Reinitializing RAG manager...")
        rag_manager = RAGManager()
        
        # Verify the data was persisted
        collection = chroma_client.get_collection("command_examples")
        count = collection.count()
        logger.info(f"Verified collection has {count} examples")
        
        logger.info("RAG system reinitialized successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Failed to reinitialize RAG system: {str(e)}")
        return False

if __name__ == "__main__":
    reinitialize_rag() 