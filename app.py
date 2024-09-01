# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
from extensions import db
from models import User, Quiz, Question, option

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flash messages

# Configure your database URI here
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quizbuzz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the Flask app
db.init_app(app)

# Create tables if they don't exist
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/take_quiz/<int:quiz_id>', methods=['GET', 'POST'])
def take_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)

    if request.method == 'POST':
        for question in quiz.questions:
            selected_answer = request.form.get(f'question_{question.id}')
            is_correct = selected_answer == question.correct_answer
            user_answer = UserAnswer(
                    user_id=current_user.id,
                    question_id=question.id,
                    selected_answer=selected_answer,
                    is_correct=is_correct
                    )
            db.session.add(user_answer)
            db.session.commit()
            flash('Quiz submitted successfully!', 'success')
            return redirect(url_for('dashboard'))
        return render_template('take_quiz.html', quiz=quiz)

@app.route('/create_quiz', methods=['GET', 'POST'])
def create_quiz():
    if request.method == 'POST':
        # Retrieve quiz title and questions from form data
        quiz_title = request.form.get('quiz_title')
        questions = request.form.getlist('questions')  # Assumes form inputs have this structure

        # Create a new Quiz instance
        quiz = Quiz(title=quiz_title)
        db.session.add(quiz)
        db.session.commit()  # Commit to get quiz.id for foreign key references

        for question_text in questions:
            question = Question(text=question_text, quiz_id=quiz.id)
            db.session.add(question)
            db.session.commit()  # Commit to get question.id for foreign key references
            
            # Assuming you have form inputs for options associated with each question
            options = request.form.getlist(f'options_for_{question.id}')  # Adjust key name as necessary
            correct_option_index = int(request.form.get(f'correct_option_for_{question.id}'))  # Index of the correct option
            
            for index, option_text in enumerate(options):
                is_correct = (index == correct_option_index)
                option = Option(text=option_text, is_correct=is_correct, question_id=question.id)
                db.session.add(option)
            
            db.session.commit()  # Commit all options for the current question

        flash('Quiz created successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('create_quiz.html')

@app.route('/quiz/<int:quiz_id>')
def quiz_detail(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return "Quiz not found", 404
    return render_template('quiz_detail.html', quiz=quiz)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Add user creation logic here
        flash('Registration successful!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html')
@app.route('/logout')
def logout():
    #clear the user session
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
