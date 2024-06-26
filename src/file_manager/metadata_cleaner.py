import subprocess
from pathlib import Path
from os import system

from src.config import (HOARD_PATH,
                        HOARD_BROKEN_VIDS_PATH
                        )

real_path = HOARD_PATH
path_broken_vids = HOARD_BROKEN_VIDS_PATH

# enables ansi escape characters in terminal
system("")

def main(paths_to_clean):

    print("\nCleaner started.")

    # check if there is any files to clean
    if paths_to_clean:
        # clear given files and time
        metadata_clean(paths_to_clean)
    else:
        print("\n\033[0;30;47mNo files to clean\033[0;0m\n")

    print("Cleaner finished.\n")

    return "cleaner return"


def metadata_clean(paths):

    # Create temporary directory for files
    temp_folder = real_path.joinpath("temp")
    if not temp_folder.exists():
        temp_folder.mkdir()

    # Move files to temporary directory
    for file in paths:
        file.replace(temp_folder.joinpath(file.name))

    # clear files
    clear_metadata(temp_folder)

    # After cleaning return files to original dest
    for file in paths:
        # Original dest
        dest_of_org_file = file.absolute().parent.joinpath(file.name)
        # Temporary dest from file name
        temp_dest_of_file = temp_folder.joinpath(file.name)
        # move back the file
        temp_dest_of_file.replace(dest_of_org_file)

    # In the end, remove temp dicrectory
    temp_folder.rmdir()


def clear_metadata(path_to_clean):

    # build command line arg
    args_metadata_clean = ["exiftool",
                           "-overwrite_original", "-all=", " ", path_to_clean]

    # run the command line arg process
    process_1 = subprocess.run(args_metadata_clean)

    # check process_1 executed sucessfully
    if process_1.returncode == 0:
        print(f"metadata cleaned successfully")
    else:
        print(f"error when metadata cleaning, errno: {process_1.returncode}")


if __name__ == "__main__":
    main()