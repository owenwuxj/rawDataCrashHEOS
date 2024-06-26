# Script to process ed's logparse results in folder input/Summary_xxx.txt
# and the outputs are the mkdirs corresponding folderNames/output_xx.txt

import os
import re


def extract_failure_statistics(file_path):
    with open(file_path, 'r') as file:
        first_line = file.readline().strip()

    # Extract words after "Failure Statistics for " in the first line
    match = re.search(r'Failure Statistics for (.+)', first_line)
    if match:
        return match.group(1)
    else:
        return None


def extract_mac_addresses(file_path):
    with open(file_path, 'r') as file:
        first_line = file.readline().strip()

    # Extract words after "Failure Statistics for " in the first line
    match = re.search(r'MAC Addresses processed for (.+)', first_line)
    match2 = re.search(r'Processed MAC Addresses for (.+)', first_line)
    if match:
        return match.group(1)
    elif match2:
        return match2.group(1)
    else:
        return None


def extract_unique_stacktrace(file_path):
    with open(file_path, 'r') as file:
        first_line = file.readline().strip()

    # Extract words after "Failure Statistics for " in the first line
    match = re.search(r'Unique Stacktrace Signatures for (.+)', first_line)
    if match:
        return match.group(1)
    else:
        return None


def extract_watchdog_events(file_path):
    with open(file_path, 'r') as file:
        first_line = file.readline().strip()

    # Extract words after "Failure Statistics for " in the first line
    match = re.search(r'Watchdog Events for (.+)', first_line)
    if match:
        return match.group(1)
    else:
        return None


def extract_oom_events(file_path):
    with open(file_path, 'r') as file:
        first_line = file.readline().strip()

    # Extract words after "Failure Statistics for " in the first line
    match = re.search(r'OOM Events for (.+)', first_line)
    if match:
        return match.group(1)
    else:
        return None


def extract_unprov_events(file_path):
    with open(file_path, 'r') as file:
        first_line = file.readline().strip()

    # Extract words after "Failure Statistics for " in the first line
    match = re.search(r'Unprovisioned Events for (.+)', first_line)
    if match:
        return match.group(1)
    else:
        return None


def rename_and_move_files(input_files, in_folder):
    os.makedirs(os.path.join(in_folder, "Failure Statistics"), exist_ok=True)
    os.makedirs(os.path.join(in_folder, "Watchdog Events"), exist_ok=True)
    os.makedirs(os.path.join(in_folder, "Unique Stacktrace Signatures"), exist_ok=True)
    os.makedirs(os.path.join(in_folder, "MAC Addresses processed"), exist_ok=True)
    os.makedirs(os.path.join(in_folder, "OOM Events"), exist_ok=True)
    os.makedirs(os.path.join(in_folder, "Unprovisioned Events"), exist_ok=True)

    files = input_files
    for file_name in files:
        file_path = os.path.join(in_folder, file_name)
        new_name = extract_failure_statistics(file_path)
        if new_name:
            new_path = os.path.join(in_folder, "Failure Statistics", f"{new_name}.txt")
            os.rename(file_path, new_path)
            print(f"Renamed '{file_name}' to '{new_name}.txt' and moved to 'Failure Statistics' folder")
            continue
        else:
            print(f"Failed to extract failure statistics from '{file_name}'. Skipping file.")

        new_name = extract_mac_addresses(os.path.join(in_folder, file_name))
        if new_name:
            new_path = os.path.join(in_folder, "MAC Addresses processed", f"{new_name}.txt")
            os.rename(file_path, new_path)
            print(f"Renamed '{file_name}' to '{new_name}.txt' and moved to 'MAC Addresses processed' folder")
            continue
        else:
            print(f"Failed to extract MAC Addresses from '{file_name}'. Skipping file.")

        new_name = extract_unique_stacktrace(os.path.join(in_folder, file_name))
        if new_name:
            new_path = os.path.join(in_folder, "Unique Stacktrace Signatures", f"{new_name}.txt")
            os.rename(file_path, new_path)
            print(f"Renamed '{file_name}' to '{new_name}.txt' and moved to 'Stacktrace' folder")
            continue
        else:
            print(f"Failed to extract Unique Stacktrace Sign from '{file_name}'. Skipping file.")

        new_name = extract_watchdog_events(os.path.join(in_folder, file_name))
        if new_name:
            new_path = os.path.join(in_folder, "Watchdog Events", f"{new_name}.txt")
            os.rename(file_path, new_path)
            print(f"Renamed '{file_name}' to '{new_name}.txt' and moved to 'watchdog_events' folder")
            continue
        else:
            print(f"Failed to extract Watchdog Events from '{file_name}'. Skipping file.")

        new_name = extract_oom_events(os.path.join(in_folder, file_name))
        if new_name:
            new_path = os.path.join(in_folder, "OOM Events", f"{new_name}.txt")
            os.rename(file_path, new_path)
            print(f"Renamed '{file_name}' to '{new_name}.txt' and moved to 'watchdog_events' folder")
            continue
        else:
            print(f"Failed to extract OOM Events from '{file_name}'. Skipping file.")

        new_name = extract_unprov_events(os.path.join(in_folder, file_name))
        if new_name:
            new_path = os.path.join(in_folder, "Unprovisioned Events", f"{new_name}.txt")
            os.rename(file_path, new_path)
            print(f"Renamed '{file_name}' to '{new_name}.txt' and moved to 'watchdog_events' folder")
            continue
        else:
            print(f"Failed to extract Unprovisioned Events from '{file_name}'. Skipping file.")


def process_all_txt_files_in_folder(in_folder):
    print(os.listdir(in_folder), in_folder)
    files = [file for file in os.listdir(in_folder) if file.endswith('.txt')]  # found all txt files
    if files:
        rename_and_move_files(files, in_folder)
    else:
        print(f"Failed to find txt files")


###################################################################################################
## Above is the second step to process/rename & move all the output files #########################
###################################################################################################


def separate_strings(input_file):
    with open(input_file, 'r') as file:
        data = file.read()

    # Split the data by the separator "*************"
    strings = data.split("=====================================================")

    return strings


def write_strings(strings, input_file):
    summary_folder_name = os.path.splitext(input_file)[0]  # Extracting filename without extension
    os.makedirs(summary_folder_name, exist_ok=True)  # Creating a folder with the same name as input file
    for i, string in enumerate(strings):
        output_file = os.path.join(summary_folder_name, f'output_{i + 1}.txt')  # Path to output file
        with open(output_file, 'w') as file:
            file.write(string.strip())


def split_into_txt_files_in_folders(input_folder):
    for file_name in os.listdir(input_folder):
        if file_name.endswith('.txt'):
            input_file = os.path.join(input_folder, file_name)
            strings = separate_strings(input_file)
            write_strings(strings, input_file)
            print(
                f"Separation complete for '{input_file}'! {len(strings)} strings separated "
                f"and saved to the folder '{os.path.splitext(input_file)[0]}'.")


###################################################################################################
## Above is the first step to cut the Summary.txt into small output files.#########################
###################################################################################################


def main():
    input_folder = 'input4'  # Change this to your input folder path

    # Form the first level txt files' folders
    split_into_txt_files_in_folders(input_folder)  # Cut all BIG the SummaryX.txt files to small SummaryX folders

    # Form the second levels - all the /summary_folder_name/Xxx.txt for renaming and grouping into
    # failures/wdg/oom... folders
    for folder_name in os.listdir(input_folder):
        if folder_name == ".DS_Store" or folder_name.endswith('.txt'):
            continue
        else:
            process_all_txt_files_in_folder(os.path.join(input_folder, folder_name))  # in one SummaryX folder
            # to rename/move all the txt files into diff folders(fail, wdg...)

        # Traverse each folder_name to form the "clustersAndDate" NODE by Date

        # go into each folder to form the "ClusterProdxREV" NODE by the cluster and xRev

        # ... then "productsByOsType" & "productTypesInOsType" -> "DWAR-COre-CY2023"/"DWHI-Core-FY22"/"All-Prod"

        # ... then to have "crashTypesCounts"+"WatchdogCounts"+"TotalUserInitiatedUploads"+"TotalOOM"+"stacktrace"

        # into the JSON file


if __name__ == "__main__":
    main()
