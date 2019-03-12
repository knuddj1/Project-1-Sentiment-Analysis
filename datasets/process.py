from . import load
from . import stats
import time


def run():
    datasets = load.loader.load_data()
    stats.generate_stats(datasets)

