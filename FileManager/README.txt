Christine Oladapo

Project Overview
This project extends the functionality of a basic file management tool, 
integrating advanced features and APIs to enhance user interaction 
and data management. The application leverages the Python Standard 
Library and additional APIs to provide a robust command-line tool.

Features
Core Functionality
File Management Commands:

L [DIRECTORY] [OPTIONS]: Lists the contents of a directory with various filtering options.
-r: Output directory contents recursively.
-f: Output only files, excluding directories.
-s [NAME]: Output only files that match the specified name.
-e [EXTENSION]: Output only files that match the specified extension.
C [DIRECTORY] -n [NAME]: Creates a new file in the specified directory with a .dsu extension.
D [FILE]: Deletes a .dsu file and confirms deletion.
R [FILE]: Reads and prints the contents of a .dsu file or prints EMPTY if the file is empty.
API Integrations:

Last.fm API: Integrates with the Last.fm API to retrieve and transclude 
track information. The LastFM class includes methods to:
    Retrieve top tracks by a specified artist.
    Replace keywords in messages with Last.fm data.
OpenWeather API: Integrates weather information into the application using the @weather keyword.
    Additional Features:
        Interactive Command Line Interface: The tool interacts with the user through the command line, processing commands and options dynamically.
        Error Handling: The application handles errors gracefully, providing user-friendly messages for incorrect inputs or issues.
Technical Details:
    Python Standard Library: Utilizes pathlib for file manipulation, ensuring
    efficient and effective directory and file operations.
APIs: Implements Last.fm and OpenWeather APIs to enhance functionality beyond standard file operations.
Instructions
    Listing Directory Contents:

        Example: L /path/to/directory -r -f
        Lists all files in the specified directory and its subdirectories.
    Creating a New File:

        Example: C /path/to/directory -n newfile
        Creates a new file named newfile.dsu in the specified directory.
    Deleting a File:

        Example: D /path/to/directory/file.dsu
        Deletes the specified .dsu file.
    Reading a File:

        Example: R /path/to/directory/file.dsu
        Reads and prints the contents of the specified .dsu file or indicates if it is empty.

Getting Started
Dependencies: Ensure you have the necessary API keys and dependencies installed if
you want to use the API features
Running the Application: Run the application (mainfile.py) and use
the command-line interface to interact with the file management and API features.