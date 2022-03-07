from importlib.resources import path
import tensorflow as tf
from src.utils.common import create_directories, read_yaml
import logging
import os
import argparse
STAGE= "Stage04_Model_train" ##stage name

logging.basicConfig(filename=os.path.join("Logs", 'running_logs.log'),
                    level=logging.INFO,
                    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s", filemode="a+")


def main(config_path):
    config = read_yaml(config_path)
    local_dir = config["data"]["local_dir"]
    data_dir = config["data"]["unzip_data_dir"]
    path_to_data = os.path.join(local_dir, data_dir, config["data"]['parent_data_dir'])
    model_dir = config["data"]["model_dir"]
    path_to_model = os.path.join(local_dir, model_dir, config["data"]['init_model_file'])
    params = config['params']

    # reading data
    logging.info(f"reading data from {path_to_data}")
    train_dataset = tf.keras.preprocessing.image_dataset_from_directory(path_to_data,
                    validation_split= params['validation_split'],
                    subset='training',
                    seed = params['seed'],
                    image_size = params['img_shape'][:-1],
                    batch_size = params['batch_size'],
                    )

    val_dataset = tf.keras.preprocessing.image_dataset_from_directory(path_to_data,
                    validation_split = params['validation_split'],
                    subset = "validation",
                    seed = params['seed'],
                    image_size = params['img_shape'][:-1],
                    batch_size = params['batch_size'],
                    )
    
    train_dataset = train_dataset.prefetch(buffer_size=params['buffer_size'])
    val_dataset = val_dataset.prefetch(buffer_size=params['buffer_size'])

    ## load base model

    logging.info(f"loading base model from {path_to_model}")
    classifier = tf.keras.models.load_model(path_to_model)
    logging.info(f"base model{path_to_model} has been loaded")

    logging.info(f"training started")
    classifier.fit(train_dataset, epochs=params['epochs'], validation_data=val_dataset)
    logging.info('training completed')

    ##saving trained model
    path_to_trained_model = os.path.join(local_dir, model_dir, config["data"]['trained_model_file'])
    classifier.save(path_to_trained_model)
    logging.info(f"trained model saved at {path_to_trained_model}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config","-c", default="config/config.yaml")
    parsed_args = parser.parse_args()
    try:
        logging.info("\n************************************")
        logging.info(f"{STAGE} started")
        main(parsed_args.config)
        logging.info(f"{STAGE} completed successfully")
    except Exception as e:
        logging.exception(e)
        raise e

    