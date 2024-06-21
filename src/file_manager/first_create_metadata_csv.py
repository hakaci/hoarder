from pathlib import Path
import os.path
import csv

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

extentions_to_get = [".mp4", ".png", ".jpg",
                        ".jpeg", ".webm", ".mov", ".gif", ".webp"]

# title names
fields = ["no", "file_name", "ext", "creation_date", "parent_path"]


def main():

    print("*******Warning: Paths are static*******")
    execute = input(
        "Wanna execute first Create Metadata CSV?(Y/N): ")

    if execute == "y" or execute == "Y":

        u.lowercase_extentions()
        all_files = u.file_search(paths_to_get, extentions_to_get)

        with open(path_MetadataCSV, "w", newline="", encoding="utf-8") as metadataCSVfile:

            # create list for metadata csv rows
            i = 0
            metadataListToWrite = []
            for file in all_files:
                i += 1

                # get file creation time in unixtime-stamp
                file_creationDate = os.path.getctime(file)

                # a single row
                tempRow = [str(i), file.stem, file.suffix, int(file_creationDate), file.parent]

                # append row to metadata list
                metadataListToWrite.append(tempRow)

            # get file writer object
            csvwriter = csv.writer(metadataCSVfile, delimiter=",")

            # Write title row
            csvwriter.writerow(fields)

            # write data to rows with list
            csvwriter.writerows(metadataListToWrite)

    else:
        exit("Create Metadata CSV exited.")

    print("Create Metadata CSV finished.")


if __name__ == "__main__":
    main()
