import os
import wget
import pandas as pd

# Current working directory
home_dir = os.getcwd()
cbm_page_dir = f'{home_dir}/CAZy_cbm_pages'

# Make directory if it doesn't exist
def dir_exists(directory:str):
    if os.path.exists(directory) == False:
        return os.makedirs(directory)

# Convert each value in combined_list to an integer if possible
def num_convert(num_string:str):
    try:
        return int(num_string)
    except ValueError:
        pass

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
    # Create list of all html files in current directory
    html_files = [file for file in os.listdir(cbm_page_dir) if file.endswith('.html')]
    html_files.sort()

    # Set up excel file writing
    writer = pd.ExcelWriter(f'{home_dir}/CAZy Pages.xlsx', engine='xlsxwriter')

    # Convert html tables to sheets within an excel file
    for file in html_files:
        print(file)
        # Read table(s) from html file into a list of DataFrames
        html_table = pd.read_html(f'{cbm_page_dir}/{file}')

        # Extract DataFrame from list
        html_df = html_table[0]

        # Write DataFrame to sheet in output excel file
        html_df.to_excel(writer, sheet_name=file.strip('.html'), index=False, header=False)

        ######### Placeholder plain text of what i want to do
        # Add activity row to each directory
        cbm_dict = {}

        for row in html_df:
            print(row)
            # if first column value is 'Activities in Family':
            #     cbm_dict[file.strip('.html')] = column value
            #     break

        # Convert CBM dictionary to a DataFrame

        # Convert DataFrame to csv file

    writer.close()

def test():
    wget_CAZy()
    html_to_excel()

def main():
    wget_CAZy()
    html_to_excel()

if __name__ == '__main__':
    test()
    # main()
