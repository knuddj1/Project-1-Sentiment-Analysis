def load(path):
    import pandas as pd
    import zipfile

    label_converter = {0: -1, 2: 0, 4: 1}

    data = list()

    archive = zipfile.ZipFile(path, 'r')

    for csvfile in archive.namelist():

        df = pd.read_csv(
            archive.open(csvfile),
            header=None,
            names=('target', 'ids', 'date', 'flag', 'user', 'text'),
            encoding="ISO-8859-1",
            error_bad_lines=False
        )

        print()

        for _, row in df.iterrows():
            data.append({"input": row['text'], "label": label_converter[row['target']]})

    return data
