from pathlib import Path
from datetime import datetime as dt
import csv
from os.path import getctime, splitext, join, exists, relpath
from os import makedirs, walk
from operator import itemgetter


# Define the folders to search
paths_to_get = [
    Path(r"C:\Users\hakaci-desktop\Hers\hoard\0_gifs"),
    Path(r"C:\Users\hakaci-desktop\Hers\hoard\0_imgs"),
    Path(r"C:\Users\hakaci-desktop\Hers\hoard\0_mix"),
    Path(r"C:\Users\hakaci-desktop\Hers\hoard\0_videos")
]

# CSV file path
path_MetadataCSV = Path(r"C:\Users\hakaci-desktop\Hers\hoard\Metadata_static.csv")
path_DropedMetadataCSV = Path(r"C:\Users\hakaci-desktop\Hers\hoard\Droped_Metadata.csv")


extentions_to_get = [".mp4", ".png", ".jpg",
                        ".jpeg", ".webm", ".mov", ".gif", ".webp"]

# title names
fields = ["no", "file_name", "ext", "creation_date", "parent_path"]


def file_search(paths, extentions):

    # Search folders and append all_files
    all_files = []

    for path in paths:

        # example exts. [".mp4", ".png", ".jpg", ".jpeg", ".webm", ".mov", ".gif", ".webp"]
        files = {
            p.resolve()
            for p in Path(path).glob("**/*") if p.suffix in
            extentions
        }

        # Append found files one by one
        for file in files:
            all_files.append(file)

    return all_files


def lowercase_extentions():  # Lowercase to uppercase extentions like .PNG to .png

    # Just start from folder
    paths = [Path(r"C:\Users\hakaci-desktop\Hers\hoard")]

    # extentions list to lowered
    upper_extentions = [".MP4", ".PNG", ".JPG",
                        ".JPEG", ".WEBM", ".MOV", ".GIF", ".WEBP"]

    # Find all files' path with given extention
    files = file_search(paths, upper_extentions)

    for file in files:

        # Get lowercased extention string
        lowercased_extention = file.suffix.lower()

        # rename file with new lowercased extention
        file.rename(file.with_suffix(lowercased_extention))


def print_extension_types(folder_path):
    extension_types = {}

    # Walk through the directory tree
    for root, _, files in walk(folder_path):
        for filename in files:
            # Split the file name and extension
            _, extension = splitext(filename)
            # Remove the dot from the extension
            extension = extension[1:]
            # Increment the count for this extension type
            extension_types[extension] = extension_types.get(extension, 0) + 1

    print("\nExtension types in the folder:")
    for extension, count in extension_types.items():
        print(f".{extension}: {count} file(s)")


def empty_hoard_forders():
    # search files given paths or path
    lowercase_extentions()
    files = file_search(paths_to_get, extentions_to_get)

    for file in files:
        file.unlink()

def copy_folders_to_another_folder(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    if not exists(output_folder):
        makedirs(output_folder)

    # Walk through the directory tree
    for root, directories, _ in walk(input_folder):
        # Create corresponding directories in the output folder
        for directory in directories:
            src_dir = join(root, directory)
            dest_dir = join(output_folder, relpath(src_dir, input_folder))
            makedirs(dest_dir, exist_ok=True)


def sort_files_by_creation_date(files):

    # Create timestamp, absolute file path array
    timestamps_filepaths = []

    # fill timestamp_filepath array
    for file in files:
        # add to first column file creation time in unixtime-stamp
        # add to second column file path
        timestamps_filepaths.append(
            [getctime(file), file])

    # sort timestamp_filepath array related to timestamp
    timestamps_filepaths.sort(key=itemgetter(0))

    # get path colunm.
    files = []
    for time_filespath in timestamps_filepaths:
        files.append(time_filespath[1])

    return files


def rename_a_file_given_name(file, new_file_name):

    # rename the file
    file_extention = file.suffix
    ParentDicName = file.absolute().parent

    new_file_name = Path(new_file_name)

    # create absolute path with new name for rename function
    absolute_new_file_name = ParentDicName.joinpath(
        new_file_name.with_suffix(file_extention))

    # rename
    file.rename(absolute_new_file_name)


def get_start_unixtimestamp_by_given_day(day):

    # 86400 is one day in unixtime.
    days_in_unixtime = float(day) * 86400

    # Get creation_date_to_start by subtructing given days
    utc_now = dt.utcnow()
    creation_date_to_start = utc_now.timestamp() - days_in_unixtime

    return creation_date_to_start


def get_metadata_csv_list(path):

    # Open metadata CSV file
    with open(path, newline="", encoding="utf-8") as metadataCSVfile:

        # get file reader object
        allMetadataRows = csv.reader(metadataCSVfile, delimiter=",")     

        return list(allMetadataRows)


def get_last_row_of_csv(path):

    # get metadata list
    metaDataList = get_metadata_csv_list(path)

    # return last row
    return metaDataList.pop(-1)


def get_absolute_paths_from_metadata_csv(metadataCSVList):

    absolutePaths = []

    # delete title row
    del metadataCSVList[0]

    # create and append absolute paths
    for row in metadataCSVList:

        absolutePaths.append(row[4] + "\\" + row[1] + row[2])

    return absolutePaths


def get_file_path_from_name(nameList):

    pathList = []

    # get paths from CVS for searching
    pathsFromCSV = get_absolute_paths_from_metadata_csv(get_metadata_csv_list(path_MetadataCSV))
    pathsFromCSV = list(map(Path, pathsFromCSV))

    # iterate names for searching
    for name in nameList:
        # search in path list
        for path in pathsFromCSV:
            # if found, add paths to new list, then break
            if str(name) == path.name:
                pathList.append(path)
                break
    
    return pathList


def get_file_path_from_stem(stemList):

    pathList = []

    # get paths from CVS for searching
    pathsFromCSV = get_absolute_paths_from_metadata_csv(get_metadata_csv_list(path_MetadataCSV))
    pathsFromCSV = list(map(Path, pathsFromCSV))

    # iterate stems for searching
    for stem in stemList:
        # search in path list
        for path in pathsFromCSV:
            # if found, add paths to new list, then break
            if str(stem) == path.stem:
                pathList.append(path)
                break
    
    return pathList


def write_metadata_csv(listToWrite, path):

    with open(path, "w", newline="", encoding="utf-8") as metadataCSVfile:

        # get file writer object
        csvwriter = csv.writer(metadataCSVfile, delimiter=",")

        # Write title row
        csvwriter.writerow(fields)

        # write data to rows with list
        csvwriter.writerows(listToWrite)


def append_metadata_csv(listToAppend, path):

     with open(path, "a", newline="", encoding="utf-8") as metadataCSVfile:
         
        # get file writer object
        csvwriter = csv.writer(metadataCSVfile, delimiter=",")

        # append data to rows with list
        csvwriter.writerows(listToAppend)


def create_rename_metadata_rows(files):

    metadataRows = []

    # get last row of metadataCSV
    lastRowCSV = get_last_row_of_csv(path_MetadataCSV)
    lastNo = int(lastRowCSV[0])
    lastName = int(lastRowCSV[1])

    # create path, creationdata list sorted.
    # Create timestamp, absolute file path list
    timestamps_filepaths = []

    # fill timestamp_filepath list
    for file in files:

        # add to first column file creation time in unixtime-stamp
        # add to second column file paths
        timestamps_filepaths.append(
            [int(getctime(file)), file])

    # sort timestamp_filepath array related to timestamp
    timestamps_filepaths.sort(key=itemgetter(0))

    # create rows sorted str
    i = 0
    for timestamps_filepath in timestamps_filepaths:
        i += 1
        rename_a_file_given_name(timestamps_filepath[1], str(lastName - i))
        metadataRows.append([str(lastNo + i), str(lastName - i), str(timestamps_filepath[1].suffix), str(timestamps_filepath[0]), str(timestamps_filepath[1].parent)])

    return metadataRows


def update_metadata_csv():

    pathListNames = []
    allFilesNames = []
    metadataCSVList = get_metadata_csv_list(path_MetadataCSV)
    newItemMetaData = metadataCSVList.copy()
    newItemMetaDataPath = []
    dropedMetadataList = []
    filesChangedDirectory = []
    filesChangedDirectoryReal = []

    # Firstly lowercase then get all files
    lowercase_extentions()
    allFiles = file_search(paths_to_get, extentions_to_get)

    # get absolute paths from CSV file
    pathList = get_absolute_paths_from_metadata_csv(metadataCSVList)

    # maps all items to windows file path from str
    pathList = list(map(Path, pathList))
    allFiles = list(map(Path, allFiles))

    #get names
    for pathItem in pathList:
        pathListNames.append(pathItem.stem)
    for file in allFiles:
        allFilesNames.append(file.stem)

    # find deleted items
    deletedItems = set(pathListNames).difference(allFilesNames)

    # find and pop deleted file with names in metadata list
    for deletedItem in deletedItems:
        i = 0
        for metadataCSV in newItemMetaData:
            if metadataCSV[1] == deletedItem:
                dropedMetadataList.append(newItemMetaData.pop(i))
                break
            i += 1

    # find old csv rows which files that changed directory
    newItemMetaDataPath = get_absolute_paths_from_metadata_csv(newItemMetaData)
    newItemMetaDataPath = list(map(Path, newItemMetaDataPath))
    filesChangedDirectory = set(newItemMetaDataPath).difference(allFiles)

    # find new location
    for fileChangedDirectory in filesChangedDirectory:
        filesChangedDirectoryName = fileChangedDirectory.stem
        i = 0
        for allFilesName in allFilesNames:
            if filesChangedDirectoryName == allFilesName:
                filesChangedDirectoryReal.append(allFiles[i])
            i += 1

    # update file parents
    filesChangedDirectoryReal = list(map(Path, filesChangedDirectoryReal))
    for fileChangedDirectory in filesChangedDirectoryReal:

        i = 0
        filesChangedDirectoryParent = fileChangedDirectory.parent
        filesChangedDirectoryName = fileChangedDirectory.stem
        
        for metadataCSV in newItemMetaData:
            if metadataCSV[1] == filesChangedDirectoryName:
                newItemMetaData[i][4] = str(filesChangedDirectoryParent)
                break
            i += 1

    # apend deleted file's metadata to droped csv
    append_metadata_csv(dropedMetadataList, path_DropedMetadataCSV)

    # write new csv file with updated path and without deleted items
    write_metadata_csv(newItemMetaData, path_MetadataCSV)


def main():

    print("*******Warning: Paths are static.*******")
    execute = input("\nWanna execute? (Y/N): ")

    if execute == "y" or execute == "Y":
        update_metadata_csv()

    else:
        exit("\nexited")

    print("\nfileOp_utils finished.")
    

if __name__ == "__main__":
    main()
