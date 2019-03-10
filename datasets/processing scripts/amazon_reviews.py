def load(path):
    import bz2
    import zipfile 

    label_converter = {'__label__1': -1, '__label__2': 1}

    archive = zipfile.ZipFile(path)
    data = list()

    for fname in archive.namelist():
        bz = bz2.BZ2File(archive.open(fname), "r")
        for line in bz.readlines():
            line = line.decode('utf-8')
            label, txt = line.split(' ', 1)
            data.append({"input": txt, "label": label_converter[label]})
        bz.close()
    
    return data
