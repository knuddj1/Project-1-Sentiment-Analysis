from . import loader
from . import stats
from . import construct
from .settings import *
from .data_configs import CONFIGS
from shutil import rmtree

def run():
    # Load individual datasests
    datasets = loader.load_data(CONFIGS, DATASET_FILE_EXTENSION)
    
    # Save statistics of each individual dataset
    datasets_stats = stats.generate_stats(datasets, SAVE_STATS)

    # Construct new dataset
    training_set, test_set = construct.construct_new_dataset(datasets, datasets_stats, NUM_SAMPLES, TEST_SET_SIZE)

    if DELETE_CACHED:
        rmtree("datasets/formatted_datasets")