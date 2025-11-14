"""
This app contains the Notes API built with Flask and SQLAlchemy.
It provides endpoints for CRUD operations on notes and Prometheus metrics.
"""
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db:5432/notesdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
metrics = PrometheusMetrics(app)
metrics.info("app_info", "Notes API", version="1.0.0")

class Note(db.Model):
    # pylint: disable=R0903
    """Note model for database storage."""
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)

@app.route('/')
def index():
    """Returns a simple message indicating the API is running."""
    return jsonify({"message": "Notes API is running!"})

@app.route('/notes', methods=['GET'])
def get_notes():
    """Retrieves all notes from the database."""
    notes = Note.query.all()
    return jsonify([{"id": n.id, "content": n.content} for n in notes])

@app.route('/notes', methods=['POST'])
def create_note():
    """Creates a new note based on JSON data."""
    data = request.get_json()
    new_note = Note(content=data['content'])
    db.session.add(new_note)
    db.session.commit()
    return jsonify({"id": new_note.id, "content": new_note.content}), 201

@app.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    """Deletes a note by its ID."""
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    return jsonify({"message": "Note deleted"})

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000)
