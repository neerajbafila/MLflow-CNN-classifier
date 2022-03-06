import os
import logging
import argparse
from pickletools import optimize
import tensorflow as tf
from src.utils.common import create_directories, read_yaml
from src.utils.model_ops import write_model_summary

STAGE = "stage_02_base_model_creation" ## stage name

logging.basicConfig(filename=os.path.join("Logs", 'running_logs.log'),
                    level=logging.INFO, format='[%(asctime)s: %(levelname)s: %(module)s]: %(message)s', filemode='a+')
        

def main(config_path):
    logging.info("reading config file")
    config = read_yaml(config_path)
    params = config["params"]
    logging.info(f"LAYER defining")
    LAYERS =[tf.keras.layers.Input(shape=tuple(params['img_shape'])),
            tf.keras.layers.Conv2D(filters=32, kernel_size=(3,3), activation='relu'),
            tf.keras.layers.MaxPool2D(pool_size=(2,2)),
            tf.keras.layers.Conv2D(filters=32, kernel_size=(3,3), activation='relu'),
            tf.keras.layers.MaxPool2D(pool_size=(2,2)),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(units=8, activation='relu'),
            tf.keras.layers.Dense(units=2, activation='softmax')
    ]
    logging.info(f"LAYER defined")

    classifier = tf.keras.Sequential(LAYERS)
    logging.info(f"base model summary:\n{write_model_summary(classifier)}")
    logging.info(f"base model created")

    classifier.compile(optimizer=tf.keras.optimizers.Adam(params['lr']), 
                        loss=params['loss'], metrics=params['metrics']
                        )
    path_of_model_dir = os.path.join(config['data']['local_dir'], config['data']['model_dir'])
    create_directories([path_of_model_dir])
    path_to_model = os.path.join(path_of_model_dir, config['data']['init_model_file'])
    classifier.save(path_to_model)
    logging.info(f"base model saved to {path_to_model}")
    



if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--config","-c", default="config/config.yaml")
    parsed_args = argparser.parse_args()
    try:
        logging.info("\n************************************")
        logging.info(f"{STAGE} started")
        main(parsed_args.config)
        logging.info(f"{STAGE} completed successfully")
    except Exception as e:
        logging.exception(e)
        raise e
