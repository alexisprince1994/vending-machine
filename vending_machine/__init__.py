import os

HERE = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(HERE, os.pardir)
STATE_FILE_LOCATION = os.path.join(PROJECT_ROOT, "state.json")
