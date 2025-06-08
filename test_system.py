from main import convert
import time

def test_command(nl_command: str):
    print(f"\n{'='*80}")
    print(f"Testing command: {nl_command}")
    print('='*80)
    start_time = time.time()
    convert(nl_command, debug=True)
    end_time = time.time()
    print(f"\nTime taken: {end_time - start_time:.2f} seconds")

def main():
    test_commands = [
        # File operations
        "list all files in the current directory",
        "find all python files in the current directory",
        "show me the last 10 lines of the requirements.txt file",
        
        # System operations
        "show disk usage of the current directory",
        "display all running processes",
        "show free memory and swap space",
        
        # Search operations
        "search for the word 'model' in all python files",
        "find all files modified in the last 24 hours",
        
        # File management
        "create a new directory called test_backup",
        "copy all .txt files to the test_backup directory",
        
        # Complex operations
        "compress all .log files into a single archive",
        "find and delete all temporary files in the current directory"
    ]
    
    for command in test_commands:
        test_command(command)
        time.sleep(1)  # Small delay between commands

if __name__ == "__main__":
    main() 