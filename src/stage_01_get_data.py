import os
import logging
from tqdm import tqdm
import argparse
import urllib.request as req
from src.utils.common import read_yaml, create_directories, unzip_file
from src.utils.data_mgmt import validate_image
STAGE = "GET_DATA" ## stage name


logging.basicConfig(filename=os.path.join("Logs", 'running_logs.log'),
                    level=logging.INFO,
                    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
                    filemode="a+")

def main(config_path):
    print(f"second in {STAGE}")
    logging.info(f"reading config file")
    config = read_yaml(config_path)
    source_url = config['data']['source_url']
    local_dir = config['data']['local_dir']
    data_file = config['data']['data_file']
    unzip_data_dir = config['data']['unzip_data_dir']
    parent_data_dir = config['data']['parent_data_dir']
    bad_data_folder = config['data']['bad_data_folder']
    bad_data_path = os.path.join(local_dir, bad_data_folder)
    
    # create directory for data if not present
    create_directories([local_dir])
    zip_data_full_path = os.path.join(local_dir, data_file)
    #check if data File present or not if not download it
    path_to_data = os.path.join(local_dir,unzip_data_dir,parent_data_dir)
    try:
        if os.path.isdir(path_to_data):
            for dir in os.listdir(path_to_data):
                path_to_inner_dir = os.path.join(path_to_data, dir)
                if os.path.isdir(path_to_inner_dir):
                    logging.info(f'{path_to_inner_dir} is already available')
                
        else:
            if not os.path.isfile(zip_data_full_path):
                logging.info(f"{zip_data_full_path} not available")
                logging.info('Downloading started ***********')
                print('Downloading started ***********')
                filename, header = req.urlretrieve(source_url,zip_data_full_path)
                logging.info(f"{filename} downloaded")
                unzip_destination = os.path.join(local_dir, unzip_data_dir)
                logging.info(f"Unzipping {zip_data_full_path} to {unzip_data_dir}")
                unzip_file(zip_data_full_path, unzip_destination)
                logging.info('*********Unzipping done*******')
            else:
                logging.info(f"{zip_data_full_path} already available")
                #unzip ops
                try:
                    unzip_destination = os.path.join(local_dir, unzip_data_dir)
                    logging.info(f"Unzipping {zip_data_full_path} to {unzip_data_dir}")
                    unzip_file(zip_data_full_path, unzip_destination)
                    logging.info('*********Unzipping done*******')
                except Exception as e:
                    print(e)
                    logging.exception(e)
                    raise e
    
    except Exception as e:
        print(e)
        logging.exception(e)
        raise e
    
    # image data validation
    validate_image(path_to_data, bad_data_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config","--c", default="config/config.yaml")
    parsede_args = parser.parse_args()
    try:
        logging.info("\n************************************")
        logging.info(f"STARTING STAGE: {STAGE}")
        main(config_path=parsede_args.config)
        logging.info(f"STAGE: {STAGE} COMPLETED SUCCESSFULLY")
    except Exception as e:
        logging.exception(e)
        raise e