import requests

base_url = "https://sentiment-analysis-web-app.herokuapp.com/fast-api/{}"

pos = 0
neg = 0

# change the filename to the name of your file
# this is just one simple application of sentiment analysis fast-api you could make better use of it 
# like for plotting curves or analysing brand value, etc.

with open('reviews.txt') as file:

    for line in file.readlines():
        request = requests.get(base_url.format(line)).json()
        if request.sentiment == 'Positive':
            pos += 1
        else:
            neg += 1
    total = len(file.readlines)

print(f"Out of {total} reviews, {pos} are Positive and {neg} are Negative reviews")
