def load(path):
    import tarfile
    import codecs
    import os
    
    utf8reader = codecs.getreader('utf-8')
    tar = tarfile.open(path, "r:gz")

    data = list()

    for name in tar.getmembers():

        file_path = name.name

        conditions = [
            any(s in file_path for s in ['train','test']),
            any(s in file_path for s in ['pos','neg']),
            'urls' not in file_path,
            file_path.endswith('.txt')
        ]
        
        if all(conditions):
            label = None
            if 'pos' in file_path:
                label = 1
            elif 'neg' in file_path:
                label = -1

            fp = utf8reader(tar.extractfile(name))
            
            data.append({"input": fp.read(), "label": label})
    
    return data
