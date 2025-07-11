from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initialize db

# Since render uses Postgres and may require SSL
if app.config['SQLALCHEMY_DATABASE_URI'].startswith('postgres://'):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace('postgres://', 'postgresql://', 1)

db = SQLAlchemy(app)

class ExamRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_exam = db.Column(db.Float, nullable=False)
    desired_final = db.Column(db.Float, nullable=False)
    required_second = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ExamRequest {self.id}>'

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        first_exam = float(request.form['first_exam'])
        desired_final = float(request.form['desired_final'])
        # clamp inputs to 0-100
        first_exam = max(0.0, min(100.0, first_exam))
        desired_final = max(0.0, min(100.0, desired_final))
        required_second = calculate_required_second(first_exam, desired_final)
        entry = ExamRequest(first_exam=first_exam,
                            desired_final=desired_final,
                            required_second=required_second)
        db.session.add(entry)
        db.session.commit()
        result = required_second
    return render_template('index.html', result=result)


def calculate_required_second(first_exam, desired_final):
    """Calculate the required second exam percentage."""
    return max(0.0, min(100.0, (desired_final - 0.4 * first_exam) / 0.6))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
