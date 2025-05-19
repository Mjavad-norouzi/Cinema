import os

import environ
from pathlib import Path

# BASE_DIR = environ.Path(__file__) - 2
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
env_path = os.path.join(BASE_DIR, '.env')
env.read_env(env_path)
