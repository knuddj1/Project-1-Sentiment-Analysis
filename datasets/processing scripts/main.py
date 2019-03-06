import sentiment140

path = "C:/Users/The Baboon/Downloads/datasets/trainingandtestdata.zip"


for s in sentiment140.load(path)[:5]:
    print(s)