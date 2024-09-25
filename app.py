from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Replace the placeholders with your actual NeonDB connection details
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://team_matching_owner:Zf3AKJrwqnc1@ep-purple-unit-a54far0t.us-east-2.aws.neon.tech/team_matching?sslmode=require'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    skills = db.Column(db.String(200), nullable=False)  # Store as a comma-separated string for simplicity
    rate = db.Column(db.Float, nullable=False)

# Define Project Model
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    required_skills = db.Column(db.String(200), nullable=False)  # Store as a comma-separated string for simplicity
    num_of_people_required = db.Column(db.Integer, nullable=False)

# Create the database
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        skills = request.form['skills']
        rate = float(request.form['rate'])
        new_user = User(name=name, skills=skills, rate=rate)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/')
    return render_template('add_user.html')

@app.route('/add_project', methods=['GET', 'POST'])
def add_project():
    if request.method == 'POST':
        name = request.form['name']
        required_skills = request.form['required_skills']
        num_of_people_required = int(request.form['num_of_people_required'])
        new_project = Project(name=name, required_skills=required_skills, num_of_people_required=num_of_people_required)
        db.session.add(new_project)
        db.session.commit()
        return redirect('/')
    return render_template('add_project.html')

@app.route('/add_user.html')
def add_user_template():
    return '''
    <form method="POST">
        Name: <input type="text" name="name" required><br>
        Skills (comma-separated): <input type="text" name="skills" required><br>
        Rate: <input type="number" name="rate" step="0.01" required><br>
        <input type="submit" value="Add User">
    </form>
    '''

@app.route('/add_project.html')
def add_project_template():
    return '''
    <form method="POST">
        Name: <input type="text" name="name" required><br>
        Required Skills (comma-separated): <input type="text" name="required_skills" required><br>
        Number of People Required: <input type="number" name="num_of_people_required" required><br>
        <input type="submit" value="Add Project">
    </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)
