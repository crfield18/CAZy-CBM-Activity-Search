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
    print('\nwget_cazy() done\n')

    # Convert/combine html tables into an excel file
    parse.html_to_excel()
    print('\nhtml_to_excel() done\n')

    # Download cazy_data.zip
    db_zip = trim.wget_database()
    print('\nwget_database() done\n')

    # Extract cazy_data.zip
    func.unzip(zip_file=db_zip, output_dir=downloads_dir)
    print('\nunzip() done\n')

    # Search for cazy_data.txt in the downloads folder
    for file in downloads_dir.glob('**/cazy_data.txt'):
        if pathlib.Path.is_file(file):
        # Read the database file and extract the lines relevant to CBMs
            trim.db_trim(file)
            break
    print('\ndb_trim() done\n')

    # Delete any .tmp files created by python3-wget
    func.clean_up(cwd)
    print('\nclean_up() done\n\nCAZy Database Parser complete!\n')

if __name__ == '__main__':
    main()
