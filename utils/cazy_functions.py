import pathlib
import zipfile

# Unzip zipped file
def unzip(zip_file:pathlib.PosixPath, output_dir:pathlib.PosixPath):
    with zipfile.ZipFile(str(zip_file), 'r') as zip_ref:
        zip_ref.extractall(str(output_dir))

# Make directory if it doesn't exist
def dir_exists(directory:pathlib.PosixPath):
    if pathlib.Path.is_dir(directory) is False:
        return pathlib.Path.mkdir(directory)
    return None

# Convert each value in combined_list to an integer if possible
def num_convert(num_string:str):
    try:
        return int(num_string)
    except ValueError:
        return None

# Delete all temp files created by wget
def clean_up(cwd:pathlib.PosixPath):
    for file in cwd.glob('**/*.tmp'):
        pathlib.Path.unlink(file)
