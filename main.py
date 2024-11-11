# This script controls the user interface and interacts with the backend logic for removing duplicates.

import os
print("Current working directory:", os.getcwd())
import curses
from file_handler import get_files_in_directory, organize_files_by_checksum
from ddas import remove_duplicates
from logger import setup_logger

# Global logger for terminal output
logger = setup_logger()

def get_user_input(stdscr, prompt):
    """Function to get user input through the terminal."""
    curses.echo()  # Enable input echoing
    stdscr.addstr(2, 0, prompt)  # Prompt message
    user_input = stdscr.getstr(3, 0, 80).decode()  # Get user input from the terminal
    curses.noecho()  # Disable input echoing
    return user_input

def display_message(stdscr, message, x=0, y=0):
    """Display a message in the terminal."""
    stdscr.addstr(y, x, message)
    stdscr.refresh()

def list_directories(stdscr, path):
    
    """List directories in the current path and allow the user to select one."""
    files = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
    return files

def navigate_directories(stdscr):
    """Allow user to navigate directories and select one."""
    current_path = os.getcwd()
    selected_index = 0

    while True:
        directories = list_directories(stdscr, current_path)

        stdscr.clear()
        stdscr.addstr(0, 0, f"Current Directory: {current_path}")
        stdscr.addstr(1, 0, "Select a directory using arrow keys, press Enter to choose.")

        for idx, directory in enumerate(directories):
            if idx == selected_index:
                stdscr.addstr(idx + 2, 0, f"> {directory}", curses.A_REVERSE)
            else:
                stdscr.addstr(idx + 2, 0, f"  {directory}")

        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_DOWN:
            selected_index = (selected_index + 1) % len(directories)
        elif key == curses.KEY_UP:
            selected_index = (selected_index - 1) % len(directories)
        elif key == 10:  # Enter key
            return os.path.join(current_path, directories[selected_index])
        elif key == 27:  # Escape key
            return None

def display_progress(stdscr, progress, total, y_pos=5):
    """Display a progress bar in the terminal."""
    bar_width = 50
    progress_bar = int((progress / total) * bar_width)
    progress_str = f"[{'#' * progress_bar}{'.' * (bar_width - progress_bar)}] {progress}/{total}"
    stdscr.addstr(y_pos, 0, progress_str)
    stdscr.refresh()

def start_duplication_removal(stdscr):
    """Start the file duplication removal process and show progress."""
    directory = navigate_directories(stdscr)

    if not directory or not os.path.isdir(directory):
        display_message(stdscr, "Invalid directory path.", 0, 4)
        return
    
    display_message(stdscr, f"Scanning directory {directory}...", 0, 4)
    stdscr.refresh()
    logger.info(f"Scanning directory: {directory}")

    files = get_files_in_directory(directory)
    checksum_dict = organize_files_by_checksum(files)
    total_files = sum(len(group) for group in checksum_dict.values())
    files_processed = 0
    duplicates_removed = 0

    for checksum, file_group in checksum_dict.items():
        if len(file_group) > 1:
            for file in file_group[1:]:
                os.remove(file)  # Remove the duplicate file
                duplicates_removed += 1
                files_processed += 1
                display_progress(stdscr, files_processed, total_files)
                logger.info(f"Removed duplicate: {file}")
    
    display_message(stdscr, f"Total duplicates removed: {duplicates_removed}", 0, 7)
    logger.info(f"Total duplicates removed: {duplicates_removed}")
    stdscr.refresh()
    stdscr.getch()

def main_menu(stdscr):
    """Display the main menu and navigate between options."""
    curses.curs_set(0)  # Hide the cursor
    stdscr.clear()  # Clear the screen

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "===== Data Duplication Removal ====")
        stdscr.addstr(2, 0, "1. Start Duplication Removal")
        stdscr.addstr(3, 0, "2. View Logs (Not Implemented)")
        stdscr.addstr(4, 0, "3. Exit")
        
        stdscr.addstr(6, 0, "Select an option (1-3): ")
        stdscr.refresh()

        key = stdscr.getch()  # Wait for user input
        
        if key == ord('1'):  # Start Duplication Removal
            start_duplication_removal(stdscr)
        elif key == ord('2'):  # View Logs
            display_message(stdscr, "Log functionality not implemented.", 0, 6)
            stdscr.getch()
        elif key == ord('3'):  # Exit
            break

if __name__ == "__main__":
    curses.wrapper(main_menu)
