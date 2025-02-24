import os
import glob
from datetime import datetime
import shutil


def ensure_directory(directory):
    """Ensure the specified directory exists."""
    os.makedirs(directory, exist_ok=True)


def get_timestamp():
    """Return current timestamp in YYYYMMDD_HHMMSS format."""
    return datetime.now().strftime("%Y%mDD_%H%M%S")  # Note: Use %Y%m%d if desired


def timestamped_path(directory, prefix, extension):
    """
    Return a path inside the specified directory with a given prefix, current timestamp, and file extension.
    """
    ensure_directory(directory)
    return os.path.join(directory, f"{prefix}_{get_timestamp()}.{extension}")


def write_file(file_path, content):
    """Write the provided content to the file at file_path."""
    ensure_directory(os.path.dirname(file_path))
    with open(file_path, "w") as f:
        f.write(content)


def read_file(file_path):
    """Return the content of the file at file_path."""
    with open(file_path, "r") as f:
        return f.read()


def read_latest_file(directory, pattern):
    """
    Read the content of the latest file in the given directory that matches the pattern.
    Returns an empty string if no file is found.
    """
    files = glob.glob(os.path.join(directory, pattern))
    if not files:
        return ""
    latest_file = max(files, key=os.path.getctime)
    try:
        return read_file(latest_file)
    except FileNotFoundError:
        return ""


def write_timestamped_file(directory, prefix, extension, content):
    """
    Write the provided content to a timestamped file in the specified directory,
    using the given prefix and file extension.
    """
    file_path = timestamped_path(directory, prefix, extension)
    write_file(file_path, content)


def read_code():
    """
    Read the content of the most recent generated code file from the 'files' directory
    with prefix 'code_for_riza'.
    """
    return read_latest_file("files", "code_for_riza*.py")


def write_code(content):
    """Write the provided code to a timestamped file in the 'files' directory with prefix 'code_for_riza' and .py extension."""
    write_timestamped_file("files", "code_for_riza", "py", content)


def write_review_comments(review):
    """Write the provided review comments to a timestamped file in the 'files' directory with prefix 'review_for_riza' and .txt extension."""
    write_timestamped_file("files", "review_for_riza", "txt", review)


def write_execution_output(output):
    """Write the provided execution output to a timestamped file in the 'files' directory with prefix 'execution_output' and .txt extension."""
    write_timestamped_file("files", "execution_output", "txt", output)


def clear_files_directory():
    """
    Clears all files and directories in the specified directory.
    """
    directory = "files"
    if os.path.exists(directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
