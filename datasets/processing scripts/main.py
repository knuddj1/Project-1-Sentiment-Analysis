import GOP_debate

path = "C:/Users/The Baboon/Downloads/datasets/first-gop-debate-twitter-sentiment.zip"

# GOP_debate.load(path)

for s in GOP_debate.load(path)[:5]:
    print(s)