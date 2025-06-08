from typing import Optional, Dict, Any
from llama_cpp import Llama
import os
from pathlib import Path
import logging
from src.prompts.templates import COMMAND_GENERATION_PROMPT
from src.utils.rag_manager import RAGManager
import re
import json

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ModelManager:
    def __init__(self, model_dir: str = "models"):
        self.model_dir = Path(__file__).parent.parent.parent / model_dir
        self.model: Optional[Llama] = None
        self.rag_manager = RAGManager()
        logger.info("ModelManager initialized")
        
    def load_models(self):
        """Load the CodeLlama model."""
        logger.info("[ModelManager] Loading CodeLlama model...")
        model_path = self.model_dir / "codellama-7b.gguf"
        if not model_path.exists():
            raise FileNotFoundError(f"Model not found at {model_path}")
        
        logger.info(f"[ModelManager] Model path: {model_path}")
        
        logger.info("[ModelManager] Initializing model...")
        self.model = Llama(
            model_path=str(model_path),
            n_ctx=2048,  # Context window
            n_threads=4,  # Adjust based on your CPU
            n_gpu_layers=0  # Set to higher value if using GPU
        )
        logger.info("[ModelManager] Model loaded successfully.")
    
    def process_input(self, text: str) -> str:
        """Process natural language input and generate bash command."""
        try:
            logger.info(f"[ModelManager] Processing input: {text}")
            
            # Find similar examples for context
            similar_examples = self.rag_manager.find_similar_examples(text)
            
            # Format examples for the prompt
            examples_context = "Here are some similar examples:\n\n"
            for ex in similar_examples:
                examples_context += f"Natural Language: {ex['nl']}\nBash Command: {ex['bash']}\nSimilarity: {ex['similarity']}\n\n"
            
            # Create the prompt
            prompt = f"""Task: Convert the following natural language instruction into a bash command.
Requirements:
1. Use standard bash commands and syntax
2. Include proper quoting and escaping
3. Add comments for complex operations
4. Ensure the command is safe and follows best practices
5. Handle multiple targets and options appropriately
6. Include error handling where necessary

{examples_context}

Natural Language Input: {text}

Your response should be ONLY the bash command, nothing else. Do not include any explanations or additional text.

Bash Command:"""
            
            # Get response from model
            response = self.model(
                prompt,
                max_tokens=256,
                temperature=0.1,
                stop=["Natural Language Input:", "\n\n"]
            )
            
            command = response["choices"][0]["text"].strip()
            logger.info(f"[ModelManager] Generated command: {command}")
            
            return command
            
        except Exception as e:
            logger.error(f"[ModelManager] Error in process_input: {str(e)}", exc_info=True)
            raise 