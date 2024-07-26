from file_manager import video_finder_and_converter_ffmpeg as ve
from file_manager import renamer as rn
from file_manager import metadata_cleaner as mdc
from file_manager import get_last_files as lfg

from youtube import append_youtube_video_metadata_csv as yvm
from youtube import downloader as dl

from other import convert_mp3_music as cmm
from other import replace_string as rs

from utils.file_operation_utils import update_metadata_csv

from os import system

# enables asci escape characters in terminal
system("")


def main():

    print("\nWelcome to hoarder\n")

    print("\033[0;30;47m*******Warning: Paths are static.*******\033[0;0m\n")

    print("\033[0;30;47m*******Warning: Don't forget to CLOSE media that going to process.*******\033[0;0m\n")

    print("1. File organizer")
    print("2. Youtube metadata fetcher")
    print("3. Youtube video downloader from CVS file")
    print("4. Other")
    selected_app = input("\nSelect an application(1 or 2 or 3 or 4): ")

    if selected_app == '1':
        execute_all = input("\nWanna execute all; encoder, renamer, cleaner, last file getter? (Y/N): ")
        if execute_all == "y" or execute_all == "Y":
            # update file paths and update deleted file rows
            update_metadata_csv()

            ve.main()
            newRenamedFilePaths = rn.main()
            mdc.main(newRenamedFilePaths)
            lfg.main()
        else:
            exit("\nFile organizer exited")
        print("\nFile organizer finished\n")
    elif selected_app == '2':
        yvm.append_youtube_video_metadata_csv()
    elif selected_app == '3':
        dl.download_youtube_video()
    elif selected_app == '4':
        # cmm.main()
        rs.main()
    else:
        print(f"Unknown application: {selected_app}. Available applications: '1', '2' and '3'.")


if __name__ == "__main__":
    main()
