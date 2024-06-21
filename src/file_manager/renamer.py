from pathlib import Path
from os import system

import utils.file_operation_utils as u


# Define the folders to search
paths_to_get = [
    Path(r"C:\Users\hakaci-desktop\Hers\hoard\0_gifs"),
    Path(r"C:\Users\hakaci-desktop\Hers\hoard\0_imgs"),
    Path(r"C:\Users\hakaci-desktop\Hers\hoard\0_mix"),
    Path(r"C:\Users\hakaci-desktop\Hers\hoard\0_videos")
]

# CSV file path
path_MetadataCSV = Path(r"C:\Users\hakaci-desktop\Hers\hoard\Metadata_static.csv")

extentions_to_rename = [".mp4", ".png", ".jpg",
                        ".jpeg", ".webm", ".mov", ".gif", ".webp"]

# 37th fibonacci number for reverse naming constant
reverseNamingConst = 24157817

# enables ansi escape characters in terminal
system("")

def main():

    print("\nFull renamer started.")
    
    newFileAbsolutePaths = []

    # get metadata list
    metadataCSVList = u.get_metadata_csv_list(path_MetadataCSV)

    # Firstly lowercase then get all files
    u.lowercase_extentions()
    allFiles = u.file_search(paths_to_get, extentions_to_rename)

    # find new files
    metadataCSVList = u.get_absolute_paths_from_metadata_csv(metadataCSVList)
    metadataCSVList = list(map(Path, metadataCSVList))
    newFiles = set(allFiles).difference(metadataCSVList)

    # check if there is any files to rename
    if newFiles:
        # create and rename metadata rows
        newMetadataRows = u.create_rename_metadata_rows(newFiles)

        # append
        u.append_metadata_csv(newMetadataRows, path_MetadataCSV)

        # get new row's absolute paths
        # create and append absolute paths
        for row in newMetadataRows:
            newFileAbsolutePaths.append(Path(row[4] + "\\" + row[1] + row[2]))
    else:
        print("\n\033[0;30;47mNo files to rename\033[0;0m\n")

    print("Renamer finished.\n")

    return newFileAbsolutePaths


if __name__ == "__main__":
    main()
