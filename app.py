from textblob import TextBlob
from flask import Flask, render_template, request

app = Flask(__name__,template_folder='templates')

@app.route('/', methods = ['POST', 'GET'])
def hello():
	if request.method == 'POST':
		text = request.form.get('twt')
		blob = TextBlob(text).sentiment
		if blob[0]>0:
			sentiment="Positive "
		elif blob[0]<0:
			sentiment="Negative"
		else:
			sentiment="Neutral"
		return render_template('index.html',text=blob,sentiment=sentiment )
	return render_template('index.html')

@app.route('/about')
def about():
	return render_template('about.html')
	
@app.route('/member')
def contact():
	return render_template('members.html')
if __name__ == "__main__":
	app.run()
