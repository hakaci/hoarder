import csv
import yt_dlp
from os.path import join
from utils.file_operation_utils import get_metadata_csv_list

from config import (HOARD_YOUTUVBE_CSV_PATH,
                    HOARD_YOUTUBE_DOWNLOAD_PATH
                    )

csv_file_path = HOARD_YOUTUVBE_CSV_PATH
output_dir = HOARD_YOUTUBE_DOWNLOAD_PATH


def get_false_download_status_rows(rows, item_count_to_download):
    filtered_rows = []

    # Iterate over each row
    for row in rows:
        # Check if download_status is "False" (download_status is 8th column)
        if row[7] == "False":
            filtered_rows.append(row)
    
    # Calculate actual number of rows to process
    num_rows_to_process = min(item_count_to_download, len(filtered_rows))

    return filtered_rows[:num_rows_to_process]


def get_channels_list_from_csv(rows):

    # Collect unique channel names using a set to ensure uniqueness and by alphabetical
    channel_names = sorted({row[2] for row in rows[1:]})

    # Create the dictionary with channel_names
    channel_names = {index + 1: channel for index, channel in enumerate(channel_names)}

    return channel_names

def choose_channel(channel_names):

    print("\nAvailable channels:")
    for index, channel in channel_names.items():
        print(f"{index}: {channel}")

    while True:
        try:
            choice = int(input("\nEnter the number of the channel you want to choose: "))
            if choice in channel_names:
                return channel_names[choice]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    

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
        video_format_id = filtered_row[8]

        # Define the options for yt-dlp
        ydl_opts = {
            'format': f'{video_format_id}+bestaudio[ext=m4a]/bestaudio',  # Specify the format ID and audio codec
            'outtmpl': join(output_dir, f'%(timestamp)s - %(title)s - %(channel)s.%(ext)s'),  # Output template for downloaded file
            # 'merge_output_format': 'mp4',
            # 'postprocessors': [{
            #     'key': 'FFmpegVideoConvertor',
            #     'preferedformat': 'mp4'
            # }]
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
                        rows[index][7] = True
            except Exception as e:
                print(f"\nFailed to download video with ID: {row[0]}. Error: {e}\n")
        
    header = rows[0]  # First element is the header
    rows = rows[1:]   # Remaining elements are rows
    
    # Write updated_rows to the CSV file
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write the header
        writer.writerow(header)
        
        # Write all rows
        writer.writerows(rows)


def main():
    pass
        

if __name__ == "__main__":
    main()
