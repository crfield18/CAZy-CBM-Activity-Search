import glob, os
import utils.cazy_functions as func
import utils.cazy_parse as parse
import utils.database_trim as trim

# Working Directories
home_dir = os.getcwd()
downloads_dir = f'{home_dir}/downloads'
results_dir = f'{home_dir}/results'

def main():
    # Set up directory structure
    parse.dir_setup()
    # Download all CBM pages
    parse.wget_CAZy()
    # Convert/combine html tables into an excel file
    parse.html_to_excel()
    # Download cazy_data.zip
    db_zip = trim.wget_database()
    # Extract cazy_data.zip
    func.unzip(zip_file=db_zip, output_dir=downloads_dir)
    # Search for cazy_data.txt in the downloads folder
    for file in glob.glob(f'{home_dir}/downloads/**/cazy_data.txt', recursive=True):
        if os.path.isfile(file):
    # Read the database file and extract the lines relevant to CBMs
            trim.db_trim(file)
    print('Done.')

if __name__ == '__main__':
    main()
