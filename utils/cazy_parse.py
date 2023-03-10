import os
import wget
import pandas as pd
import utils.cazy_functions as func

# Working directory
home_dir = os.getcwd()
downloads_dir = f'{home_dir}/downloads'
results_dir = f'{home_dir}/results'
pages_dir = f'{downloads_dir}/cbm_pages'

# Make working directories if they don't exist
def dir_setup():
    func.dir_exists(downloads_dir)
    func.dir_exists(results_dir)
    func.dir_exists(pages_dir)
    return None


# Download all cbm pages listed on CAZy database
def wget_CAZy():
    # Download the main CAZy CBM page
    if not os.path.isfile(f'{downloads_dir}/Carbohydrate-Binding-Modules.html'):
        wget.download(url='http://www.cazy.org/Carbohydrate-Binding-Modules.html', out=downloads_dir)

    # Read html tables into a list of pandas DataFrames
    html_table = pd.read_html(f'{downloads_dir}/Carbohydrate-Binding-Modules.html')

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
        if not os.path.isfile(f'{pages_dir}/CBM{i}.html'):
            wget.download(url=f'http://www.cazy.org/CBM{i}.html', out=pages_dir)

# Convert HTML tables inside CAZy pages to an excel spreadsheet
def html_to_excel():
    substrate_dict = {}
    # fold_dict = {}
    # Create list of all html files in current directory
    html_files = [file for file in os.listdir(pages_dir) if file.endswith('.html')]
    html_files.sort()

    # Set up pages excel file writing
    pages_writer = pd.ExcelWriter(f'{results_dir}/CAZy Pages.xlsx', engine='xlsxwriter')

    # Convert html tables to sheets within an excel file
    for file in html_files:
        # Read table(s) from html file into a list of DataFrames
        html_table = pd.read_html(f'{pages_dir}/{file}')

        # Extract DataFrame from list
        html_df = html_table[0]

        # Write DataFrame to sheet in output excel file
        html_df.to_excel(pages_writer, sheet_name=file.strip('.html'), index=False, header=False)

        # Add Activity row to each directory
        labelled_html_df = html_df.set_index(0)

        # Use Note row if Activities row is empty
        if isinstance(labelled_html_df[1].loc['Activities in Family'], float) is True:
            substrate_dict[file.strip('.html')] = labelled_html_df[1].loc['Note']
        else:
            substrate_dict[file.strip('.html')] = labelled_html_df[1].loc['Activities in Family']
    pages_writer.close()

    # Set up cbm table excel file writing
    cbm_table_writer = pd.ExcelWriter(f'{results_dir}/CAZy CBM Table.xlsx', engine='xlsxwriter')

    # Convert CBM dictionary to a DataFrame
    cbm_df = pd.DataFrame.from_dict(substrate_dict, orient='index')
    cbm_df.columns = ['Activities in Family']

    # Convert DataFrame to Excel file
    cbm_df.to_excel(cbm_table_writer, sheet_name='CAZy CBM Table', index=True, header=True)
    cbm_table_writer.close()
