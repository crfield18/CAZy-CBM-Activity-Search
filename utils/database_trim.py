import pathlib
from collections import defaultdict
import pandas as pd
import wget
import utils.cazy_functions as func

# Working directory
cwd = pathlib.Path.cwd()
downloads_dir = cwd.joinpath('downloads')
results_dir = cwd.joinpath('results')
pages_dir = downloads_dir.joinpath('cbm_pages')

# Download the cazy_data file to the CAZy_database directory
def wget_database():
    # Make CAZy_database directory if it does not exist
    func.dir_exists(downloads_dir)
    # Download cazy_data.zip to CAZy_database if it does not exist
    database_zip = downloads_dir.joinpath('cazy_data.zip')
    if database_zip.is_file():
        pass
    else:
        wget.download(url='http://www.cazy.org/IMG/cazy_data/cazy_data.zip', out=str(downloads_dir))
    # Return path to cazy_data.zip
    return database_zip

# Read the database file and extract the lines relevant to CBMs
def db_trim(database_file:str):
    cbm_database = {
        'Family': [],
        'Domain': [],
        'Species': [],
        'GenBank Accession Number': []
    }
    family_list = []

    with open(database_file, 'r', encoding='utf-8') as input_file:
        # Write each line containing 'CBM' in the left column to the trimmed database
        for line in input_file:
            line_list = line.split()
            if 'CBM' not in line_list[0]:
                pass
            else:
                if line_list[0] not in family_list:
                    family_list.append(line_list[0])
                cbm_database['Family'].append(line_list[0])
                cbm_database['Domain'].append(line_list[1])
                cbm_database['Species'].append(' '.join(line_list[2:-1]))
                cbm_database['GenBank Accession Number'].append(line_list[-1])

    ## SHEET 1 ##
    # Write out trimmed database
    database_writer = pd.ExcelWriter(results_dir.joinpath('cazy_data_cbm_only.xlsx'), engine='xlsxwriter')
    cbm_df = pd.DataFrame.from_dict(cbm_database)
    cbm_df.to_excel(database_writer, sheet_name='CAZy Database CBMs', index=False, header=True)

    ## SHEET 2 ##
    # Count the occurrences of each CBM family in the trimmed
    family_counter = defaultdict(int)
    for family in cbm_database['Family']:
        family_counter[family] += 1
    family_counter = dict(family_counter)

    # Add any missing families to the counter dictionary
    for i in range(0, len(family_counter)):
        if f'CBM{i}' not in family_list:
            family_counter[f'CBM{i}'] = 0

    # Write out count dictionary
    family_counter = {family: count for family, count in sorted(family_counter.items(), key=lambda item: item[1], reverse=True)}
    family_counter_df = pd.DataFrame.from_dict(family_counter, orient='index')
    family_counter_df.columns = ['Count']
    family_counter_df.to_excel(database_writer, sheet_name='CBM Family Count', index=True, header=True)

    ## SHEET 3 ##
    # Count the occurrences of each Domain in the trimmed database
    domain_counter = defaultdict(int)
    for domain in cbm_database['Domain']:
        domain_counter[domain] += 1
    domain_counter = dict(domain_counter)

    domain_counter = {domain: count for domain, count in sorted(domain_counter.items(), key=lambda item: item[1], reverse=True)}
    domain_counter_df = pd.DataFrame.from_dict(domain_counter, orient='index')
    domain_counter_df.columns = ['Count']
    domain_counter_df.to_excel(database_writer, sheet_name='Domain Count', index=True, header=True)

    database_writer.close()
