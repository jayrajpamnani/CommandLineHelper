from main import convert
import typer

def test_commands():
    """Test various natural language commands."""
    test_cases = [
        "list all files in the current directory",
        "find all python files in the current directory",
        "create a new directory called test and move all .txt files into it",
        "show me the last 10 lines of the requirements.txt file",
        "count the number of lines in all python files",
        "search for the word 'model' in all files",
        "compress all .log files into a single archive",
        "show disk usage of the current directory",
        "find all files modified in the last 24 hours",
        "create a backup of the src directory"
    ]
    
    for command in test_cases:
        print(f"\n{'='*80}")
        print(f"Testing command: {command}")
        print('='*80)
        convert(command)

if __name__ == "__main__":
    test_commands() 