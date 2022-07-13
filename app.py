from flask import Flask, redirect, request, render_template, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

RESPONSES_KEY = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = "birbsarecool"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.route('/')
def home():
    return render_template('home.html', survey=survey)

@app.route('/start')
def start_survey():
    session[RESPONSES_KEY] = []
    return redirect('questions/0')

@app.route('/questions/<int:id>')
def question(id):
    responses = session.get(RESPONSES_KEY)

    if(len(responses) == len(survey.questions)):
        return render_template('done.html')

    if(len(responses) != id):
        flash("You must answer the questions in order")
        return redirect(f"/questions/{len(responses)}")
        
    question = survey.questions[id]
    
    return render_template('question.html', num_q=id+1, question=question)


@app.route('/answer', methods=["POST"])
def store_answers():
    selection = request.form['answer']
    responses = session[RESPONSES_KEY]
    responses.append(selection)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(survey.questions)):
        return render_template('done.html')
    
    else:
        return redirect(f"/questions/{len(responses)}")
