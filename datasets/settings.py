"""
TODO
"""

# The name of the folder the final dataset will be saved in
DATASET_NAME = ""


# Path to the datasets configuration file
DATA_CONFIG_PATH = ""


# File type to save datasets under
# One of either 'csv' or 'json'
DATASET_FILE_EXTENSION = "csv"


# Method in which final dataset will be established
#    ->  when UNIFORM=FALSE all records from each dataset are combined
#
#    ->  when UNIFORM=TRUE each dataset has X amount of samples retrieved from it
UNIFORM = False


# Number of samples to retrieve from each dataset
# If NUM_SAMPLES=None then the number of samples is the size of the smallest dataset is used
# Only used if UNIFORM=True.
NUM_SAMPLES = None


# Whether to shuffle final dataset
SHUFFLE = True


# Number of times to shuffle dataset
# Only used if SHUFFLE=True
NUM_SHUFFLES = 1
