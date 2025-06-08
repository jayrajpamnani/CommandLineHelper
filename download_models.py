import os
import requests
from tqdm import tqdm
from pathlib import Path

def download_file(url: str, filename: str):
    """Download a file with progress bar."""
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(filename, 'wb') as file, tqdm(
        desc=filename,
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as pbar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            pbar.update(size)

def main():
    # Create models directory if it doesn't exist
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    # Model URLs (using Hugging Face model files)
    models = {
        "codellama-7b.gguf": "https://huggingface.co/TheBloke/CodeLlama-7B-GGUF/resolve/main/codellama-7b.Q4_K_M.gguf"
    }
    
    for filename, url in models.items():
        filepath = models_dir / filename
        if not filepath.exists():
            print(f"Downloading {filename}...")
            download_file(url, str(filepath))
            print(f"Downloaded {filename}")
        else:
            print(f"{filename} already exists")

if __name__ == "__main__":
    main() 