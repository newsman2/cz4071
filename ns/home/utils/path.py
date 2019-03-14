import os
from ns import settings

# ROOT_DIR_PATH = os.path.abspath(os.path.dirname(__file__))

ROOT_DIR_PATH = os.path.abspath(settings.MEDIA_ROOT)
TXT_NETWORK_DIR_PATH = os.path.join(settings.MEDIA_ROOT, 'network_files')
CSV_NETWORK_DIR_PATH = os.path.join(settings.MEDIA_ROOT, 'network_csv_files')
DB_PLOT_DIR_PATH = os.path.join(settings.MEDIA_ROOT, 'plot')

ROOT_DIR_PATH = os.path.abspath(os.path.dirname(__file__))
DB_DIR_PATH = os.path.join(ROOT_DIR_PATH, 'db')

GRAPH_DIR_PATH = os.path.join(ROOT_DIR_PATH, 'graph')
GENERATOR_DIR_PATH = os.path.join(ROOT_DIR_PATH, 'generator')
DATA_DIR_PATH = os.path.join(GRAPH_DIR_PATH, 'data')
RESULTS_DIR_PATH = os.path.join(GRAPH_DIR_PATH, 'results')

DB_NETWORK_DIR_PATH = os.path.join(DB_DIR_PATH, 'networks')
