from . import load
from . import stats


def run():
    datasets = load.loader.load_data()
    stats.generate_stats(datasets)

