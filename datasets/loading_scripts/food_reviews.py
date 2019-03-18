def load(path):
    import pandas as pd
    import zipfile

    score_converter = {5: 1, 3: 0, 1: -1}

    data = list()

    archive = zipfile.ZipFile(path, 'r')
    df = pd.read_csv(archive.open('Reviews.csv'))

    query = df['Score'].isin(score_converter.keys())
    result = df.loc[query]

    for _, row in result.iterrows():  
        data.append({"input": row['Text'], "label": score_converter[row['Score']]})

    return data
