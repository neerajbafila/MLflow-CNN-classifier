import logging
from PIL import Image
import imghdr
import os
import shutil
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

from src.utils.common import create_directories, read_yaml

def validate_image(image_folder: str, bad_data_path:str):
    
    """it will validate image data and move bad images to bad dataFolder

    Args:
        image_folder (str): Image data Folder path
    """
    logging.info(f"In validate_image function of data_mgmt")
    invalid_image = 0
    print("*******Image validation started*************")
    for dirs in os.listdir(image_folder):
        path_to_inner_dir = os.path.join(image_folder, dirs)
        for fi in os.listdir(path_to_inner_dir):
            image_path = os.path.join(path_to_inner_dir, fi)
            try:
                img = Image.open(image_path)
                img.close()
                if (len(img.getbands()) !=3) or imghdr.what(image_path) not in ['jpeg', 'png']:
                    logging.info(f"{fi} not a valid image")
                    bad_data_path_inner_path = os.path.join(bad_data_path, dirs)
                    if not os.path.isdir(bad_data_path_inner_path):   
                        create_directories([bad_data_path_inner_path])
                    logging.info(f"moving {fi} to {bad_data_path_inner_path}")
                    shutil.move(image_path, bad_data_path_inner_path)
                    
                    
                    invalid_image +=1
            except Exception as e:
                logging.info(f"{fi} not a valid image" )
                logging.exception(e)
                bad_data_path_inner_path = os.path.join(bad_data_path, dirs)
                if not os.path.isdir(bad_data_path_inner_path):
                    create_directories([bad_data_path_inner_path])
                logging.info(f"moving {fi} to {bad_data_path_inner_path}")
                shutil.move(image_path, bad_data_path_inner_path)
                invalid_image +=1
    print(f"*{'*'*30}invalid images are {invalid_image}*{'*'*30}")
    logging.info(f"Total invalid images are {invalid_image}")
    logging.info(f"image validation completed")
