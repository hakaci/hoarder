from pathlib import Path

from utils.file_operation_utils import file_search


gondolo_path = Path(r"D:\Videos\gon\gondolas\video")
gondolas_to_watch_path = Path(r"D:\Videos\gon\gondolas_to_watch")


def main():

    print("*******Warning: Paths are static.*******")
    number_of_gondolos_to_get = input(
        "How many gondolos do you want? (enter just int number): ")

    print("gondola_picker started.")

    # search files given paths or path
    files = file_search([gondolo_path], [".webm"])

    # gondolo mover according to given number. files list always random. so gondolos picken random
    for x in range(int(number_of_gondolos_to_get)):

        print(files[x].name)

        # Move gondolo to gondolas_to_watch_folder
        files[x].replace(gondolas_to_watch_path.joinpath(files[x].name))


if __name__ == "__main__":
    main()


print("gondola_picker finished.")
