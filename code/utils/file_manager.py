import re
import os


def get_folder_content(folder_path, pattern):
    matched_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if re.search(pattern, file):
                matched_files.append(os.path.join(root, file))
    return matched_files
