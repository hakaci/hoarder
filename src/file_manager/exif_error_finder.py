import subprocess
from pathlib import Path

from src.config import (HOARD_GIFS_PATH, 
                        HOARD_IMGS_PATH, 
                        HOARD_MIX_PATH, 
                        HOARD_VIDEOS_PATH,
                        HOARD_BROKEN_VIDS_PATH
                        )

# Define the folders to search
paths_to_get = [
    HOARD_GIFS_PATH,
    HOARD_IMGS_PATH,
    HOARD_MIX_PATH,
    HOARD_VIDEOS_PATH
]

# Path for broken videos
path_broken_vids = HOARD_BROKEN_VIDS_PATH

def main():
    """Main function to clear metadata from specified folders."""
    print("\nCleaner started.")

    for path in paths_to_get:
        clear_metadata(path)

    print("Cleaner finished.\n")
    return "cleaner return"

def clear_metadata(path_to_clean):
    """Clear metadata from files in the specified directory."""
    # Build command line arguments
    args_metadata_clean = ["exiftool", "-r", "-overwrite_original", "-all=", " ", str(path_to_clean)]

    # Run the command line process
    process_1 = subprocess.run(args_metadata_clean, capture_output=True, text=True)

    print(f"\nerr:\n{process_1.stderr}")
    print(f"\nout:\n{process_1.stdout}")

    # Check if process executed successfully
    if process_1.returncode == 0:
        print(f"Metadata cleaned successfully")
    else:
        print(f"Error when cleaning metadata, errno: {process_1.returncode}")

        # Get paths from error output
        err_absolute_paths = get_absolute_paths_from_exif_errors(process_1.stderr)

        # Move errored files to broken folder
        for err_absolute_path in err_absolute_paths:
            # Destination path
            new_destination = path_broken_vids.joinpath(err_absolute_path.name)
            err_absolute_path.replace(new_destination)

def get_absolute_paths_from_exif_errors(output):
    """Extract absolute file paths from exiftool error output."""
    absolute_paths = []

    # Split lines into list
    output_lines = output.splitlines()

    # Extract absolute paths
    for line in output_lines:
        # Find position of "-" followed by a space
        i = line.find('- ') + 2
        if i > 1:
            # Slice string after "- " and append
            absolute_paths.append(line[i:])

    # Map all items to Windows file paths
    absolute_paths = list(map(Path, absolute_paths))

    return absolute_paths

if __name__ == "__main__":
    main()
