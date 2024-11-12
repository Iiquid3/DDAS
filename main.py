import os
import curses
import shutil
from file_handler import get_files_in_directory, organize_files_by_checksum
from ddas import remove_duplicates
from logger import setup_logger
import send2trash

# Global logger for terminal output
logger = setup_logger()

# Constants for UI layout
HEADER = "===== Data Duplication Removal ===="
FOOTER = "Press any key to return to the menu."

# Utility Functions
def display_message(stdscr, message, x=0, y=0, highlight=False):
    """Display a message with optional highlighting."""
    max_y, max_x = stdscr.getmaxyx()
    if y < max_y:
        try:
            if highlight:
                stdscr.addstr(y, x, message, curses.A_REVERSE)
            else:
                stdscr.addstr(y, x, message)
            stdscr.refresh()
        except curses.error as e:
            logger.error(f"Error displaying message: {message} - {e}")
            display_message(stdscr, "Error displaying message.", 0, 0)
    else:
        logger.error("Message cannot be displayed because the screen is too small.")

def get_deletion_mode(stdscr):
    """Prompt the user to select a deletion mode (trash or permanent)."""
    try:
        stdscr.clear()
        max_y, max_x = stdscr.getmaxyx()
        if max_y >= 12:
            stdscr.addstr(8, 0, "Choose deletion mode:")
            stdscr.addstr(9, 0, "1. Send to Trash")
            stdscr.addstr(10, 0, "2. Permanently Delete")
            stdscr.addstr(12, 0, "Select an option (1-2): ")
            stdscr.refresh()

            while True:
                key = stdscr.getch()
                if key == ord('1'):
                    return "trash"
                elif key == ord('2'):
                    return "permanent"
        else:
            display_message(stdscr, "Terminal window is too small. Please resize.", 0, 0)
    except curses.error as e:
        logger.error(f"Error in get_deletion_mode: {e}")
        display_message(stdscr, "Error occurred in deletion mode selection.", 0, 0)

def list_directories(path):
    """Return a list of directories in the given path."""
    return [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]

def navigate_directories(stdscr):
    """Allow the user to navigate directories and select one."""
    current_path = os.getcwd()
    selected_index = 0

    while True:
        directories = list_directories(current_path)

        stdscr.clear()
        stdscr.addstr(0, 0, f"Current Directory: {current_path}")
        stdscr.addstr(1, 0, "Select a directory using arrow keys, press Enter to choose.")

        max_y, max_x = stdscr.getmaxyx()
        for idx, directory in enumerate(directories):
            if idx == selected_index:
                if idx + 2 < max_y:
                    stdscr.addstr(idx + 2, 0, f"> {directory}", curses.A_REVERSE)
            else:
                if idx + 2 < max_y:
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
    try:
        max_y, max_x = stdscr.getmaxyx()
        if y_pos < max_y:
            bar_width = 50
            progress_bar = int((progress / total) * bar_width)
            progress_str = f"[{'#' * progress_bar}{'.' * (bar_width - progress_bar)}] {progress}/{total}"
            stdscr.addstr(y_pos, 0, progress_str)
            stdscr.refresh()
    except curses.error as e:
        logger.error(f"Error displaying progress: {e}")
        display_message(stdscr, "Error displaying progress.", 0, 0)

# File Handling Functions
def move_to_trash(file_path):
    """Move a file to the trash."""
    try:
        if os.name == 'nt':  # For Windows
            send2trash.send2trash(file_path)
        else:  # For Unix-based systems
            trash_dir = os.path.expanduser('~/.local/share/Trash/files')
            if not os.path.exists(trash_dir):
                os.makedirs(trash_dir)
            shutil.move(file_path, trash_dir)
    except Exception as e:
        logger.error(f"Error sending file to trash: {file_path} - {e}")
        return False
    return True

def start_duplication_removal(stdscr):
    """Start the file duplication removal process and show progress."""
    try:
        directory = navigate_directories(stdscr)

        if not directory or not os.path.isdir(directory):
            display_message(stdscr, "Invalid directory path.", 0, 4)
            return

        # Ask user for deletion mode (display only once)
        deletion_mode = get_deletion_mode(stdscr)
        if deletion_mode == "trash":
            logger.info("User chose to send duplicates to trash.")
        elif deletion_mode == "permanent":
            logger.info("User chose to permanently delete duplicates.")

        display_message(stdscr, f"Scanning directory {directory}...", 0, 4)
        stdscr.refresh()
        logger.info(f"Starting scan of directory: {directory}")

        # Get files and organize by checksum
        files = get_files_in_directory(directory)
        checksum_dict = organize_files_by_checksum(files)

        # Log total files scanned
        total_files = len(files)
        logger.info(f"Total files scanned: {total_files}")

        # Log duplicate removal progress
        total_duplicates_removed = 0
        files_processed = 0

        for checksum, file_group in checksum_dict.items():
            if len(file_group) > 1:
                for file in file_group[1:]:
                    if deletion_mode == "trash":
                        if move_to_trash(file):
                            total_duplicates_removed += 1
                            logger.info(f"Moved duplicate to trash: {file}")
                    elif deletion_mode == "permanent":
                        try:
                            os.remove(file)  # Permanently delete the file
                            total_duplicates_removed += 1
                            logger.info(f"Permanently deleted duplicate: {file}")
                        except Exception as e:
                            logger.error(f"Error deleting file {file}: {e}")
                    files_processed += 1
                    display_progress(stdscr, files_processed, total_files)

        display_message(stdscr, f"Total duplicates removed: {total_duplicates_removed}", 0, 7)
        logger.info(f"Total duplicates removed: {total_duplicates_removed}")
        stdscr.refresh()
        stdscr.getch()
    except Exception as e:
        logger.error(f"Unexpected error during duplication removal: {e}")
        display_message(stdscr, "An unexpected error occurred. Please check logs.", 0, 0)

def view_logs(stdscr):
    """Display log file contents in the terminal."""
    try:
        log_file_path = 'removal_log.txt'

        with open(log_file_path, 'r') as file:
            stdscr.clear()
            stdscr.addstr(0, 0, "===== Log Contents =====")
            lines = file.readlines()
            
            for i, line in enumerate(lines):
                stdscr.addstr(i + 1, 0, line.strip())
                if i >= curses.LINES - 3:
                    stdscr.addstr(i + 2, 0, "-- More lines in the log file --")
                    break

            stdscr.addstr(curses.LINES - 2, 0, "Press any key to return to the menu.")
            stdscr.refresh()
            stdscr.getch()
    except FileNotFoundError:
        logger.error("Log file not found.")
        display_message(stdscr, "Log file not found.", 0, 6)
        stdscr.getch()
    except Exception as e:
        logger.error(f"Error viewing logs: {e}")
        display_message(stdscr, "An error occurred while viewing logs.", 0, 6)
        stdscr.getch()

# Main Menu and Navigation
def main_menu(stdscr):
    """Display the main menu and navigate between options."""
    try:
        curses.curs_set(0)  # Hide the cursor
        stdscr.clear()  # Clear the screen

        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, HEADER)

            # Check terminal height to ensure we stay within bounds
            max_y, max_x = stdscr.getmaxyx()

            if max_y >= 6:
                stdscr.addstr(2, 0, "1. Start Duplication Removal")
            if max_y >= 7:
                stdscr.addstr(3, 0, "2. View Logs")
            if max_y >= 8:
                stdscr.addstr(4, 0, "3. Exit")

            if max_y >= 10:
                stdscr.addstr(6, 0, "Select an option (1-3): ")

            stdscr.refresh()

            key = stdscr.getch()  # Wait for user input

            if key == ord('1'):  # Start Duplication Removal
                start_duplication_removal(stdscr)
            elif key == ord('2'):  # View Logs
                view_logs(stdscr)
            elif key == ord('3'):  # Exit
                break
    except Exception as e:
        logger.error(f"Unexpected error in main menu: {e}")
        display_message(stdscr, "An unexpected error occurred. Please check logs.", 0, 0)
        stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main_menu)
