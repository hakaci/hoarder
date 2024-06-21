import subprocess
from pathlib import Path
from numpy import random
from os import system

import utils.file_operation_utils as u


# Define the folders to search
paths_to_get = [
    Path(r"C:\Users\hakaci-desktop\Hers\hoard\0_gifs"),
    Path(r"C:\Users\hakaci-desktop\Hers\hoard\0_imgs"),
    Path(r"C:\Users\hakaci-desktop\Hers\hoard\0_mix"),
    Path(r"C:\Users\hakaci-desktop\Hers\hoard\0_videos")
]

path_broken_vids = Path(r"C:\Users\hakaci-desktop\Hers\hoard\broken_vids")
path_reencoded = Path(
    r"C:\Users\hakaci-desktop\Hers\hoard\broken_vids\reencoded__clean_this")

extensitons_to_encode = [".mov", ".webm"]

# enables ansi escape characters in terminal
system("") 

def main():

    print("\nVideo finder and converter started.")

    encodedFilePaths = []

    # Firstly lowercase then search files to convert
    u.lowercase_extentions()
    files = u.file_search(paths_to_get, extensitons_to_encode)

    # sort creation date(write util function)
    files = u.sort_files_by_creation_date(files)

    # check if there is any files to convert
    if files:
        # convert files
        encodedFilePaths = encode_to_mp4(files)
    else:
        print("\n\033[0;30;47mNo files to convert\n\033[0;0m\n")
  
    print("Video finder and converter finished.\n")
    return encodedFilePaths


def encode_to_mp4(all_files):
    
    encodedFilePaths = []

    for file in all_files:

        # Get parent directory name of file
        ParentDirName = file.parent

        # get file name
        fileName = Path(file.stem + "_" +str(random.randint(1000, 9999)))

        # Same file name with .mp4 suffix.
        output_name = ParentDirName.joinpath(fileName.with_suffix(".mp4"))

        # Command line argument
        args = ["ffmpeg", "-i", file, "-c:v", "libx264", "-c:a",
                "aac", output_name]

        # to call ffmpeg
        process = subprocess.run(args)

        # check to executed sucessfully
        if process.returncode == 0:
            print(f"sucessfully converted {file}")
            # Remove file if sucessfull
            if file.exists():
                file.unlink()
        else:
            print(f"error converting {file}, errno: {process.returncode}")
            # Remove file if error (sometimes ffmpeg creates a corrupted/empty file)
            if output_name.exists():
                output_name.unlink()

            # Move original file to broken_vid folder
            file.replace(path_broken_vids.joinpath(file.name))

        # get encoded file absolute path to a list
        encodedFilePaths.append(output_name)
    
    # return encoded files absolute path (pathlib.WindowsPath in list)
    return encodedFilePaths


def encode_to_webm_vp8(file):

    # incrementally name for this application. Because, can be overwrite other webm files.
    output_name = path_reencoded.joinpath(file.name)

    # Command line argument
    args = ["ffmpeg", "-i", file, "-c:v", "libvpx", "-c:a",
            "libvorbis", "-map", "0", "-map_metadata", "-1", output_name]

    # to call ffmpeg
    process = subprocess.run(args)

    # check to executed sucessfully
    if process.returncode == 0:
        print(f"sucessfully converted {file}")

        # If success, just change extention name for no more encode in future
        output_name.replace(output_name.with_suffix(".mp4"))
    else:
        print(f"error converting {file}, errno: {process.returncode}")
        # Remove file if error (sometimes ffmpeg creates a corrupted/empty file)
        if output_name.exists():
            output_name.unlink()


if __name__ == "__main__":
    main()
