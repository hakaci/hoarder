import csv
from utils.youtube_utils import fetch_video_metadata, get_convenient_formats, update_with_new_rows
from os.path import exists

from config import (HOARD_YOUTUBE_CSV_PATH
                    )

# CSV file path
csv_file_path = HOARD_YOUTUBE_CSV_PATH

# Field names for CSV header
fieldnames = [
    'id', 'title', 'channel', 'duration_string', 'upload_date', 'timestamp',
    'original_url', 'download_status', 'selected_format_id', 'duration',
    'channel_id', 'channel_url', 'uploader', 'uploader_id', 'uploader_url',
    'webpage_url_domain'
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


def get_relavent_video_infos(video_infos):
    # List to store metadata for each video
    all_video_metadata = []    
    
    for video_info in video_infos:
        video_id = video_info.get('id')
        if not video_id:
            continue  # Skip if video ID is not available
        
        selected_formats = get_convenient_formats(video_info.get('formats'))
        # Get the first key-value pair (resolution and format details)
        first_resolution, first_format_details = next(iter(selected_formats.items()))
        # Extract the format ID from the format details
        selected_format_id = first_format_details['format_id']

        video_metadata = {
            'id': video_id,
            'title': video_info.get('title'),
            'channel': video_info.get('channel'),
            'duration_string': video_info.get('duration_string'),
            'upload_date': video_info.get('upload_date'),
            'timestamp': video_info.get('timestamp'),
            'original_url': video_info.get('original_url'),
            'download_status': False,
            'selected_format_id': selected_format_id,
            'duration': video_info.get('duration'),
            'channel_id': video_info.get('channel_id'),
            'channel_url': video_info.get('channel_url'),
            'uploader': video_info.get('uploader'),
            'uploader_id': video_info.get('uploader_id'),
            'uploader_url': video_info.get('uploader_url'),
            'webpage_url_domain': video_info.get('webpage_url_domain')
        }
        all_video_metadata.append(video_metadata)
    
    return all_video_metadata


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
                
        updated_rows = update_with_new_rows(all_video_metadata)
        
        # Write the updated metadata back to the CSV file
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(updated_rows)
        
        print(f"\nSuccessfully appended/updated {len(updated_rows)} entries to {csv_file_path}.")        
    
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
