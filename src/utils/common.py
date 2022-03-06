import yaml
import os
import logging
from zipfile import ZipFile
from datetime import datetime

"""Used for coomon task like directiory creation, read config 
"""

def read_yaml(path_to_yaml: str) -> dict:
    """Read yaml file
    """
    with open(path_to_yaml) as yaml_file:
        content = yaml.safe_load(yaml_file)
    logging.info(f"yaml file {path_to_yaml} loaded")
    return content


def create_directories(path_to_dir: list):
    """Create directories if not exist
    """
    full_path = ""
    for path in path_to_dir:
        full_path = os.path.join(full_path, path)
    os.makedirs(full_path, exist_ok=True)
    logging.info(f"created directory at: {path}")


def unzip_file(source: str, destination: str):
    """Unzip file
    """
    with ZipFile(source, 'r') as zip_file:
        zip_file.extractall(destination)
    logging.info(f"extracted {source} to {destination}")

def get_date_time():
    """get current date time"""
    now = datetime.now()
    unique_name = now.strftime("%Y_%m_%d")
    return unique_name

