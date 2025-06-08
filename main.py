import typer
from rich.console import Console
from rich.prompt import Prompt
from src.models.model_manager import ModelManager
import json
from pathlib import Path
from datetime import datetime

app = typer.Typer()
console = Console()

# Initialize history file
HISTORY_FILE = Path("command_history.json")
if not HISTORY_FILE.exists():
    HISTORY_FILE.write_text("[]")

def save_to_history(input_text: str, output_command: str, debug_info: dict = None):
    """Save command history to JSON file."""
    history = json.loads(HISTORY_FILE.read_text())
    history.append({
        "timestamp": datetime.now().isoformat(),
        "input": input_text,
        "output": output_command,
        "debug_info": debug_info
    })
    HISTORY_FILE.write_text(json.dumps(history, indent=2))

@app.command()
def convert(
    text: str = typer.Argument(None, help="Natural language command to convert"),
    interactive: bool = typer.Option(False, "--interactive", "-i", help="Run in interactive mode"),
    debug: bool = typer.Option(False, "--debug", "-d", help="Show debug information")
):
    """Convert natural language to bash commands using two LLMs."""
    try:
        model_manager = ModelManager()
        console.print("[bold green]Loading models...[/bold green]")
        model_manager.load_models()
        console.print("[bold green]Models loaded successfully![/bold green]")
        
        if interactive:
            while True:
                text = Prompt.ask("\nEnter your command (or 'exit' to quit)")
                if text.lower() == 'exit':
                    break
                    
                console.print("\n[bold blue]Processing...[/bold blue]")
                if debug:
                    components = model_manager._extract_command_components(text)
                    console.print("\n[bold yellow]Language Model Output:[/bold yellow]")
                    console.print(json.dumps(components, indent=2))
                    command = model_manager._generate_bash_command(components)
                else:
                    command = model_manager.process_input(text)
                console.print(f"\n[bold green]Generated command:[/bold green]\n{command}")
                save_to_history(text, command, components if debug else None)
        else:
            if not text:
                console.print("[bold red]Error:[/bold red] Please provide a command or use --interactive mode")
                raise typer.Exit(1)
                
            console.print("[bold blue]Processing...[/bold blue]")
            if debug:
                components = model_manager._extract_command_components(text)
                console.print("\n[bold yellow]Language Model Output:[/bold yellow]")
                console.print(json.dumps(components, indent=2))
                command = model_manager._generate_bash_command(components)
            else:
                command = model_manager.process_input(text)
            console.print(f"\n[bold green]Generated command:[/bold green]\n{command}")
            save_to_history(text, command, components if debug else None)
            
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        raise typer.Exit(1)

@app.command()
def history():
    """Show command history."""
    try:
        history = json.loads(HISTORY_FILE.read_text())
        if not history:
            console.print("[yellow]No command history found.[/yellow]")
            return
            
        for entry in history:
            console.print(f"\n[bold blue]Time:[/bold blue] {entry['timestamp']}")
            console.print(f"[bold green]Input:[/bold green] {entry['input']}")
            console.print(f"[bold yellow]Output:[/bold yellow] {entry['output']}")
            if entry.get('debug_info'):
                console.print("[bold magenta]Debug Info:[/bold magenta]")
                console.print(json.dumps(entry['debug_info'], indent=2))
            console.print("-" * 50)
    except Exception as e:
        console.print(f"[bold red]Error reading history:[/bold red] {str(e)}")

if __name__ == "__main__":
    app() 