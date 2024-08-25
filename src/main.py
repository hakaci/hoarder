from youtube import append_youtube_video_metadata_csv as yvm
from youtube import downloader as dl

from os import system

# enables asci escape characters in terminal
system("")


def main():

    print("\nWelcome to hoarder\n")

    print("\033[0;30;47m*******Warning: Paths are static.*******\033[0;0m\n")

    print("\033[0;30;47m*******Warning: Don't forget to CLOSE media that going to process.*******\033[0;0m\n")

    print("1. Youtube metadata fetcher")
    print("2. Youtube video downloader from CVS file")
    selected_app = input("\nSelect an application(1 or 2): ")

    if selected_app == '1':
        yvm.append_youtube_video_metadata_csv()
    elif selected_app == '2':
        dl.download_youtube_video()
    else:
        print(f"Unknown application: {selected_app}. Available applications: '1' and '2'.")


if __name__ == "__main__":
    main()
