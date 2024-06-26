from pathlib import Path
import shutil

import utils.file_operation_utils as u

from config import (HOARD_TEMP_PATH,
                        HOARD_METADATA_CSV_PATH
                        )

# daily_temp path
temp_path = HOARD_TEMP_PATH

# CSV file path
path_MetadataCSV = HOARD_METADATA_CSV_PATH

extentions_to_get = [".mp4", ".png", ".jpg",
                     ".jpeg", ".webm", ".mov", ".gif", ".webp"]

ItemAmount = 610

def main():

    print("\nLast file getter started.")

    # get metadata csv list
    metadataListCSV = u.get_metadata_csv_list(path_MetadataCSV)

    # get last 100 item
    lastItems = metadataListCSV[-ItemAmount:]

    # create and append absolute paths
    lastPaths = []
    for row in lastItems:
        lastPaths.append(row[4] + "\\" + row[1] + row[2])
        
    lastPaths = list(map(Path, lastPaths))

    # get last created items to temp folder
    get_last_files(lastPaths)

    print("Last file getter finished.\n")

    return "Last file getter return"


def get_last_files(Paths):

    # clear temp folder content
    newFiles = clear_temp_folder_content(Paths)    

    # new file paths
    newFilesPaths = u.get_file_path_from_name(newFiles)

    # copy files to daily_temp
    for newFilesPath in newFilesPaths:
        shutil.copy(newFilesPath, temp_path)


def clear_temp_folder_content(Paths):

    # create temp folder if not exist
    if not temp_path.exists():
        temp_path.mkdir()

    # get temp files
    tempFiles = u.file_search([temp_path], extentions_to_get)

    #get names
    pathNames = []
    tempPathNames = []
    for pathItem in Paths:
        pathNames.append(pathItem.name)
    for pathItem in tempFiles:
        tempPathNames.append(pathItem.name)

    # find new files
    newFiles = set(pathNames) - set(tempPathNames)
    # find old files
    oldFiles = set(tempPathNames) - set(pathNames)
    
    # unlink old files
    for oldFile in oldFiles:
        temp_path.joinpath(oldFile).unlink()

    return newFiles


if __name__ == "__main__":
    main()
