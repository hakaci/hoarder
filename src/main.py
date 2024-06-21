from file_manager import video_finder_and_converter_ffmpeg as ve
from file_manager import renamer as rn
from file_manager import metadata_cleaner as mdc
from file_manager import get_last_files as lfg

from youtube import append_youtube_video_metadata_csv as yvm
from youtube import downloader as dl

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
    selected_app = input("\nSelect an application(1 or 2 or 3): ")

    if selected_app == '1':
        execute_all = input("\nWanna execute all; encoder, renamer, cleaner, last file getter? (Y/N): ")
        if execute_all == "y" or execute_all == "Y":
            # update file paths and update deleted file rows
            update_metadata_csv()

            encodedFilePaths = ve.main()
            newRenamedFilePaths = rn.main()
            cleanerReturn = mdc.main(newRenamedFilePaths)
            lfgReturn = lfg.main()

            # print(encodedFilePaths)
            # print(newRenamedFilePaths)
            # print(cleanerReturn)
            # print(lfgReturn)
        else:
            exit("\nFile organizer exited")

        print("\nFile organizer finished\n")
    elif selected_app == '2':
        print("\n\033[0;30;47m*******Warning: Single video URL does not support.*******\033[0;0m\n")
        youtube_url = input("\nEnter youtube playlist URL or Channel video section URL: ")
        yvm.append_youtube_video_metadata_csv(youtube_url)
        # all_video_metadata = fetch_video_metadata(youtube_url)
        # if not isinstance(all_video_metadata, list):
        #     all_video_metadata = [all_video_metadata]
        # for video_metadata in all_video_metadata:
        #     print_generic_video_metadata(video_metadata)
    elif selected_app == '3':
        item_count_to_download = input("\nEnter item count number to download from CSV: ")
        try:
            item_count_to_download_integer = int(item_count_to_download)
            dl.download_youtube_video(item_count_to_download_integer)
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    else:
        print(f"Unknown application: {selected_app}. Available applications: '1', '2' and '3'.")


if __name__ == "__main__":
    main()
