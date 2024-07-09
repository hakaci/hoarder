import csv
import yt_dlp
from os.path import join
from utils.file_operation_utils import get_metadata_csv_list
from utils.youtube_utils import (get_channels_list_from_csv, 
                                 choose_channel, 
                                 get_false_download_status_rows
                                 )

from config import (HOARD_YOUTUBE_CSV_PATH,
                    HOARD_YOUTUBE_DOWNLOAD_PATH
                    )

csv_file_path = HOARD_YOUTUBE_CSV_PATH
output_dir = HOARD_YOUTUBE_DOWNLOAD_PATH


def download_youtube_video():
    filtered_rows = []

    # Get all rows from csv
    rows = get_metadata_csv_list(csv_file_path)

    # Get channel names
    channel_names = get_channels_list_from_csv(rows)

    # Get channel name from user
    chosen_channel_name = choose_channel(channel_names)

    # Filter by channel name
    for row in rows[1:]:
        if row[2] == chosen_channel_name:
            filtered_rows.append(row)
    
    # Get number of videos to download.       
    try:
        item_count_to_download = int(input("\nEnter item count number to download from CSV: "))        
    except ValueError:
        print("Invalid input. Please enter a valid number.")
          
    # Get x number of False download status rows
    filtered_rows = get_false_download_status_rows(filtered_rows, item_count_to_download)

    for filtered_row in filtered_rows:
        video_id = filtered_row[0]

        # Define options for yt-dlp
        ydl_opts = {
            'format_sort': ['ext', 'res:1080', '+vbr'],
            'outtmpl': join(output_dir, f'%(timestamp)s - %(title)s - %(channel)s.%(ext)s'),  # Output template for downloaded file
        }

        # Initialize YoutubeDL object
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                # Construct the video URL using provided options
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                
                # Download the video using the URL
                ydl.download([video_url])
                print(f"\nSuccessfully downloaded video with ID: {video_id}\n")
                
                # Iterate over each row in CSV rows
                for index, row in enumerate(rows):
                    if row[0] == video_id:
                        # Found the matching ID, mark download_status as True
                        rows[index][4] = True
            except Exception as e:
                print(f"\nFailed to download video with ID: {video_id}. Error: {e}\n")
        
    # Write updated rows to the CSV file
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write all rows
        writer.writerows(rows)


def main():
    pass
        

if __name__ == "__main__":
    main()
