from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import sys
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add the parent directory to Python path to import the model manager
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.models.model_manager import ModelManager

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5000"}})

# Configure SQLite database
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'commands.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Models
class Command(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    input_text = db.Column(db.String(500), nullable=False)
    output_command = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    feedback = db.Column(db.Boolean, nullable=True)
    is_template = db.Column(db.Boolean, default=False)

class Template(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    command = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Initialize model manager
logger.info("Initializing model manager...")
model_manager = ModelManager()
logger.info("Loading models...")
model_manager.load_models()  # Load the models at startup
logger.info("Models loaded successfully!")

# Create database tables
with app.app_context():
    logger.info("Creating database tables...")
    db.create_all()
    logger.info("Database tables created successfully!")

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/convert', methods=['POST'])
def convert():
    data = request.json
    input_text = data.get('text')
    
    logger.info(f"Received input text: {input_text}")
    
    if not input_text:
        logger.error("No input text provided")
        return jsonify({'error': 'No input text provided'}), 400
    
    try:
        # Process the input using our model manager
        logger.info("Processing input with model manager")
        command = model_manager.process_input(input_text)
        logger.info(f"Generated command: {command}")
        
        # Save to database
        new_command = Command(
            input_text=input_text,
            output_command=command
        )
        db.session.add(new_command)
        db.session.commit()
        logger.info(f"Saved command to database with ID: {new_command.id}")
        
        return jsonify({
            'command': command,
            'id': new_command.id
        })
    except Exception as e:
        logger.error(f"Error processing command: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    commands = Command.query.order_by(Command.timestamp.desc()).all()
    return jsonify([{
        'id': cmd.id,
        'input': cmd.input_text,
        'output': cmd.output_command,
        'timestamp': cmd.timestamp.isoformat(),
        'feedback': cmd.feedback,
        'is_template': cmd.is_template
    } for cmd in commands])

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    data = request.json
    command_id = data.get('id')
    feedback = data.get('feedback')
    
    if not command_id or feedback is None:
        return jsonify({'error': 'Missing command ID or feedback'}), 400
    
    command = Command.query.get(command_id)
    if not command:
        return jsonify({'error': 'Command not found'}), 404
    
    command.feedback = feedback
    db.session.commit()
    
    return jsonify({'success': True})

@app.route('/api/templates', methods=['GET'])
def get_templates():
    templates = Template.query.order_by(Template.created_at.desc()).all()
    return jsonify([{
        'id': t.id,
        'name': t.name,
        'command': t.command,
        'created_at': t.created_at.isoformat()
    } for t in templates])

@app.route('/api/templates', methods=['POST'])
def create_template():
    data = request.json
    name = data.get('name')
    command = data.get('command')
    
    if not name or not command:
        return jsonify({'error': 'Missing name or command'}), 400
    
    template = Template(name=name, command=command)
    db.session.add(template)
    db.session.commit()
    
    return jsonify({
        'id': template.id,
        'name': template.name,
        'command': template.command,
        'created_at': template.created_at.isoformat()
    })

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True) 