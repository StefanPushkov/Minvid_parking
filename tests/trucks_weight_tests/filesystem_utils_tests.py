from trucks_weight.tw_filesystem_utils import generate_image_path, copy_image_with_recog_in_name, \
    find_last_directory_in, find_files_added_in_last_5_sec

print(generate_image_path("GTT091"))

print(generate_image_path(""))

print(copy_image_with_recog_in_name("/media/data/server_img/carplates_trucks/26/GTT091.jpg", "GTT091"))

print(find_last_directory_in('/media/data/server_img'))

print(find_files_added_in_last_5_sec())