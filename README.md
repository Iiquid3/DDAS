## Data Duplication Removal Using File Checksum
This project aims to help users efficiently identify and remove duplicate files from a specified directory by comparing their checksums (MD5 or SHA256). The solution works by scanning the directory, calculating the checksums of files, and identifying duplicates. The program then removes these duplicates, ensuring that only identical files are deleted, while maintaining data integrity.

The project offers a terminal-based interface, allowing users to navigate directories, view progress, and interact with the duplication removal process. It includes features like real-time progress bars, logging, and safe deletion by either moving duplicates to a backup directory or sending them to the system trash.
