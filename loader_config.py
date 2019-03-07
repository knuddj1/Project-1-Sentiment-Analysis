'''
What dataset will be saved under
'''
DATASET_NAME = ""

'''
File type to save datasets under.
Use one of:
    -> csv
    -> json
    -> txt
'''
DATASET_FILE_EXTENSION = "csv"


'''
Method in which final dataset will be established
Use one of:
    
    -> concatenate - all records from each dataset are combined
    
    -> uniform - 
    
    -> min - each dataset has X amount of samples retrieved from it,
             where X is the the number of samples in the dataset with
             the least records.
'''
FINAL_SET_TYPE = "concatenate"
