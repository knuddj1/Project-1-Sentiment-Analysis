import imdb

path = "C:\\Users\\The Baboon\\Downloads\\datasets\\aclImdb_v1.tar.gz"

for r in imdb.load(path)[:5]:
    print(r)
    print()
    print()

