import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent


# utility function
def to_bool(key, true_value="true", default_value="false"):
    return os.environ.get(key, default_value).lower() == true_value


def to_list(key, default=None, sep=","):
    return os.environ.get(key, default).split(sep)
