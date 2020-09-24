from flask import Flask, render_template, request, jsonify
from model_nltk import predict_sentiment
from pickle import load
from flask_sqlalchemy import SQLAlchemy
import os
from textblob import TextBlob

app = Flask(__name__, template_folder='templates')

# "sqlite:///data.sqlite"
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
def home():
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

    return jsonify({'sentence': sentence, 'sentiment': sentiment})


@app.route('/upload')
def upload():
    return render_template("upload.html")


@app.route('/canvas')
def canvas():
    subject = []
    polar = []
    pos = 0
    neg = 0
    with open('review.txt') as file:
        for i in file.readlines():
            a = TextBlob(i).sentiment.polarity*100
            subject.append(TextBlob(i).sentiment.subjectivity*100)
            polar.append(a)
            if a > 0: pos += 1
            else: neg += 1
    return render_template("canvas.html", value1=subject, value2=polar, pos=pos, neg=neg)


@app.errorhandler(404)
def error404(error):
    return render_template("error404.html"), 404


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
