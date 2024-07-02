

def update_video_formats():
    video_IDs = []
    while True:
        # Prompt the user for input
        video_ID = input("Enter a video ID (or enter 0 to finish): ")

        # Check if the user entered 0 to stop the input
        if video_ID == "0":
            break

        # Append the entered URL to the list
        video_IDs.append(video_ID)
        
    

def main():
    pass
    

if __name__ == "__main__":
    main()
