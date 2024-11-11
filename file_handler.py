# This file contains functions to handle file operations like listing files in a directory and generating checksums for comparison.


import os
import hashlib

def get_files_in_directory(directory):
    """Get all files in a given directory and its subdirectories."""
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            files.append(file_path)
    return files

def generate_checksum(file_path):
    """Generate MD5 checksum for a given file."""
    hash_md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def organize_files_by_checksum(files):
    """Organize files by checksum (grouping duplicates)."""
    checksum_dict = {}
    for file in files:
        checksum = generate_checksum(file)
        if checksum not in checksum_dict:
            checksum_dict[checksum] = []
        checksum_dict[checksum].append(file)
    return checksum_dict
