import os


def get_filename(filename):
    """
    Checks if a file exists and returns a unique name by adding a number.

    Args:
        filename (str): The original filename (e.g., 'examplefile.csv').

    Returns:
        str: A unique filename (e.g., 'examplefile1.csv').
    """
    # Split the filename into the base and the extension
    base, extension = os.path.splitext(filename)
    counter = 1

    # Loop until a unique filename is found
    new_filename = filename
    while os.path.exists(new_filename):
        new_filename = f"{base}({counter}){extension}"
        counter += 1

    return new_filename


def create_logging_dir():
    if os.path.exists("./logged_data"):
        return
    else:
        print("Logging directory does not exist, creating now")
        os.mkdir("./logged_data")
    return
