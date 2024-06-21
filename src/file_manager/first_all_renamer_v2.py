from pathlib import Path

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

# 37th fibonacci number for reverse naming constant
reverseNamingConst = 24157817


def main():

    print("*******Warning: Paths are static*******")
    execute = input(
        "Wanna execute first AllRenamer?(Y/N): ")

    if execute == "y" or execute == "Y":

        # get metadata list
        allMetadataRowsList = u.get_metadata_csv_list(path_MetadataCSV)
        
        # delete title row
        del allMetadataRowsList[0]

        # rename file given list
        for row in allMetadataRowsList:
             
            # create absolute path with CVS columns
            absolutePathStr = row[4] + "\\" + row[1] + row[2]
            absolutePath = Path(absolutePathStr)

            # create new name absolute path: constant - No
            newName = str(reverseNamingConst - int(row[0])) + absolutePath.suffix
            newNameAbsolute = absolutePath.parent.joinpath(newName)

            # rename with new name
            absolutePath.rename(newNameAbsolute)

    else:
        exit("AllRenamer exited.")

    print("AllRenamer finished.")


if __name__ == "__main__":
    main()
