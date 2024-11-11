# This script contains the function that removes duplicate files based on checksums.

import os

def remove_duplicates(checksum_dict):
    """Remove duplicates by deleting files with the same checksum."""
    duplicates_removed = 0
    for checksum, file_group in checksum_dict.items():
        if len(file_group) > 1:
            for file in file_group[1:]:
                os.remove(file)  # Remove the duplicate file
                duplicates_removed += 1
    return duplicates_removed

