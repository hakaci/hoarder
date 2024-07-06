import subprocess
import csv
from pathlib import Path
from os import makedirs, system
from os.path import dirname, basename, exists

from utils.file_operation_utils import file_search

from config import (CONVERT_MP3_CSV_PATH,
                    CONVERT_MP3_OUTPUT_PATH
                    )

csv_file_path = CONVERT_MP3_CSV_PATH
temp_path = CONVERT_MP3_OUTPUT_PATH

extentions_to_get = [".mp4", ".webm", ".mp3"]
# Define the CSV header
header = ["File Name"]

# enables ansi escape characters in terminal
system("")  

def get_new_file_paths(files):
    # Read converted file names from the CSV file
    converted_file_names = set()
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header
        for row in reader:
            converted_file_names.add(row[0])

    # Get file names from searched file paths
    file_names = [Path(file).name for file in files]
    
    # Subtract converted file names from searched file names to get new file names
    new_file_names = set(file_names) - converted_file_names
    
    # Get absolute paths from new file names
    file_path_dict = {Path(file_path).name: file_path for file_path in files}  # Create a dictionary mapping file names to their absolute paths
    new_file_paths = [file_path_dict[file_name] for file_name in new_file_names if file_name in file_path_dict] # Retrieve absolute paths using new file names
    
    return new_file_paths

def encode_to_mp3(files):
    successfully_converted_file_paths = []
    
    for file in files:

        # Get new file name with new suffix
        newFileName = Path(file.stem + ".mp3")

        # Get parent directory name
        ParentDirName = dirname(file)
        ParentDirBaseName = basename(ParentDirName)

        # Get temp directory name
        tempDiretoryName = Path(temp_path + "\\" + ParentDirBaseName)

        # Create parent folder in temp folder if not exist
        if not exists(tempDiretoryName):
            makedirs(tempDiretoryName)

        # Create output path for ffmpeg output
        output_path = tempDiretoryName.joinpath(newFileName)

        # Command line argument
        args = ["ffmpeg", "-i", file, "-vn", "-acodec", "libmp3lame", "-ab", "128k", output_path]

        # to call ffmpeg
        process = subprocess.run(args)

        # check to executed sucessfully
        if process.returncode == 0:
            print(f"sucessfully converted {file}")
            successfully_converted_file_paths.append(file)
        else:
            print(f"error converting {file}, errno: {process.returncode}")
            # Remove file if error (sometimes ffmpeg creates a corrupted/empty file)
            if output_path.exists():
                output_path.unlink()

    return successfully_converted_file_paths

def main():

    print("\n\033[0;30;47m*******Warning: Don't forget to CLOSE media that going to process.*******\033[0;0m\n")

    music_folder_path = input("\nEnter folder absolute path: ")

    files = file_search([music_folder_path], extentions_to_get)
    
    new_file_paths = get_new_file_paths(files)
    
    # Check if there are any files to convert
    if new_file_paths:
        successfully_converted_file_paths = encode_to_mp3(new_file_paths)
                
        data_to_write = [[successfully_converted_file_path.name] for successfully_converted_file_path in successfully_converted_file_paths]

        with open(csv_file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(data_to_write)

        print(f"New file names written to {csv_file_path}")
    else:
        print("\n\033[0;30;47mNo files to convert\n\033[0;0m\n")

    print("\nMP3 converter finished\n")


if __name__ == "__main__":
    main()