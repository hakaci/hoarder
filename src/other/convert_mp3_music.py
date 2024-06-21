import subprocess
from pathlib import Path
from os import makedirs, system
from os.path import dirname, basename, exists


from utils.file_operation_utils import file_search


extentions_to_get = [".mp4", ".webm", ".mp3"]

temp_path = r"C:\Users\hakaci-desktop\Music\_convert_mp3_temp"

# enables ansi escape characters in terminal
system("")  

def main():

    print("\n\033[0;30;47m*******Warning: Don't forget to CLOSE media that going to process.*******\033[0;0m\n")

    music_folder_path = input("\nEnter folder absolute path: ")

    # # Create folders and subfolder in temporaty folder
    # u.copy_folders_to_another_folder(music_folder_path, temp_path)

    # # Get extentions names. (Dont forget to edit extentions_to_get varible)
    # u.print_extension_types(music_folder_path)
    
    files = file_search([music_folder_path], extentions_to_get)

    # check if there are any files to convert
    if files:
        encode_to_mp3(files)
    else:
        print("\n\033[0;30;47mNo files to convert\n\033[0;0m\n")

    print("\nMP3 converter finished\n")
  

def encode_to_mp3(files):

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
        else:
            print(f"error converting {file}, errno: {process.returncode}")
            # Remove file if error (sometimes ffmpeg creates a corrupted/empty file)
            if output_path.exists():
                output_path.unlink()

if __name__ == "__main__":
    main()