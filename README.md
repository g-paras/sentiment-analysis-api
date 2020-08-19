<img style="width:10%; height:10%" src="https://github.com/g-paras/sentiment-analysis-api/blob/master/static/icon.png?raw=true">

# Sentiment Analysis 
This is a sentiment analysis web applications, we have used nltk tweet sample for training model and Naive bais classier and deployed using flask api on heroku server.
For training and testing our sentiment analysis model we used Google colaboratory which is an open source platform for machine learning or data science projects.
It helps us training the model fast by using virtual GPU.
For HTML and CSS we use Microsoft VS Code which a great code editor with syntax highlighting, emmit abbreviations and much more.
Python dependencies used:-
1. Keras
2. Flask 1.2.2
3. TextBlob 0.15.3
4. Gunicorn 20.0.4
5. Numpy 1.9.0
6. Regex 2020.6.8
7. NLTK 3.5

Check it out on 
https://sentiment-analysis-web-app.herokuapp.com

It might take few seconds to load please give it a try

## Files and folder classification
#### static folder contains all the images used
#### templates folder has all html templates
#### requirement.txt contains the python dependencies used in this project
#### nltk.txt has the files which need to be downloaded for processing the input text
#### Procfile is configuration file for Heroku server
#### app.py is the flask application file
#### model_nltk.py contains the source code for the Naive Bayes classifer which has been used in the production
#### model_keras is another model but we haven't used this in production because of its accuracy.