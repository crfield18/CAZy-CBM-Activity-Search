import os
import wget
import pandas as pd
from functions import dir_exists, num_convert

# Current working directory
home_dir = os.getcwd()
cbm_page_dir = f'{home_dir}/CAZy_cbm_pages'

# Download all cbm pages listed on CAZy database
def wget_CAZy():
    # Make CBM pages directory page if it does not exist
    dir_exists(cbm_page_dir)

    # Check for existing html files
    downloaded_html_files = [file for file in os.listdir(cbm_page_dir) if file.endswith('.html')]

    # Download the main CAZy CBM page
    if not os.path.isfile(f'{home_dir}/Carbohydrate-Binding-Modules.html'):
        wget.download(url='http://www.cazy.org/Carbohydrate-Binding-Modules.html', out=home_dir)

    # Read html tables into a list of pandas DataFrames
    html_table = pd.read_html('Carbohydrate-Binding-Modules.html')

    # Convert DataFrame into list of rows
    rows = html_table[0].values.tolist()

    # Combine rows into a single list
    combined_list = [0]
    for i in range(len(rows)):
        combined_list += rows[i]

    # Convert values in list to integers
    int_list = [num_convert(n) for n in combined_list if num_convert(n) is not None]

    # Download all CBM pages that are not already downloaded
    for i in int_list:
        if f'CBM{i}.html' not in downloaded_html_files:
            wget.download(url=f'http://www.cazy.org/CBM{i}.html', out=cbm_page_dir)

# Convert HTML tables inside CAZy pages to an excel spreadsheet
def html_to_excel():
    substrate_dict = {}
    fold_dict = {}
    # Create list of all html files in current directory
    html_files = [file for file in os.listdir(cbm_page_dir) if file.endswith('.html')]
    html_files.sort()

    # Set up pages excel file writing
    pages_writer = pd.ExcelWriter(f'{home_dir}/CAZy Pages.xlsx', engine='xlsxwriter')

    # Convert html tables to sheets within an excel file
    for file in html_files:
        # Read table(s) from html file into a list of DataFrames
        html_table = pd.read_html(f'{cbm_page_dir}/{file}')

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
    cbm_table_writer = pd.ExcelWriter(f'{home_dir}/CAZy CBM Table.xlsx', engine='xlsxwriter')

    # Convert CBM dictionary to a DataFrame
    cbm_df = pd.DataFrame.from_dict(substrate_dict, orient="index")
    cbm_df.columns = ['Activities in Family']

    # Convert DataFrame to Excel file
    cbm_df.to_excel(cbm_table_writer, sheet_name='CAZy CBM Table', index=True, header=True)
    cbm_table_writer.close()

def main():
    wget_CAZy()
    html_to_excel()

if __name__ == '__main__':
    main()
