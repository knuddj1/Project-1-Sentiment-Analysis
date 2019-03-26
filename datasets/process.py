from . import loader
from . import stats
from . import construct
from .settings import *
from . import save
from .data_configs import CONFIGS
from shutil import rmtree

def run():
    save_func = save.get_save_func(DATASET_FILE_EXTENSION)

    # Load individual datasests
    datasets = loader.load_data(CONFIGS, save_func)
    
    # Construct new dataset
    training_set, test_set = construct.get_subset(datasets, NUM_SAMPLES, TEST_SET_SIZE)


    save.save_multiple(training_set, DATASET_NAME + "_training_set", save_func)
    save.save_multiple(test_set, DATASET_NAME + "_test_set", save_func)

    # Save statistics of each individual dataset
    datasets_stats = stats.generate_stats(training_set, SAVE_STATS, save_func)

    # Remove formatted datasets if DELETE_CACHED=True as they are no longer needed
    if DELETE_CACHED: rmtree("datasets/formatted_datasets")