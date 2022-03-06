from enum import unique
from venv import create
import mlflow
import argparse
import os
import logging

from src.utils.common import read_yaml, create_directories, unzip_file, get_date_time



STAGE = "MAIN" ## stage name
# root_log_folder, unique_name, log_file = log_path()

create_directories(["logs"])
with open(os.path.join("logs", 'running_logs.log'), "w") as f:
    f.write("")

logging.basicConfig(filename=os.path.join("Logs", 'running_logs.log'),
                    level=logging.INFO,
                    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
                    filemode="a+")

def main():
    with mlflow.start_run() as run:
        mlflow.run(".", "get_data", use_conda=False)


if __name__ == "__main__":

    # logging.info("\n************************************")
    
    try:
        logging.info("\n************************************")
        logging.info(f">>>>>>>>>>{STAGE} STARTED<<<<<<<<<<")
        main()
        logging.info(f">>>>>>>>>>{STAGE} COMPLETED SUCCESSFULLY<<<<<<<<<<")
    except Exception as e:
        logging.exception(e)
        raise e



