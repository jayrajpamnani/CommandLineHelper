#!/bin/bash

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download models
python download_models.py

# Run tests
python test_commands.py

echo "Setup complete! You can now run the tool using:"
echo "python main.py 'your natural language command'"
echo "or"
echo "python main.py --interactive" 