from textblob import TextBlob
from flask import Flask, render_template, request
from twilio.rest import Client
from datetime import datetime

app = Flask(__name__, template_folder='templates')


@app.route('/', methods=['POST', 'GET'])
def hello():
    if request.method == 'POST':
        text = request.form.get('twt')
        account_sid = 'ACab790f15c54deca02be41147ccdc347a'
        auth_token = '532557b12a0020c91a55aa0a19948804'
        client = Client(account_sid, auth_token)
        message = client.messages \
            .create(
                body="Someone searched " + text + " at " + str(datetime.now()),
                from_='+15614751275',
                to='+917906313014'
            )

        blob = TextBlob(text).sentiment
        if blob[0] > 0:
            sentiment = "Positive \U0001f600"
        elif blob[0] < 0:
            sentiment = "Negative \U0001F641"
        else:
            sentiment = "Neutral \U0001F610"
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
