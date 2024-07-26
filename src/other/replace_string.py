import os
from utils.file_operation_utils import file_search


extentions_to_get = [".mp4", ".webm", ".mp3", ".m4a"]


def get_user_input():
    strings_to_replace = input("Enter strings to replace separated by commas: ").split(',')
    replacement_string = input("Enter replacement string: ")
    folder_paths = input("Enter folder paths separated by commas: ").split(',')
    
    # Remove any leading/trailing whitespace
    folder_paths = [path.strip() for path in folder_paths]  
    
    return strings_to_replace, replacement_string, folder_paths


def replace_strings_in_filenames(files, string_to_replace, replacement_string):
    for file_path in files:
        dir_name = os.path.dirname(file_path)
        base_name = os.path.basename(file_path)
        
        if string_to_replace in base_name:
            new_base_name = base_name.replace(string_to_replace, replacement_string)
            new_file_path = os.path.join(dir_name, new_base_name)
            os.rename(file_path, new_file_path)
            print(f"Renamed: {base_name} -> {new_base_name}")


def main():
    # Get user input
    strings_to_replace, replacement_string, folder_paths = get_user_input()
    
    # Get files absolute path
    files = file_search(folder_paths, extentions_to_get)
    
    # Replace string with given string input
    for string_to_replace in strings_to_replace:
        replace_strings_in_filenames(files, string_to_replace, replacement_string)


if __name__ == "__main__":
    main()
