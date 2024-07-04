import csv
from utils.youtube_utils import fetch_video_metadata, get_relavent_video_infos
from os.path import exists

from config import (HOARD_YOUTUBE_CSV_PATH
                    )

# CSV file path
csv_file_path = HOARD_YOUTUBE_CSV_PATH

# Field names for CSV header
fieldnames = [
    'id', 'title', 'channel', 'timestamp', 'download_status', 'duration', 'channel_id'
]


def append_metadata_to_csv(all_video_metadata):

    # Check if the CSV file exists, create it with header if it doesn't
    if not exists(csv_file_path):
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as file:
            csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
            csv_writer.writeheader()


    # Open the CSV file in append mode and initialize the CSV writer
    with open(csv_file_path, 'a', newline='', encoding='utf-8') as file:
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)

        # If the file is empty, write the header row
        if file.tell() == 0:
            csv_writer.writeheader()

        # Iterate over each video metadata dictionary and append to CSV
        for video_metadata in all_video_metadata:
            csv_writer.writerow(video_metadata)

    print(f"\nSuccessfully appended {len(all_video_metadata)} entries to {csv_file_path}.")


def append_youtube_video_metadata_csv():
    
    URL_type_options = {
        1: "Single video URLs",
        2: "Youtube playlist URL or Channel video section URL"
    }
    print("\nChoose URL type:")
    for index, URL_type in URL_type_options.items():
        print(f"{index}: {URL_type}")
    # Get URL type from user 
    URL_type = input("\nURL type(1 or 2): ")
                
    if URL_type == '1':
        # Initialize an empty list to store URLs
        youtube_urls = []

        while True:
            # Prompt the user for input
            youtube_url = input("Enter a URL (or enter 0 to finish): ")

            # Check if the user entered 0 to stop the input
            if youtube_url == "0":
                break

            # Append the entered URL to the list
            youtube_urls.append(youtube_url)
    
        video_infos = []
        for youtube_url in youtube_urls:
            video_infos.append(fetch_video_metadata(youtube_url))
            
        all_video_metadata = get_relavent_video_infos(video_infos)
        
        # Append metadata to CSV
        append_metadata_to_csv(all_video_metadata)       
    
    elif URL_type == '2':
        youtube_url = input("\nEnter youtube playlist URL or Channel video section URL: ")
        
        print(f"\nFetching metadata for {youtube_url}\n")
        video_infos = fetch_video_metadata(youtube_url)

        all_video_metadata = get_relavent_video_infos(video_infos)

        # Append metadata to CSV
        append_metadata_to_csv(all_video_metadata)
        

def main():
    pass
    # for video_metadata in all_video_metadata:
    #     print(video_metadata)
    

if __name__ == "__main__":
    main()
