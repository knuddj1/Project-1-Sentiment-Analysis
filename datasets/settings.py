"""
Settings for the construction of a custom dataset
"""

# The name of the folder the final dataset will be saved in
DATASET_NAME = "custom"


# File type to save datasets under
# One of either 'csv' or 'json'
DATASET_FILE_EXTENSION = "csv"


# Save file with information about each dataset
SAVE_STATS = False



# Delete all versions of dataset that are saved during creation of custom dataset
DELETE_CACHED = False

# type : int
# Number of samples to retrieve from each dataset
# If NUM_SAMPLES=None then the number of samples is the size of the smallest dataset is used
# If dataset size is less that NUM_SAMPLES then total samples from that dataset are used
# Using this may result in unbalanced datasets
NUM_SAMPLES = None


# type : float
# Number between 0 and 1
# How much of each dataset is used for testing set 
TEST_SET_SIZE = 0.2


# Whether to shuffle final dataset
SHUFFLE = True


# Number of times to shuffle dataset
# Only used if SHUFFLE=True
NUM_SHUFFLES = 1
