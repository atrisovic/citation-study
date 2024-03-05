"""Marker OCR file processing utilities"""

"""
See https://github.com/VikParuchuri/marker.git 
"""
import os
import subprocess


def process_files(
    path,
    output_path,
    script_dir,
    parallel_factor=2,
    max_pages=None,
    workers=1,
    max=None,
    metadata_file=None,
    min_length=None,
):
    """
    Convert a PDF or a directory of PDFs to markdown using the Marker OCR model.
    The function requires the location of the cloned Marker OCR repository and the desired naming convention for the output `.md` file or folder.
    Typical usage example:
    marker_ocr.process_files('../path_to_publication/publication.pdf', '../output_file_location_and_name/output.md', '../path_to_marker_repo/marker')
    Args:
        path (str): The path to the PDF file or directory of PDF files to be converted.
        output_path (str): The path to the output directory or file.
        script_dir (str): The path to the Marker OCR repository.
        parallel_factor (int, optional): The number of parallel processes to use. Defaults to 2.
        max_pages (int, optional): The maximum number of pages to process. Defaults to None.
        workers (int, optional): The number of workers to use. Defaults to 1.
        max (int, optional): The maximum number of files to process. Defaults to None.
        metadata_file (str, optional): The path to the metadata file. Defaults to None.
        min_length (int, optional): The minimum length of the text to process. Defaults to None.
    Raises:
        Exception: An error occurred.
    """
    try:
        os.chdir(script_dir)  # change the current working directory

        if os.path.isfile(path):
            command = f"poetry run python {os.path.join(script_dir, 'convert_single.py')} {path} {output_path} --parallel_factor {parallel_factor}"
            if max_pages:
                command += f" --max_pages {max_pages}"
        elif os.path.isdir(path):
            command = f"poetry run python {os.path.join(script_dir, 'convert.py')} {path} {output_path} --workers {workers}"
            if max:
                command += f" --max {max}"
            if metadata_file:
                command += f" --metadata_file {metadata_file}"
            if min_length:
                command += f" --min_length {min_length}"
        else:
            print(f"{path} is not a valid file or directory")
            return

        process = subprocess.Popen(command, shell=True)
        process.wait()
    except Exception as e:
        print(f"An error occurred: {e}")


def list_files(directory):
    """Returns a set of file names in the given directory."""
    return set(os.listdir(directory))


directory1 = "../papers"
directory2 = "../markdown"

# List files in each directory
files_in_dir1 = list_files(directory1)
files_in_dir2 = list_files(directory2)

script_dir = "marker"

files_in_dir2 = [f[:-4] for f in files_in_dir2]

# Check for files in directory1 not in directory2 and convert them
for file_name in files_in_dir1:
    if file_name[:-4] not in files_in_dir2:
        file_path = os.path.join(directory1, file_name)
        process_files(file_path, directory2, script_dir)
        print(f"Converted {file_name} to markdown")
