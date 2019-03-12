def load(path, confidence_min=0.0):
    import pandas as pd
    import zipfile

    label_converter = {"negative": -1, "neutral": 0, "positive": 1}

    data = list()

    archive = zipfile.ZipFile(path, 'r')
    df = pd.read_csv(archive.open('Tweets.csv'))

    query = df['airline_sentiment_confidence'] >= confidence_min
    result = df.loc[query]
    
    for _, row in result.iterrows():  
        data.append({"input": row['text'], "label": label_converter[row['airline_sentiment']]})

    return data
