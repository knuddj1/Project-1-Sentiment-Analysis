"""
Settings for the construction of
"""

# The name of the folder the final dataset will be saved in
DATASET_NAME = ""


# File type to save datasets under
# One of either 'csv' or 'json'
DATASET_FILE_EXTENSION = "csv"


# Save file with information about each dataset
SAVE_STATS = True


# type : int
# Number of samples to retrieve from each dataset
# If NUM_SAMPLES=None then the number of samples is the size of the smallest dataset is used
# Using this may result in unbalanced datasets
NUM_SAMPLES = None


# Whether to shuffle final dataset
SHUFFLE = True


# Number of times to shuffle dataset
# Only used if SHUFFLE=True
NUM_SHUFFLES = 1
