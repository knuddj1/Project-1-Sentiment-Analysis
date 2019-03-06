import twitter_airline

path = "C:/Users/The Baboon/Downloads/datasets/twitter-airline-sentiment.zip"

for s in twitter_airline.load(path)[:5]:
    print(s)