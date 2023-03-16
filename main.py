import pathlib
import utils.cazy_functions as func
import utils.cazy_parse as parse
import utils.database_trim as trim

# Working Directories
cwd = pathlib.Path.cwd()
downloads_dir = cwd.joinpath('downloads')
results_dir = cwd.joinpath('results')

def main():
    # Set up directory structure
    parse.dir_setup()
    print('dir_setup() done')

    # Download all CBM pages
    parse.wget_CAZy()
    print('wget_cazy() done')

    # Convert/combine html tables into an excel file
    parse.html_to_excel()
    print('html_to_excel() done')

    # Download cazy_data.zip
    db_zip = trim.wget_database()
    print('wget_database() done')

    # Extract cazy_data.zip
    func.unzip(zip_file=db_zip, output_dir=downloads_dir)
    print('unzip() done')

    # Search for cazy_data.txt in the downloads folder
    for file in downloads_dir.glob('**/cazy_data.txt'):
        if pathlib.Path.is_file(file):
        # Read the database file and extract the lines relevant to CBMs
            trim.db_trim(file)
            break
    print('db_trim() done')

    # Delete any .tmp files created by python3-wget
    func.clean_up(cwd)
    print('clean_up() done\n\nCAZy Database Parser complete!')

if __name__ == '__main__':
    main()
