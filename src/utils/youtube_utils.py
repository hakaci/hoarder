from os import path, makedirs
import yt_dlp


def get_convenient_formats(formats):
    # Initialize an empty dictionary to store convenient formats
    convenient_formats = {}

    # Iterate through video formats
    for fmt in formats:
        # Extract width, height, vbr, and extension (ext) from the format
        width = fmt.get('width')
        height = fmt.get('height')
        vbr = fmt.get('vbr')
        ext = fmt.get('ext')

        # Skip formats that are None or higher than 1920x1080 or not MP4
        if (width is None or height is None or vbr is None or
                width > 1920 or height > 1080 or ext != 'mp4'):
            continue

        # Create a resolution tuple
        resolution = (width, height)

        # Check if the resolution tuple is already a key in the dictionary
        if resolution in convenient_formats:
            # Check if this format has a lower bitrate (vbr)
            if (convenient_formats[resolution]['vbr'] is None or 
                    (vbr is not None and vbr < convenient_formats[resolution]['vbr'])):
                convenient_formats[resolution] = fmt
        else:
            # Add the format to the convenient_formats dictionary
            convenient_formats[resolution] = fmt

    # Sort convenient_formats by resolution (descending order)
    sorted_formats = dict(sorted(convenient_formats.items(), key=lambda item: item[0], reverse=True))

    return sorted_formats


def get_lowest_bitrate_format(formats):
    lowest_bitrate = float('inf')  # Start with a very high value
    selected_format = None
    
    for fmt in formats:
        format_bitrate = fmt.get('abr') or fmt.get('vbr') or float('inf')
        if format_bitrate < lowest_bitrate:
            lowest_bitrate = format_bitrate
            selected_format = fmt
    
    return selected_format


def print_video_metadata(video_url):
    ydl_opts = {
        'quiet': False, # Print info messages
        'no_warnings': False, # Print warnings
        'force_generic_extractor': True, # Force generic extractor
        'force-ipv4': True, # Force IPv4
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            # Extract metadata for the video without downloading it
            video_info = ydl.extract_info(video_url, download=False)
            # Check if metadata was successfully retrieved
            if video_info:
                print("Video Metadata:")
                # Iterate through the metadata dictionary and print each key-value pair
                for key, value in video_info.items():
                    if isinstance(value, list):
                        # If the value is a list, join it into a comma-separated string
                        value = ', '.join(str(item) for item in value)
                    print(f"{key}: {value}")
            else:
                print(f"No metadata found for {video_url}")
        except Exception as e:
            print(f"Failed to extract metadata for {video_url}: {e}")


def print_generic_video_metadata(video_info):
    video_id = video_info.get('id')
    video_title = video_info.get('title')
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    video_duration = video_info.get('duration')
    video_upload_date = video_info.get('upload_date')

    print(f"Video ID: {video_id}")
    print(f"Title: {video_title}")
    print(f"Url: {video_url}")
    print(f"Duration: {video_duration} seconds")
    print(f"Upload Date: {video_upload_date}")

    video_formats = video_info.get('formats')
    if video_formats:
        print("Formats:")
        for fmt in video_formats:
            format_id = fmt.get('format_id')
            format_resolution = fmt.get('resolution')
            if not format_resolution:
                width = fmt.get('width')
                height = fmt.get('height')
                if width and height:
                    format_resolution = f"{width}x{height}"
                else:
                    format_resolution = "Unknown"
            format_extension = fmt.get('ext')
            format_bitrate = fmt.get('abr') if fmt.get('abr') else fmt.get('vbr') # Conditional (Ternary) Operator
            print(f"  - {format_id}: {format_resolution}, {format_extension}, {format_bitrate}kbps")


def list_video_info_fields(video_info):
    # Print all the fields (keys) in the video_info dictionary
    print("Available fields in video_info:")
    for key in video_info.keys():
        print(key)


def download_video(url, output_dir):
    # Create the output directory if it doesn't exist
    makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        # Specifies the output template for the downloaded file. Here, %(title)s.%(ext)s ensures that the downloaded file will be named using the video's title and extension.
        # Constructs the full path to the output file in the specified output_dir.
        'outtmpl': path.join(output_dir, '%(title)s.%(ext)s'),
    }
    # Initializes a YoutubeDL object with the specified options.
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Initiates the download of the video specified by url.
        ydl.download([url])


def fetch_video_metadata(channel_url):
    ydl_opts = {
        'quiet': False, # Print info messages
        'no_warnings': False, # Print warnings
        'ignoreerrors': True, # Ignore errors (e.g., private videos)
        'extract_flat': True, # Treat channel URL as a flat playlist
        'force_generic_extractor': True, # Force generic extractor
        'force-ipv4': True, # Force IPv4
    }

    video_metadata = []

    # Use yt-dlp with the specified options
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            # Extract metadata from url without downloading it
            video_info = ydl.extract_info(channel_url, download=False)
            if 'entries' in video_info:
                # Playlist or channel
                videos = video_info['entries']
                for video in videos:
                    video_id = video.get('id')
                    if not video_id:
                        continue  # Skip if video ID is not available
                    video_url = f"https://www.youtube.com/watch?v={video_id}"
                    print(f"\nFetching details for video ID: {video_id}")

                    # Extract metadata for each video
                    try:
                        video_metadata.append(ydl.extract_info(video_url, download=False))
                    except Exception as e:
                        print(f"\nFailed to extract video info for {video_url}: {e}")
                        continue
                
                return video_metadata
            else:
                # Single video
                return video_info
        except Exception as e:
            print(f"\nFailed to extract metadata for {channel_url}: {e}")
            return None


def main():
    channel_url = "https://www.youtube.com/c/MF%C3%87mefsoft/videos"
    video_url = "https://www.youtube.com/watch?v=ATVj1VAxcMo"
    output_dir = r"C:\Users\hakaci-desktop\Videos\downloder_outputs"

    # Fetch and print video metadata
    metadata = fetch_video_metadata(channel_url)
    for video in metadata:
        print_video_metadata(f"https://www.youtube.com/watch?v={video['id']}")

    # Download a video
    download_video(video_url, output_dir)


if __name__ == "__main__":
    main()