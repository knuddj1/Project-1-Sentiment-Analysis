CONFIGS = {

    "Amazon_Reviews": {
        "use": True,
        "dataset_path": None,
        "dataset_filename": "amazonreviews.zip",
        "loading_script": "amazon_reviews.py",
        "other_params": None

    },


    "Food_Reviews": {
        "use": True,
        "dataset_path": None,
        "dataset_filename": "amazon-fine-food-reviews.zip",
        "loading_script": "food_reviews.py",
        "other_params": None

    },


    "Twitter_GOP_Debate": {
        "use": True,
        "dataset_path": None,
        "dataset_filename": "first-gop-debate-twitter-sentiment.zip",
        "loading_script": "GOP_debate.py",
        "other_params": {
            "confidence_min": 1.0
        }
    },


    "IMDB": {
        "use": True,
        "dataset_path": None,
        "dataset_filename": "aclImdb_v1.tar.gz",
        "loading_script": "imdb.py",
        "other_params": None

    },


    "Sentiment140": {
        "use": True,
        "dataset_path": None,
        "dataset_filename": "trainingandtestdata.zip",
        "loading_script": "sentiment140.py",
        "other_params": None

    },


    "Twitter_Airline": {
        "use": True,
        "dataset_path": None,
        "dataset_filename": "twitter-airline-sentiment.zip",
        "loading_script": "twitter_airline.py",
        "other_params": {
            "confidence_min": 1.0
        }
    }

}
