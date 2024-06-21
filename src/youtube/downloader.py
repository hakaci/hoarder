import csv
import yt_dlp
from os.path import join
from utils.file_operation_utils import get_metadata_csv_list

csv_file_path = r"C:\Users\hakaci-desktop\Videos\downloder_outputs\youtube_download_list.csv"
output_dir = r"C:\Users\hakaci-desktop\Videos\downloder_outputs"


def get_false_download_status_rows(rows, item_count_to_download):
    filtered_rows = []

    # Skips the header row
    rows = rows[1:]

    # Iterate over each row in the CSV reader
    for row in rows:
        # Check if download_status is "False" (download_status is 8th column)
        if row[7] == "False":
            filtered_rows.append(row)
    
    # Calculate actual number of rows to process
    num_rows_to_process = min(item_count_to_download, len(filtered_rows))
    return filtered_rows[:num_rows_to_process]


def download_youtube_video(item_count_to_download):
    # get all rows from csv
    rows = get_metadata_csv_list(csv_file_path)

    # Create a list to hold updated rows
    updated_rows = list(rows)

    # get x number of False download status rows
    filtered_rows = get_false_download_status_rows(rows, item_count_to_download)

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
                        updated_rows[index][7] = True
            except Exception as e:
                print(f"\nFailed to download video with ID: {row[0]}. Error: {e}\n")
        
    header = updated_rows[0]  # First element is the header
    rows = updated_rows[1:]   # Remaining elements are rows
    
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
