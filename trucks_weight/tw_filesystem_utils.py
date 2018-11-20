# Client that requests ip camera for image


import numpy as np
import datetime
import os
import time
import logging

from config import CONFIG

logger = logging.getLogger('TWFilesystemUtils')
logger.setLevel(CONFIG.FILESYSTEM_UTILS_LOGGER_LEVEL)

def generate_image_path(recog_str):
    path = CONFIG.images_root_folder

    now = datetime.datetime.now()

    if recog_str == "":
        recog_str = "No_Plate"

    # filename = 'GTT091_15_07_17_733178.png'
    filename = recog_str + '_' + \
               str(now.time()).replace('.', '_').replace(':', '_') + \
               '.jpg'

    path = os.path.join(path,
                        str(now.year),
                        str(now.month),
                        str(now.day),
                        filename)

    return path

def copy_image_with_recog_in_name(src_img_path, recog_str):

    if not os.path.isfile(src_img_path):
        logger.warning("copy_image_with_recog_in_name: src_img_path dosen't exist: " + src_img_path)
        return

    dst_path = generate_image_path(recog_str)
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)

    command = "cp %s %s" % (src_img_path, dst_path)

    ret = os.system(command)

    if ret != 0:
        logger.warning("Failed to perform command '%s'" % command)



def find_last_directory_in(root_dir):
    if not os.path.isdir(root_dir):
        logger.warning("find_last_directory_in: root dir dosen't exist: " + root_dir)
        return None

    create_time = 0
    last_created_dir = ""
    for file_or_dir in os.listdir(root_dir):
        path = os.path.join(root_dir, file_or_dir)
        if(os.path.isdir(path)):
            dir_create_time = os.path.getctime(path)
            if dir_create_time > create_time:
                last_created_dir = path
                create_time = dir_create_time

    return last_created_dir


def find_new_files(dir_to_search_in: str, create_time: float):
    found_files = []
    for file in os.listdir(dir_to_search_in):
        file_path = os.path.join(dir_to_search_in, file)
        file_create_time = os.path.getctime(file_path)
        if file_create_time > create_time:
            found_files.append(file_path)

    return found_files


def find_files_added_in_last_5_sec() -> []:
    #find last month directory
    last_month_dir = find_last_directory_in(CONFIG.SRC_IMAGES_ROOT_FOLDER)
    if last_month_dir is None:
        return []

    last_day_dir = find_last_directory_in(last_month_dir)
    if last_month_dir is None:
        return []

    last_files = find_new_files(last_day_dir, time.time()-5)
    return last_files