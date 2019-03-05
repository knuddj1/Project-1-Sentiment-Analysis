import food_reviews


path = "C:/Users/The Baboon/Downloads/datasets/amazon-fine-food-reviews.zip"

for i in  food_reviews.load(path)[:5]:
    print(i)





