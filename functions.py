import os
import zipfile

def unzip(zip_file:str, output_dir:str):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(output_dir)

# Make directory if it doesn't exist
def dir_exists(directory:str):
    if os.path.exists(directory) is False:
        return os.makedirs(directory)
    return None

# Convert each value in combined_list to an integer if possible
def num_convert(num_string:str):
    try:
        return int(num_string)
    except ValueError:
        return None
