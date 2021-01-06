<img style="width:5%; height:5%;" src="https://github.com/g-paras/sentiment-analysis-api/blob/master/static/img/icon.png?raw=true">

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

<ul>
    <li>static folder contains all the images used</li>
    <li>templates folder has all html templates</li>
    <li>requirement.txt contains the python dependencies used in this project</li>
    <li>nltk.txt has the files which need to be downloaded for processing the input text</li>
    <li>Procfile is configuration file for Heroku server</li>
    <li>app.py is the flask application file</li>
    <li>model_nltk.py contains the source code for the Naive Bayes classifer which has been used in the production</li>
    <li>model_keras.py is another source code for model usign keras but we haven't used this in production because of its accuracy.</li>
</ul>

## Updates

- Implemented some async js to make predictions faster and avoid reloading using jquery

- The above mentioned feature is in beta version, you can check it our [here](https://sentiment-analysis-web-app.herokuapp.com/test)

- Added session object to remember admin credentials to a small time

- Now you can upload a test file of reviews and then it will show you the graph of the predicted sentiments. Check it out [here](https://sentiment-analysis-web-app.herokuapp.com/upload)

- Implemented custom scroll bar, now it looks kind of cool and now you can use it as a pwa, go to 'add to screen' and then it will be a stand alone app
