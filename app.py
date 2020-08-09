from textblob import TextBlob
from flask import Flask, render_template, request
import sqlite3 as sql
from datetime import datetime

app = Flask(__name__, template_folder='templates')


@app.route('/', methods=['POST', 'GET'])
def hello():
    if request.method == 'POST':
        text = request.form.get('twt')
        blob = TextBlob(text).sentiment
        if blob[0] > 0:
            sentiment = "Positive \U0001f600"
        elif blob[0] < 0:
            sentiment = "Negative \U0001F641"
        else:
            sentiment = "Neutral \U0001F610"

        with sql.connect("text.sqlite") as con:
            cur = con.cursor()
            cur.execute("""INSERT INTO Texts (text, date, sentiment) 
               VALUES (?,?,?)""",(text, datetime.now(), sentiment.split()[0]))
            con.commit()
        return render_template('index.html', text=blob, sentiment=sentiment)
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/member')
def contact():
    return render_template('members.html')


if __name__ == "__main__":
    app.run()
