def load(path, confidence_min=0.0):
    import pandas as pd
    import zipfile

    label_converter = {"Negative": -1, "Neutral": 0,"Positive": 1}

    data = list()

    archive = zipfile.ZipFile(path, 'r')
    df = pd.read_csv(archive.open('Sentiment.csv'))

    query = df['sentiment_confidence'] >= confidence_min
    result = df.loc[query]
    
    for _, row in result.iterrows():  
        data.append({"input": row['text'], "label": label_converter[row['sentiment']]})

    return data
