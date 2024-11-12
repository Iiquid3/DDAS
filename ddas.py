# This script contains the function that removes duplicate files based on checksums.

import os
import logging
from send2trash import send2trash  # Import send2trash for sending files to the trash

# Initialize logger
logger = logging.getLogger('DuplicationRemover')

def remove_duplicates(checksum_dict, deletion_mode="trash"):
    """
    Remove duplicates by either sending files to trash or deleting permanently.
    
    Parameters:
        checksum_dict (dict): Dictionary of checksums with lists of file paths.
        deletion_mode (str): Either 'trash' or 'permanent' for deletion mode.
    """
    duplicates_removed = 0
    for checksum, file_group in checksum_dict.items():
        if len(file_group) > 1:
            # Keep the first file, remove the rest as duplicates
            for file in file_group[1:]:
                try:
                    if deletion_mode == "trash":
                        send2trash(file)  # Send the duplicate file to the trash
                        logger.info(f"Sent to trash: {file}")
                    elif deletion_mode == "permanent":
                        os.remove(file)  # Permanently delete the file
                        logger.info(f"Permanently deleted: {file}")
                    
                    duplicates_removed += 1
                except Exception as e:
                    logger.error(f"Error removing file {file}: {e}")
    
    logger.info(f"Total duplicates removed: {duplicates_removed}")
    return duplicates_removed


