import os
import csv
import pandas as pd


def process_folder(input_folder):
    input_dir = input_folder

    # List to hold extracted data
    data_module_prod_types = []

    # Append 32 columns header data/letters for the file as the first row, for the usage of MergeCSVdata.py
    data_num_crash_types = ['abcdefghijklmnopqrestuvwxyz12345']

    # Specify the columns to extract (0-based index)
    columns_to_extractProductType = [0, 6, 7]  # Example:"Failure Statistics for Product Type : (AIOS5 DENON_COMP_DHAMP)
    columns_to_extractModuleNames = [0, 3]  # exp: "Failure Statistics for AIOS65"
    columns_to_extractNumOfCrashes = [0, 1]  # Example: extract 1st and 2nd columns which are numbers and crashTypes

    # Define two sets of strings
    crashType_set = {"HEALTH_HUB", "GEM", "AMS", "CLI", "HOME_AUTOMATION", "NPPL", "AIOSDSP", "MCU_CONTROL",
                     "CLOUDCONTROL", "NETWORKMANAGER", "UPNP_SERVER", "WEB-API", "WEB_CONTROL", "Watchdog", "Critical",
                     "System"}
    moduleType_set = {"AIOS4", "AIOS5", "AIOS6", "AIOS65", "AIOS7", "AIOS8", "AIOS9", "HS1", "HS2"}

    # Iterate over each file in the directory
    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):
            file_data = []  # Temporary list to hold data for a single file
            with open(os.path.join(input_folder, filename), 'r') as infile:
                for line in infile:
                    columns = line.split()

                    if len(columns) > max(columns_to_extractProductType):
                        extracted_columns = [columns[i] for i in columns_to_extractProductType]
                        data_module_prod_types.append(extracted_columns)

                    if len(columns) > max(columns_to_extractNumOfCrashes):
                        extracted_crash_columns = [columns[i] for i in columns_to_extractNumOfCrashes]
                        if extracted_crash_columns[1] in crashType_set:
                            file_data.extend(extracted_crash_columns)

                    if len(columns) > max(columns_to_extractModuleNames):
                        extracted_module_columns = [columns[i] for i in columns_to_extractModuleNames]
                        if extracted_module_columns[1] in moduleType_set:
                            data_module_prod_types.append(extracted_module_columns)

            if file_data:
                data_num_crash_types.append(file_data)

    # Save extracted data to CSV files
    output_file_prod_types = input_dir + 'consolidated_outputProdTypes.csv'
    output_file_num_crash = input_dir + 'consolidated_outputNumCrash.csv'

    with open(output_file_prod_types, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(data_module_prod_types)

    with open(output_file_num_crash, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(data_num_crash_types)

    print(f'Data extracted and consolidated into {output_file_prod_types} and {output_file_num_crash}')

    # Merge the two CSV files into one
    df = pd.read_csv(output_file_num_crash)

    columns1 = []
    columns2 = []

    for i in range(0, df.shape[1], 2):
        col1 = df.columns[i]
        col2 = df.columns[i + 1]
        columns1.append(df[col1])
        columns2.append(df[col2])

    final_col1 = pd.concat(columns1, ignore_index=True)
    final_col2 = pd.concat(columns2, ignore_index=True)

    final_df = pd.DataFrame({
        'joined_col1': final_col1,
        'joined_col2': final_col2
    })

    output_file_path = input_dir + 'output_file.csv'
    final_df.to_csv(output_file_path, index=False)

    print(f"Every two columns have been successfully joined into two long columns and saved to {output_file_path}")


def main():
    input_folder = 'input4/Summary_319.350_0617w/Failure Statistics/'
    process_folder(input_folder)


if __name__ == "__main__":
    main()
