import os

def find_missing_files(directory, start, end):
    existing_files = set()
    for filename in os.listdir(directory):
        if filename.endswith('.ass'):
            try:
                number = int(filename.split('.')[0])
                if start <= number <= end:
                    existing_files.add(number)
            except ValueError:
                continue

    missing_files = [num for num in range(start, end + 1) if num not in existing_files]
    return missing_files

if __name__ == "__main__":
    directory = 'temp_folder'
    start = 1053
    end = 1121
    missing_files = find_missing_files(directory, start, end)
    print("Missing files:", missing_files)