# importing libraries for flask, database, model
import os
from datetime import datetime, timedelta
from pickle import load

import pytz
from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from textblob import TextBlob

from model_nltk import predict_sentiment

app = Flask(__name__, template_folder="templates")

# "sqlite:///data.sqlite"
# /// for relative path
# //// for absolute path
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///data.sqlite"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "thisissecret")
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=12)

db = SQLAlchemy(app)

# since the app is hosted on heroku so this line of code is to change the timezone
IST = pytz.timezone("Asia/Kolkata")


# I have creted two models but I am using model_nltk because of its high accurcy and less execution time.
# textblob is used for ploting the subjectivity and polarity curve for the input data

# class for creating and initialising database
class New_Data(db.Model):

    Id = db.Column(db.Integer, primary_key=True)
    Text = db.Column(db.Text)
    Sentiment = db.Column(db.String(20))
    # .now(IST).strftime('%Y-%m-%d %H:%M:%S'))
    Date = db.Column(
        db.DateTime, default=datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S")
    )

    def __init__(self, Text, Sentiment):
        self.Text = Text
        self.Sentiment = Sentiment


# loading classifier
with open("my_classifier.pickle", "rb") as f:
    classifier = load(f)


def allowed_file(filename):
    """Checking file extension i.e. text file or not"""
    return "." in filename and filename.split(".")[1] == "txt"


# route for home page
@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        sentence = str(request.form.get("twt"))

        sentiment = predict_sentiment(sentence, classifier)

        # adding emoji to the sentiment
        if sentiment == "Positive":
            sentiment += " \U0001f600"

        elif sentiment == "Negative":
            sentiment += " \U0001F641"

        else:
            pass

        # creating an instance of the data table for the database and commiting the changes
        usr_data = New_Data(sentence, sentiment.split()[0])
        db.session.add(usr_data)
        db.session.commit()

        text = 'You have entered "' + sentence + '"'
        return render_template(
            "index.html", text=text, sentiment="Sentiment: " + sentiment
        )

    return render_template("index.html")


# route for about page
@app.route("/about")
def about():
    return render_template("about.html")


# route for members page
@app.route("/member")
def contact():
    return render_template("members.html")


# route for fastapi
# setting default value for the api
@app.route("/fast-api/", defaults={"sentence": "Great"})
@app.route("/fast-api/<sentence>")
def fast_api(sentence):
    sentiment = predict_sentiment(sentence, classifier)

    return jsonify({"sentence": sentence, "sentiment": sentiment})


# setting post method for the api
@app.route("/fastapi", methods=["POST"])
def fastapi():
    text = request.form["text"]
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0:
        sentiment = "Positive"
    elif polarity < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    return jsonify({"sentiment": sentiment})


# route for uploading and saving temperary file
@app.route("/upload")
def upload():
    mssg = request.args.get("msg")
    # if the uploaded file is not a text file
    if mssg == "ntxt":
        mssg = "Kindly Upload a text file"

    # if the uploaded textfile is not readable
    elif mssg == "incrt":
        mssg = "Upload file of correct format"

    else:
        mssg = None

    return render_template("upload.html", mssg=mssg)


# route for displaying the curves for the given text file
@app.route("/canvas", methods=["POST", "GET"])
def canvas():
    if request.method == "POST":
        pos = 0
        neg = 0
        subject = []
        polar = []
        file = request.files["file"]

        # if the file is correct and readable then save it
        if allowed_file(file.filename):
            file.save(file.filename)

            try:
                # open file, read the content perform the analysis and then return the template with the values
                with open(file.filename) as fl:
                    content = fl.read().split("\n")
                    for line in content:
                        # t = fl.readline()
                        a = TextBlob(line).sentiment.polarity * 100
                        polar.append(a)
                        subject.append(TextBlob(line).sentiment.subjectivity * 100)
                        if a > 0:
                            pos += 1
                        else:
                            neg += 1
                os.remove(file.filename)
                return render_template(
                    "canvas.html", value1=subject, value2=polar, pos=pos, neg=neg
                )

            except:
                os.remove(file.filename)
                return redirect(url_for("upload", msg="incrt"))

        return redirect(url_for("upload", msg="ntxt"))

    # these readings are for mannual or you can say get request when there is no file upload.
    # these readings are not random value, the values are valid for the review.txt file present in static/temp
    from values import polar, subject

    pos = 246
    neg = 254

    return render_template(
        "canvas.html", value1=subject, value2=polar, pos=pos, neg=neg
    )


# route for admin login panel
@app.route("/login")
def login():
    error = request.args.get("er")
    if error == "incrt":
        error = "Invalid Credentials"

    elif error == "lnf":
        error = "You need to login first"

    else:
        error = None

    return render_template("login.html", error=error)


# this route is for showing the data of the database with in html template
@app.route("/show", methods=["GET", "POST"])
def show():
    if request.method == "POST":
        if request.form.get("username") == os.environ.get(
            "sausr", "gparas"
        ) and request.form.get("pwd") == os.environ.get("sapwd", "gparas"):
            session["sausr"] = request.form.get("username")
            session["sapwd"] = request.form.get("pwd")
            table = New_Data.query.all()[::-1]
            return render_template("show.html", table=table)

        else:
            return redirect(url_for("login", er="incrt"))

    try:
        if "sausr" in session:
            table = New_Data.query.all()[::-1]
            return render_template("show.html", table=table)

    except:
        pass

    return redirect(url_for("login", er="lnf"))


@app.route("/test")
def test():
    return render_template("index.html", script=True)


@app.errorhandler(404)
def error404(error):
    return render_template("error404.html"), 404


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
