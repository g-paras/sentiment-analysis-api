from flask import Flask, render_template, request, jsonify
from model_nltk import predict_sentiment
from pickle import load
from flask_sqlalchemy import SQLAlchemy
import os
import click
from flask.cli import with_appcontext
#from textblob import TextBlob

app = Flask(__name__, template_folder='templates')

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')
db = SQLAlchemy(app)


# I have creted two models but I am using model_nltk because of its high accurcy and less execution time.
# textblob was used in the development mode for checking the subjectivity and polarity of the text

class data(db.Model):
	Id = db.Column("Id", db.Integer, primary_key=True)
	Text = db.Column(db.String(100))
	Sentiment = db.Column(db.String(20))

	def __init__(self, Text, Sentiment):
		self.Text = Text
		self.Sentiment = Sentiment

with open('my_classifier.pickle', 'rb') as f:
    classifier = load(f)


@app.route('/', methods=['POST', 'GET'])
def hello():
    if request.method == 'POST':
        sentence = request.form.get('twt')

        sentiment = predict_sentiment(sentence, classifier)

        if sentiment == "Positive":
            sentiment += " \U0001f600"

        elif sentiment == "Negative":
            sentiment += " \U0001F641"

        else:
            pass

        usr_data = data(sentence, sentiment.split()[0])
        db.session.add(usr_data)
        db.session.commit()

        text = "You have entered \"" + sentence + "\""
        return render_template('index.html', text=text, sentiment="Sentiment: " + sentiment)

    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/member')
def contact():
    return render_template('members.html')


@app.route('/fast-api/<sentence>')
def fast_api(sentence):
    sentiment = predict_sentiment(sentence, classifier)
    
    return jsonify({'sentence':sentence, 'sentiment':sentiment})


if __name__ == "__main__":
    db.create_all() 
    #app.run(debug=True)
