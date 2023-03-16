import pathlib
import wget
import pandas as pd
import utils.cazy_functions as func

# Working directory
cwd = pathlib.Path.cwd()
downloads_dir = cwd.joinpath('downloads')
results_dir = cwd.joinpath('results')
pages_dir = downloads_dir.joinpath('cbm_pages')

# Make working directories if they don't exist
def dir_setup():
    func.dir_exists(downloads_dir)
    func.dir_exists(results_dir)
    func.dir_exists(pages_dir)

# Download all cbm pages listed on CAZy database
def wget_CAZy():
    # Download the main CAZy CBM page
    cbm_home_page = downloads_dir.joinpath('Carbohydrate-Binding-Modules.html')
    if not cbm_home_page.is_file():
        wget.download(url='http://www.cazy.org/Carbohydrate-Binding-Modules.html', out=str(downloads_dir))

    # Read html tables into a list of pandas DataFrames
    html_table = pd.read_html(cbm_home_page)

    # Convert DataFrame into list of rows
    rows = html_table[0].values.tolist()

    # Combine rows into a single list
    combined_list = [0]
    for i in range(len(rows)):
        combined_list += rows[i]

    # Convert values in list to integers
    int_list = [func.num_convert(n) for n in combined_list if func.num_convert(n) is not None]

    # Download all CBM pages that are not already downloaded
    for i in int_list:
    ## Use if you only want to download missing pages
    #     if not pages_dir.joinpath(f'CBM{i}.html').is_file():
    #         wget.download(url=f'http://www.cazy.org/CBM{i}.html', out=str(pages_dir))

    ## Use if re-downloading/updating already downloaded files (recommended)
        wget.download(url=f'http://www.cazy.org/CBM{i}.html', out=str(pages_dir))

# Convert HTML tables inside CAZy pages to an excel spreadsheet
def html_to_excel():
    substrate_dict = {}

    # Create list of all html files in current directory
    html_files = [file for file in pathlib.Path(pages_dir).glob('*.html') if file.is_file()]
    html_files.sort()

    # Set up pages excel file writing
    pages_writer = pd.ExcelWriter(results_dir.joinpath('CAZy Pages.xlsx'), engine='xlsxwriter')

    # Convert html tables to sheets within an excel file
    for file in html_files:
        # Read table(s) from html file into a list of DataFrames
        html_table = pd.read_html(file)

        # Extract DataFrame from list
        html_df = html_table[0]

        # Write DataFrame to sheet in output excel file
        # file_name_from_path = str(file).split('/')[-1]
        file_name_from_path = str(file).rsplit('/', maxsplit=1)[-1]
        html_df.to_excel(pages_writer, sheet_name=file_name_from_path.strip('.html'), index=False, header=False)

        # Add Activity row to each directory
        labelled_html_df = html_df.set_index(0)

        # Use Note row if Activities row is empty
        if isinstance(labelled_html_df[1].loc['Activities in Family'], float) is True:
            substrate_dict[file_name_from_path.strip('.html')] = labelled_html_df[1].loc['Note']
        else:
            substrate_dict[file_name_from_path.strip('.html')] = labelled_html_df[1].loc['Activities in Family']
    pages_writer.close()

    # Set up cbm table excel file writing
    cbm_table_writer = pd.ExcelWriter(results_dir.joinpath('CAZy CBM Table.xlsx'), engine='xlsxwriter')

    # Convert CBM dictionary to a DataFrame
    cbm_df = pd.DataFrame.from_dict(substrate_dict, orient='index')
    cbm_df.columns = ['Activities in Family']

    # Convert DataFrame to Excel file
    cbm_df.to_excel(cbm_table_writer, sheet_name='CAZy CBM Table', index=True, header=True)
    cbm_table_writer.close()
