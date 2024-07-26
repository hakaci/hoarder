from utils.file_operation_utils import file_search, rename_a_file_given_name


extentions_to_get = [".mp4", ".webm", ".mp3", ".m4a"]


def get_user_input():
    string_to_replace = input("Enter the string to replace: ")
    replacement_string = input("Enter the replacement string: ")
    folder_paths = input("Enter folder paths separated by commas: ").split(',')
    folder_paths = [path.strip() for path in folder_paths]  # Remove any leading/trailing whitespace
    return string_to_replace, replacement_string, folder_paths


def main():
    # Get user input
    string_to_replace, replacement_string, folder_paths = get_user_input()
    
    # Get files absolute path
    files = file_search(folder_paths, extentions_to_get)
    
    for file in files:
        print(file)


if __name__ == "__main__":
    main()
