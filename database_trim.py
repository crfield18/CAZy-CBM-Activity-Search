import os
from pathlib import Path
import zipfile
import wget
from cazy_parse import dir_exists

# Current working directory
home_dir = os.getcwd()
database_dir = f'{home_dir}/CAZy_database'

# Download the cazy_data file to the CAZy_database directory
def wget_database():
    # Make CAZy_database directory if it does not exist
    dir_exists(database_dir)
    # Download cazy_data.zip to CAZy_database if it does not exist
    database_zip = Path(f'{database_dir}/cazy_data.zip')
    if database_zip.is_file():
        pass
    else:
        wget.download(url='http://www.cazy.org/IMG/cazy_data/cazy_data.zip', out=database_dir)
    # Return path to cazy_data.zip
    return f'{database_dir}/cazy_data.zip'

# Unzip a zipped file
def unzip(zip_file:str, output_dir:str):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(output_dir)

# Read the database file and extract the lines relevant to CBMs
def db_trim(database_file:str):
    output_file = open('cazy_data_cbm_only.txt', 'w', encoding='utf-8')
    with open(database_file, 'r', encoding='utf-8') as file:
        # Write each line containing 'CBM' in the left column to the trimmed database file
        for line in file:
            if 'CBM' not in line.split()[0]:
                pass
            else:
                output_file.writelines(line)

def main():
    db_zip = wget_database()
    unzip(zip_file=db_zip, output_dir=database_dir)
    db_trim(f'{database_dir}/ssd/biblio/cazy_data/cazy_data.txt')

if __name__ == '__main__':
    main()
