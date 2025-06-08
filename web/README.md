# Command Line Helper Web Interface

A modern web interface for the Command Line Helper tool that translates natural language into bash commands.

## Features

- Convert natural language to bash commands
- Save and reuse command templates
- View command history with search functionality
- Provide feedback on generated commands
- Clean, modern user interface
- Local SQLite database for storing commands and templates

## Setup

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the Flask application:
   ```bash
   python app.py
   ```

3. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## Usage

1. **Converting Commands**
   - Type your command in natural language in the input box
   - Click "Convert" to generate the bash command
   - The generated command will appear in the output section

2. **Using Templates**
   - Click "New Template" to create a command template
   - Give your template a name and save the command
   - Click the play button on any template to use it

3. **Command History**
   - View your past commands in the history section
   - Search through your history using the search box
   - Provide feedback on commands using the thumbs up/down buttons

## Database

The application uses SQLite to store:
- Command history
- Command templates
- User feedback

The database file is automatically created when you first run the application.

## Development

The web interface is built using:
- Flask for the backend
- SQLite for the database
- Tailwind CSS for styling
- Vanilla JavaScript for interactivity 