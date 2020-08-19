from flask import Flask, render_template, request
from model_nltk import remove_noise, word_tokenize
from pickle import load
#from textblob import TextBlob

app = Flask(__name__, template_folder='templates')

# I have creted two models but I am using model_nltk because of its high accurcy and less execution time.
# textblob was used in the development mode for checking the subjectivity and polarity of the text

with open('my_classifier.pickle', 'rb') as f:
    classifier = pickle.load(f)


@app.route('/', methods=['POST', 'GET'])
def hello():
    if request.method == 'POST':
        sentence = request.form.get('twt')
        custom_tokens = remove_noise(word_tokenize(sentence))
        sentiment = classifier.classify(
            dict([token, True] for token in custom_tokens))

        if sentiment == "Positive":
            sentiment += " \U0001f600"

        elif sentiment == "Negative":
            sentiment += " \U0001F641"

        else:
            pass

        text = "You have entered \" " + sentence + "\""
        return render_template('index.html', text=text, sentiment="Sentiment: " + sentiment)

    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/member')
def contact():
    return render_template('members.html')


if __name__ == "__main__":
    app.run(debug=True)
