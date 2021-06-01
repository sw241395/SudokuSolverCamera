# Class to handle all the functions relating too the temp folder

import os
import shutil
import cv2

# Static variables
temp_folder_path = "./TEMP/"
full_image_file_name = temp_folder_path + 'inital_saved_img.jpg'


# Create the temp folder
def create_temp_folder():
    if not os.path.exists(temp_folder_path):
        os.mkdir("TEMP")


# Remove the temp folder
def remove_temp_folder():
    if os.path.exists(temp_folder_path):
        shutil.rmtree(temp_folder_path)


# Save image then reimport
def save_image(image, image_name):
    file_path = temp_folder_path + image_name
    cv2.imwrite(filename=file_path, img=image)
    return cv2.imread(file_path)

