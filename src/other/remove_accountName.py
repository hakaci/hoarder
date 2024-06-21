from pathlib import Path

from utils.file_operation_utils import file_search, rename_a_file_given_name


def main():

    print("*******Remove until -.*******")
    path = input(
        "Enter path: ")

    files_path = Path(path)

    print("Remover started.")

    files = file_search([files_path], [".m4a", ".mp4", ".M4A", ".MP4"])

    for file in files:

        # counter for pointing "-"
        i = 1

        # get file name
        file_name = file.name

        # iter until "-" and count
        for file_char in file_name:

            if file_char == '-':
                i += 1
                break

            i += 1

        # slice string after "- "
        new_file_name = file_name[i:]

        rename_a_file_given_name(file, Path(new_file_name))

    print("Remover finished.")


if __name__ == "__main__":
    main()
