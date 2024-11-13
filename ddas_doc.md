# Data Duplication Alert System using File Checksums

## `ddas.py`
This script contains the remove_duplicates function that removes duplicate files based on their checksums. The duplicates are identified by comparing checksums and then either moved to the trash or permanently deleted based on the specified mode.

**Dependencies:**
`os`: Provides functionalities for interacting with the operating system, such as removing files.
`logging`: Used for logging the process, including actions taken and errors encountered.
`send2trash`: A utility that allows safely sending files to the trash instead of permanently deleting them.

**Functions:**
`remove_duplicates(checksum_dict, deletion_mode="trash")`
This function removes duplicate files based on the provided checksum dictionary. It can either send files to the trash or permanently delete them.

**Parameters:**
`checksum_dict (dict):` A dictionary where keys are checksums (e.g., MD5, SHA1) and values are lists of file paths that share the same checksum (i.e., they are duplicates).
`deletion_mode (str, optional):` Specifies the deletion method.

**Acceptable values are:**
1. "trash" (default): Sends duplicates to the trash using `send2trash`.
2. "permanent": Permanently deletes the duplicate files using `os.remove`.

**Returns:**
(int): The total number of duplicates removed (either sent to the trash or permanently deleted).

**Logs:**
Logs information about each file removed and any errors encountered during the process.

## `file_handler.py`
This script contains utility functions to handle file operations such as listing files in a directory, generating checksums for files, and organizing files by their checksums to identify potential duplicates.

**Functions:**
`get_files_in_directory(directory)`
This function retrieves all the files in the specified directory and its subdirectories.

**Parameters:**
`directory (str):` The path of the directory to scan for files.

**Returns:**
(list): A list of file paths within the specified directory, including all files in subdirectories.

`generate_checksum(file_path)`
This function generates the MD5 checksum for a given file. The checksum is used for file comparison to identify duplicates.

**Parameters:**
`file_path (str):` The path of the file for which to generate the checksum.

**Returns:**
(str): The MD5 checksum of the file.

`organize_files_by_checksum(files)`
This function organizes a list of files by their checksums, grouping files with identical checksums together. This helps in identifying potential duplicates.

**Parameters:**
`files (list):` A list of file paths for which to generate checksums and group by checksum.

**Returns:**
(dict): A dictionary where keys are checksums and values are lists of file paths with the same checksum.

## `logger.py`
This script sets up a logger that can log messages to both the terminal and a log file (removal_log.txt). It allows for flexible logging, either printing to the terminal alone or logging to both terminal and a file.

**Functions:**
`setup_logger(log_to_file=True)`
This function sets up a logger that can output log messages to both the console and a file. The log file is named removal_log.txt by default. The logger is configured to log messages with an INFO level and higher.

**Parameters:**
`log_to_file (bool, optional):` 
If True (default), logs will be written to a file (removal_log.txt). If False, logs will only be printed to the console.

**Returns:**
(logging.Logger): A logger object that can be used to log messages.

## `main.py`
This script provides a terminal-based user interface (UI) for managing file duplication removal tasks. It integrates with the file-handling utilities (file_handler.py), duplicate removal functionality (ddas.py), and logging system (logger.py). Users can navigate directories, select deletion modes (trash or permanent), and view logs of the operations performed.

**Functions:**
`display_message(stdscr, message, x=0, y=0, highlight=False)`
Displays a message on the screen at specified coordinates. Optionally, highlights the message.

**Parameters:**
`stdscr (curses.window):` The window object provided by curses.
`message (str):` The message to display.
`x, y (int):` The coordinates where the message will be displayed.
`highlight (bool, optional):` If True, the message is highlighted.

`get_deletion_mode(stdscr)`
Prompts the user to select a deletion mode (Trash or Permanent).

**Parameters:**
`stdscr (curses.window):` The window object provided by curses.

**Returns:**
(str): Either "trash" or "permanent", depending on the user's selection.

`list_directories(path)`
Returns a list of directories in the given path.

**Parameters:**
`path (str):` The directory path to scan.

**Returns:**
(list): A list of directory names in the specified path.

`navigate_directories(stdscr)`
Allows the user to navigate directories and select one.

**Parameters:**
`stdscr (curses.window):` The window object provided by curses.

**Returns:**
(str or None): The selected directory path or None if the user cancels.

`display_progress(stdscr, progress, total, y_pos=5)`
Displays a progress bar on the screen.

**Parameters:**
`stdscr (curses.window):` The window object provided by curses.
`progress (int):` The current progress (number of duplicates processed).
`total (int):` The total number of duplicates.
`y_pos (int, optional):` The Y position to display the progress bar.

`move_to_trash(file_path)`
Moves a file to the trash. Implements different logic for Windows and Unix-based systems.

**Parameters:**
`file_path (str):` The path to the file to be moved to the trash.

**Returns:**
(bool): True if the file was successfully moved, False otherwise.

`start_duplication_removal(stdscr)`
Starts the file duplication removal process. Allows the user to choose a directory, selects a deletion mode, and performs the duplicate removal.

**Parameters:**
`stdscr (curses.window):` The window object provided by curses.

`view_logs(stdscr)` 
Displays the contents of the log file in the terminal.

**Parameters:**
stdscr (curses.window): The window object provided by curses.

`main_menu(stdscr)`
Displays the main menu and handles navigation between options (Duplication Removal, View Logs, and Exit).

**Parameters:**
`stdscr (curses.window):` The window object provided by curses.

### **Main Flow:**
**Main Menu:** Displays options to start duplication removal, view logs, or exit.
**Duplication Removal:** Allows the user to navigate directories, select a deletion mode (Trash or Permanent), scan the selected directory for duplicates, and remove them while displaying a progress bar.
**View Logs:** Displays the contents of the removal log file (removal_log.txt).
**Logging:** Utilizes the logger.py script to log progress, errors, and actions performed.

## Key Concepts:
### **File Checksum:**

A checksum is a unique value (often represented as a hash) calculated from the contents of a file. It serves as a fingerprint for that file. The checksum is generated using an algorithm (in this case, MD5), and even a small change in the file content will result in a completely different checksum.
**Purpose:** Checksum values are used to identify duplicate files. By comparing the checksums of files in a directory, the tool can determine whether two files are identical (duplicates) or not.
**How It Works:** The tool calculates the checksum for each file in a directory, and files with matching checksums are grouped together as duplicates.

**MD5 (Message Digest Algorithm 5):**
MD5 is a cryptographic hash function that produces a 128-bit hash value, often represented as a 32-character hexadecimal number. It is commonly used to verify the integrity of data.
In the Tool: The MD5 checksum is used to identify duplicate files. The checksum is generated by reading the contents of the file in chunks and producing a hash value. Files with the same hash value are considered duplicates.

### **File Deduplication:**

Deduplication is the process of identifying and eliminating redundant copies of files. This can be done by comparing file contents (via checksums or other methods) and removing the excess copies, which are deemed unnecessary.
In the Tool: The tool removes duplicate files by identifying those with the same checksum and then allowing the user to delete or move them to the trash.

### **Deletion Modes:**

1. **Trash Deletion:** Instead of permanently deleting files, they are moved to the system's trash/recycle bin. This allows the user to recover files if they are deleted by mistake.
2. **Permanent Deletion:** Files are permanently deleted from the system. They are not recoverable from the trash or recycle bin.

### **File Operations:**

1. **Moving Files to Trash:** The tool can move duplicate files to the trash or recycle bin using send2trash (for cross-platform support). This action is reversible, meaning the user can recover the files later.
2. **Permanently Deleting Files:** The tool can also permanently delete duplicate files using the os.remove() function, which removes files from the file system completely.

### **Directory Navigation:**

The tool allows users to navigate directories and choose the folder from which they want to remove duplicates. This is done via a text-based user interface, where the user can use arrow keys to select directories.

### **Logging:**

The tool logs all actions in a text file (removal_log.txt). This includes:
1. The number of files scanned.
2. The number of duplicates found and removed.
3. Any errors encountered during the file deletion process.
4. The log helps keep track of the tool’s operations and can be useful for troubleshooting.

### **`Curses` Library:**

The curses library is used to create a text-based user interface (TUI) in the terminal. It allows users to interact with the program using the keyboard, navigate directories, and choose options for deletion modes.
The interface also includes features like progress bars to show how far along the deduplication process is.

### **Error Handling:**

Error handling in the tool is important for ensuring smooth operation. If a file cannot be accessed or deleted, an error message is logged, and the user is notified. This ensures the program doesn’t crash unexpectedly.
Examples of errors include permission issues, invalid file paths, and file access issues.

### **Why Use File Checksums?**
**Efficiency:** Checking file checksums is a highly efficient method for detecting duplicate files. It avoids comparing file sizes or manually inspecting file contents.
**Accuracy:** MD5 checksums are designed to produce unique results for different file contents, ensuring that even small differences between files result in different checksum values.
**Speed:** MD5 checksums can be calculated quickly, making it feasible to scan large directories and identify duplicates in a reasonable amount of time.

## **System Requirements:**
1. Python 3.x or higher
2. Operating System: Windows, macOS, or Linux
3. Required Python Packages:
3.1 os
3.2 hashlib
3.3 shutil
3.4 send2trash
3.5 curses (only works on Unix-based systems, but is used for the terminal interface)

## Installation:

### 1. Clone or Download the Repository:

Download the repository containing the code files, or clone it using the following Git command:

```bash
git clone <repository_url>
```

### 2. Install Required Libraries:
The tool requires some external Python libraries to function properly. Install them using pip:

```python
pip install windows-curses
pip install send2trash
```

### 3. Set Up Log File:
A log file (removal_log.txt) will be created automatically when the tool is used. This log will track all actions taken by the program.


## **Troubleshooting:**

**Terminal Window Size:** Ensure your terminal window is large enough to display the menu and messages properly. If the terminal window is too small, you will be prompted to resize it.

**Permissions:** Ensure that the program has the necessary permissions to delete or move files to the trash.

**File Access Issues:** If the program encounters any issues accessing or modifying files (e.g., read-only files), it will log these errors in the log file.

## **Key Bindings:**

**Arrow Keys:** Navigate through directories.
**Enter Key:** Select the highlighted directory or option.
**1:** Choose Trash deletion mode.
**2:** Choose Permanent deletion mode.
**Esc:** Exit or cancel the current operation.
**Any Key:** Press to return to the menu after a task is completed.

# FAQs:

## Can I run the program on Windows?

Yes, the program works on Windows. Just ensure that you have installed the necessary Python packages, such as `windows-curses` for the curses library.

## What happens if I choose Permanent Deletion?

The file will be permanently deleted from your system and cannot be recovered unless you have backups.

## Can I undo the file deletion?

If you chose **Trash** deletion mode, the files will be moved to the trash/recycle bin, from where they can be restored. However, if you chose **Permanent deletion**, the files will be deleted permanently.
