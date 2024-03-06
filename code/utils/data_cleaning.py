import re
import os
from typing import List

###
# Use the following code to load the documents and clean them:
# from data_cleaning import load_clean_doc_paths

# document_texts = load_clean_doc_paths(document_paths[:1])
# print(document_texts[0])
###


def remove_latex_tables(text):
    # This pattern matches \begin{table} followed by any characters (including newlines) up to \end{table}
    pattern = r"\\begin{table}.*?\\end{table}"

    # Replace found patterns with an empty string
    cleaned_text = re.sub(pattern, "", text, flags=re.DOTALL)
    return cleaned_text


def remove_before_introduction(text):
    # remove everything before ##### Introduction / Abstract
    pattern = r".*## \S Introduction"
    cleaned_text = re.sub(pattern, "", text, flags=re.DOTALL | re.IGNORECASE)
    cleaned_text = re.sub(
        r".*## Abstract", "", cleaned_text, flags=re.DOTALL | re.IGNORECASE
    )
    return cleaned_text


def remove_after_references(text):
    # remove everything after ###### References
    pattern = r"## References.*"
    cleaned_text = re.sub(pattern, "", text, flags=re.DOTALL | re.IGNORECASE)
    return cleaned_text


def clean_content_from_path(path: str) -> str:
    """
    Args:
        path (str): A valid, readable document path.

    Returns:
        str: Cleaned content of the document path.
    """
    with open(path, "r") as file:
        content = file.read()

    content = remove_before_introduction(content)
    content = remove_after_references(content)
    content = remove_latex_tables(content)

    content = content.replace("\n", " ").replace("\r", " ").replace("\t", " ").strip()

    # # get number of words in content
    # world_len = len(content.split())
    # print(world_len)
    return content


def load_clean_doc_paths(document_paths: List[str]) -> List[str]:
    """
    Args:
        document_paths (List[str]): A list of valid, readable document paths.

    Returns:
        List[str]: The content of the document paths, cleansed and normalized.
    """
    return [clean_content_from_path(path) for path in document_paths]


def get_text_before_introduction(text):
    # return everything before ##### Introduction / Abstract
    if ("Abstract" in text) or ("Introduction" in text):
        content = text.split("####")[0]
        return content
    else:
        return None
