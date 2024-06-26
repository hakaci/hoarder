import csv
from utils.youtube_utils import fetch_video_metadata, get_convenient_formats
from os.path import exists

from src.config import (HOARD_YOUTUVBE_CSV_PATH
                        )

# CSV file path
csv_file = HOARD_YOUTUVBE_CSV_PATH

# Field names for CSV header
fieldnames = [
    'id', 'title', 'channel', 'duration_string', 'upload_date', 'timestamp',
    'original_url', 'download_status', 'selected_format_id', 'duration',
    'channel_id', 'channel_url', 'uploader', 'uploader_id', 'uploader_url',
    'webpage_url_domain'
]


def write_metadata_to_csv(all_video_metadata):

    # Check if the CSV file exists, create it with header if it doesn't
    if not exists(csv_file):
        with open(csv_file, 'w', newline='', encoding='utf-8') as file:
            csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
            csv_writer.writeheader()


    # Open the CSV file in append mode and initialize the CSV writer
    with open(csv_file, 'a', newline='', encoding='utf-8') as file:
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)

        # If the file is empty, write the header row
        if file.tell() == 0:
            csv_writer.writeheader()

        # Iterate over each video metadata dictionary and append to CSV
        for video_metadata in all_video_metadata:
            csv_writer.writerow(video_metadata)

    print(f"\nSuccessfully appended {len(all_video_metadata)} entries to {csv_file}.")

def append_youtube_video_metadata_csv(url):
    # List to store metadata for each video
    all_video_metadata = []

    print(f"\nFetching metadata for {url}\n")
    video_infos = fetch_video_metadata(url)

    for video_info in video_infos:
        video_id = video_info.get('id')
        if not video_id:
            continue  # Skip if video ID is not available
        
        selected_formats = get_convenient_formats(video_info.get('formats'))
        # Get the first key-value pair (resolution and format details)
        first_resolution, first_format_details = next(iter(selected_formats.items()))
        # Extract the format ID from the format details
        selected_format_id = first_format_details['format_id']
        # # Print selected formats sorted by resolution
        # print("Selected Formats (Sorted by Resolution - Highest to Lowest):")
        # for resolution, fmt in video_infos.items():
        #     print(f"Resolution: {resolution}, Format ID: {fmt['format_id']}, VBR: {fmt['vbr']} kbps, Ext: {fmt['ext']}")

        video_metadata = {
            'id': video_id,
            'title': video_info.get('title'),
            'channel': video_info.get('channel'),
            'duration_string': video_info.get('duration_string'),
            'upload_date': video_info.get('upload_date'),
            'timestamp': video_info.get('timestamp'),
            'original_url': video_info.get('original_url'),
            'download_status': False,  # Placeholder for download status
            'selected_format_id': selected_format_id,  # Assuming selected_format is already defined
            'duration': video_info.get('duration'),
            'channel_id': video_info.get('channel_id'),
            'channel_url': video_info.get('channel_url'),
            'uploader': video_info.get('uploader'),
            'uploader_id': video_info.get('uploader_id'),
            'uploader_url': video_info.get('uploader_url'),
            'webpage_url_domain': video_info.get('webpage_url_domain')
        }
        all_video_metadata.append(video_metadata)

    # Append metadata to CSV
    write_metadata_to_csv(all_video_metadata)


def main():
    pass
    # for video_metadata in all_video_metadata:
    #     print(video_metadata)
    

if __name__ == "__main__":
    main()
