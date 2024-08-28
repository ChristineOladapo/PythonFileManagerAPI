
# Christine Oladapo

# ui.py

# A module responsible for
# processing all commands in the official input command format (see next item).

from pathlib import Path
from Profile import Profile, Post
from ds_client import send
from OpenWeather import OpenWeather
from LastFM import LastFM
import WebAPI
import os
from dotenv import load_dotenv

load_dotenv()
# Get API key from environment variable
OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")
LAST_FM_API_KEY = os.getenv("LAST_FM_API_KEY")

PORT_NUMBER = 3021
admin = False
main_path = ""


def main():
    """
    Main function to handle user interactions and process commands.

    Displays an introduction, prompts for user input,
    and loops until the user quits the program.
    Calls different functions based on the user's input.

    Args:
        None

    Returns:
        None
    """
    global admin
    user_choice = display_intro()
    if user_choice.upper() == "ADMIN":
        admin = True
        user_input = input()
    else:
        # only going to have one command if not in admin mode
        user_input = user_choice
    while user_input.upper() != "Q":
        if admin is True:
            handle_commands(user_input)
        else:
            user_friendly_mode(user_input)
        if admin is True:
            user_input = input()
        else:
            user_input = input("Please enter command L, C, D, R, O, E, P, PUBLISH(to post to server) or Q(quit program): ")


def user_friendly_mode(user_input):
    """
    Process user input in user-friendly mode.

    Args:
        user_input (str): User input command.

    Returns:
        None
    """
    user_input = user_input.strip()
    if user_input.upper() == "E":
        print_edit_options()
        additional_input = input("Enter additional option(s): ")
        all_user_info = user_input + " " + additional_input
        handle_commands(all_user_info)
    elif user_input.upper() == "P":
        print_print_options()
        additional_input = input("Enter additional option(s): ")
        all_user_info = f"{user_input} {additional_input}"
        handle_commands(all_user_info)
    elif user_input.upper() == "C":
        directory = input("Please enter your directory path: ")
        file_name = input("Please enter file name with no spaces: ")
        all_user_info = f"{user_input} {directory} -n {file_name}"
        handle_commands(all_user_info)
    elif user_input.upper() == "D":
        user_path = input("Please enter the file path you want to delete: ")
        all_user_info = f"{user_input} {user_path}"
        handle_commands(all_user_info)
    elif user_input.upper() == "R":
        user_path = input("Please enter the file path you want to read from: ")
        all_user_info = f"{user_input} {user_path}"
        handle_commands(all_user_info)
    elif user_input.upper() == "O":
        user_path = input("Please enter the file path you want to load: ")
        all_user_info = f"{user_input} {user_path}"
        handle_commands(all_user_info)
    elif user_input.upper() == "L":
        user_path = input("Please enter the directory path you want to list contents from: ")
        print_list_options()
        additional_input = input("Enter additional option(s) if none press ENTER: ")
        all_user_info = f"{user_input} {user_path} {additional_input}"
        handle_commands(all_user_info)
    elif user_input.upper() == "PUBLISH":
        collect_publish_command_info()
    elif user_input.upper() == "ADMIN":
        global admin
        admin = True
        return
    else:
        print("ERROR")


def handle_commands(user_input):
    """
    Process user commands.

    Args:
        user_input (str): User input command.

    Returns:
        None
    """
    global main_path
    if len(user_input) < 2 or user_input == "":
        print("ERROR")
    else:
        split_input = user_input.split()
        command1 = split_input[0]
        if command1.upper() == "E":
            edit_dsu_file(user_input, main_path)
        elif command1.upper() == "P":
            print_profile_data(user_input, main_path)
        # new code
        elif command1.upper() == "PUBLISH":
            collect_publish_command_info()
        else:
            main_path = Path(split_input[1])
            if " -f" in user_input and " -r" in user_input:
                printFilesRecursively(main_path)
            elif " -s " in user_input and " -r" in user_input:
                file_name = split_input[4]
                main_path2 = main_path / file_name
                printFileNameRecursively(main_path, file_name)
            elif " -e " in user_input and " -r" in user_input:
                file_extension = split_input[4]
                printFileExtensionRecursively(main_path, file_extension)
            elif " -f" in user_input:
                printFiles(main_path)
            elif " -r" in user_input:
                printContentRecursively(main_path)
            elif " -s " in user_input:
                file_name = split_input[3]
                main_path2 = main_path / file_name
                printMatchingFile(main_path, main_path2)
            elif " -e " in user_input:
                file_extension = split_input[3]
                printWithFileExtension(main_path, file_extension)
            elif command1.upper() == "C" and " -n" in user_input:
                name_of_file = split_input[3]
                main_path = create_new_file(main_path, name_of_file)
            elif command1.upper() == "D":
                delete_dsu_specified_file(main_path)
            elif command1.upper() == "R":
                if read_file_contents(main_path) is False:
                    user_input = input()
            elif command1.upper() == "O":
                load_existing_dsu_file(main_path)
            # not sure if this should go here
            elif command1.upper() == "ADMIN":
                admin = True
            elif command1.upper() == "L":
                listDirectories(main_path)
            else:
                print("ERROR")


def listDirectories(p):
    """
    List directories in a given path.

    Args:
        p (Path): Path to list directories from.

    Returns:
        None
    """
    directories = []
    if p.exists() is False:
        # what is the path is a file
        return False
    for element in p.iterdir():
        if element.is_file():
            print(element)
        else:
            directories.append(element)
    for subdirectory in directories:
        print(subdirectory)


def printFiles(p):
    """
    Print the files present in the specified directory.

    Args:
        p (Path): The path to the directory.

    Returns:
        None
    """
    for element in p.iterdir():
        if element.is_file():
            print(element)


def printContentRecursively(p):
    """
    Print the contents of directories recursively.

    Args:
        p (Path): The path to the directory.

    Returns:
        None
    """
    directories = []
    if p.exists() is False:
        # what if the path is a file
        return False
    # new code from assignment3
    if p.is_file():
        print("Please enter a directory path, Try again")
        return
    for element in p.iterdir():
        if element.is_file():
            print(element)
        else:
            directories.append(element)
    for subdirectory in directories:
        print(subdirectory)
        printContentRecursively(subdirectory)


def printFilesRecursively(p):
    """
    Print the files present in directories recursively.

    Args:
        p (Path): The path to the directory.

    Returns:
        None
    """
    for file_name in p.iterdir():
        if file_name.is_file() is True:
            print(file_name)
        else:
            printFilesRecursively(file_name)


def printMatchingFile(p, p2):
    """
    Print a file if it matches the specified file path.

    Args:
        p (Path): The path to the directory.
        p2 (Path): The file path to match.

    Returns:
        None
    """
    for file1 in p.iterdir():
        if file1.is_file() and file1 == p2:
            print(p2)


def printFileNameRecursively(p, file_name):
    """
    Print the file names recursively.

    Args:
        p (Path): The path to the directory.
        file_name (str): The name of the file.

    Returns:
        None
    """
    p2 = p / file_name
    for element in p.iterdir():
        if element.is_file() and element == p2:
            print(p2)
        else:
            if element.is_dir():
                printFileNameRecursively(element, file_name)


def printWithFileExtension(p, file_extension_name):
    """
    Print files with a specified file extension.

    Args:
        p (Path): The path to the directory.
        file_extension_name (str): The file extension.

    Returns:
        None
    """
    for element in p.iterdir():
        if element.is_file() and "." + file_extension_name == element.suffix:
            print(element)


def printFileExtensionRecursively(p, file_extension_name):
    """
    Print files with a specified file extension recursively.

    Args:
        p (Path): The path to the directory.
        file_extension_name (str): The file extension.

    Returns:
        None
    """
    for element in p.iterdir():
        if element.is_file() and element.suffix == "." + file_extension_name:
            print(element)
        else:
            if element.is_dir():
                printFileExtensionRecursively(element, file_extension_name)


def create_new_file(p, filename):
    """
    Create a new file with the specified name.

    Args:
        p (Path): The path to the directory.
        filename (str): The name of the new file.

    Returns:
        Path: The path to the new file.
    """
    try:
        new_file_path = p / filename
        new_file_path = new_file_path.with_suffix(".dsu")
        if new_file_path.exists():
            print(f"{filename} already exists. Loading file...")
            load_existing_dsu_file(new_file_path)
            return
        # could maybe add code to check if the path is a directory and not a file
        if admin is False:
            input_username = input("Enter username: ")
            input_password = input("Enter password: ")
            input_bio = input("Enter bio: ")
            # new code
            input_server = input("Enter the server you want to publish to:  ")
            # Check if the input is empty or contains only whitespace
            while not input_server.strip():
                print("Server cannot be empty. Please enter a valid server.")
                input_server = input("Enter the server you want to publish to: ")
        else:
            input_username = input()
            input_password = input()
            input_bio = input()
            print("Enter the server you want to publish to:  ")
            input_server = input()
            while not input_server.strip():
                print("Server cannot be empty. Please enter a valid server.")
                input_server = input()
        with open(new_file_path, "a+") as opened_file:
            # Create Profile object
            profile_info = Profile(input_server, input_username, input_password)
            # Set bio attribute to the value collected from user input
            profile_info.bio = input_bio
            # Save profile to the file
            profile_info.save_profile(str(new_file_path))
            print(f"Profile created and saved to: {new_file_path}")
        return new_file_path
    except Exception as e:
        print(f"Error creating file: {e}")


def delete_dsu_specified_file(p):
    """
    Delete a specified DSU file.

    Args:
        p (Path): The path to the DSU file.

    Returns:
        None
    """
    try:
        if p.suffix != ".dsu":
            print("ERROR, does not end in '.dsu")
            return
        # don't know if this is needed
        elif p.is_dir():
            print(f"{p} is a directory, please enter a file path")
        else:
            p.unlink()
            string_path = f"{p}" + " DELETED"
            print(string_path)
    except FileNotFoundError:
        print(f"File '{p}' not found.")
    except Exception as e:
        print(f"Error deleting file: {e}")


def read_file_contents(p):
    """
    Read the contents of a DSU file.

    Args:
        p (Path): The path to the DSU file.

    Returns:
        None
    """
    if p.suffix != ".dsu":
        print("ERROR, does not end in '.dsu'")
        return
    else:
        try:
            with open(p, "r") as file1:
                file1 = file1.read()
                if len(file1) == 0:
                    print("EMPTY")
                    return
                file1 = file1.split()
                file1 = " ".join(file1)
                for line in file1.split("\n"):
                    print(line)

        except FileNotFoundError:
            print(f"File {p} not found.")
        except Exception as e:
            print(f"Error reading file: {e}")


def load_existing_dsu_file(p):
    """
    Load an existing DSU file.

    Args:
        p (Path): The path to the DSU file.

    Returns:
        None
    """
    try:
        if p.suffix != ".dsu":
            print("ERROR, does not end in '.dsu'")
            return
        else:
            user_profile = Profile()
            user_profile.load_profile(p)
            print("DSU file loaded successfully.")
            print(f"Username: {user_profile.username}")
            print("Password: ", "*" * len(user_profile.password))
            print(f"Bio: {user_profile.bio}")
            print(f"DSU Server: {user_profile.dsuserver}")
        # If the user attempts to load a file that is not
        # in a valid DSU file format, this should result in an error
    except FileNotFoundError:
        print("File does not exist")
    except Exception as ex:
        print(f"Unexpected error: {ex}")


def edit_dsu_file(user_info, p):
    """
    Edit a DSU file.

    Args:
        user_info (str): Information to edit.
        p (Path): The path to the DSU file.

    Returns:
        None
    """
    try:
        user_profile = Profile()
        user_profile.load_profile(p)
        if "-usr" in user_info:
            # Split the user_info string by "-usr"
            # to separate the command option and its argument
            updated_user_info = user_info.split("-usr")
            # to be used because the input won't always be a single word
            first_element_after_option = updated_user_info[1].strip()
            index = 1
            username = ""
            while first_element_after_option[index] != '"' and first_element_after_option[index] != "'":
                username += first_element_after_option[index]
                index += 1
            username = username.replace(" ", "")
            if len(username) == 0:
                print("ERROR not a valid username. Username NOT saved")
            else:
                # Update the username in the user profile objec
                user_profile.username = username
                # Save the updated profile to the DSU file
                user_profile.save_profile(p)
        if "-pwd" in user_info:
            updated_user_info = user_info.split("-pwd")
            first_element_after_option = updated_user_info[1].strip()
            index = 1
            password = ""
            while first_element_after_option[index] != '"' and first_element_after_option[index] != "'":
                password += first_element_after_option[index]
                index += 1
            password = password.replace(" ", "")
            if len(password) == 0:
                print("ERROR not a valid password. Password NOT saved")
            else:
                user_profile.password = password
                user_profile.save_profile(p)
        if "-bio" in user_info:
            updated_user_info = user_info.split("-bio")
            first_element_after_option = updated_user_info[1].strip()
            index = 1
            bio = ""
            while first_element_after_option[index] != '"' and first_element_after_option[index]:
                bio += first_element_after_option[index]
                index += 1
            if bio.isspace() is True:
                print("ERROR bio not a valid bio. Bio NOT saved")
            else:
                user_profile.bio = bio
                user_profile.save_profile(p)
        if "-addpost" in user_info:
            updated_user_info = user_info.split("-addpost")
            first_element_after_option = updated_user_info[1].strip()
            index = 1
            new_post_content = ""
            while first_element_after_option[index] != '"' and first_element_after_option[index] != "'":
                new_post_content += first_element_after_option[index]
                index += 1
            if new_post_content.isspace() is True:
                print("ERROR can't add an empty post. Post NOT saved")
            else:
                #  New Post object with the new post content
                if "@weather" in new_post_content:
                    # Prompt the user to configure weather settings
                    user_zipcode, user_apikey = configure_weather_settings()

                    # Create an instance of OpenWeather with customized
                    # settings
                    open_weather = OpenWeather(zipcode=user_zipcode)
                    open_weather.set_apikey(user_apikey)
                    new_post_content = open_weather.transclude(new_post_content)

                if "@lastfm" in new_post_content:
                    # Prompt the user to configure LastFM settings
                    user_apikey, artist_name = configure_lastfm_settings()

                    # Create an instance of LastFM with customized settings
                    lastfm_instance = LastFM()
                    lastfm_instance.set_apikey(user_apikey)

                    if artist_name:
                        # Transclude @lastfm keyword with user-provided
                        # artist name
                        new_post_content = lastfm_instance.transclude(new_post_content, artist=artist_name)
                    else:
                        print("Artist name not provided. @lastfm keyword will not be transcluded.")

            # Check if the post content is empty after transcluding
            if new_post_content.isspace() or not new_post_content.strip():
                print("ERROR: Can't add an empty post. Post NOT saved")
            else:
                new_post = Post(new_post_content)
                # Adding the new post to the user profile object
                user_profile.add_post(new_post)
                user_profile.save_profile(p)
        if "-delpost" in user_info:
            split_user_info = user_info.split()
            find_int_index = split_user_info.index("-delpost") + 1
            post_id_str = split_user_info[find_int_index].strip()
            # Convert the extracted string to an integer
            post_id = int(post_id_str) - 1
            # Check if the post_id is valid
            posts = user_profile.get_posts()
            if 0 <= post_id < len(posts):
                user_profile.del_post(post_id)  # Delete the post
                user_profile.save_profile(p)
    except Exception as e:
        print(f"Error editing DSU file: {e}")


def print_profile_data(user_info, p):
    """
    Print profile data from a DSU file.

    Args:
        user_info (str): Information to print.
        p (Path): The path to the DSU file.

    Returns:
        None
    """
    try:
        user_profile = Profile()
        user_profile.load_profile(p)
        if "-usr" in user_info:
            print(f"Username: {user_profile.username}")

        if "-pwd" in user_info:
            print(f"Password: {user_profile.password}")

        if "-bio" in user_info:
            print(f"Bio: {user_profile.bio}")

        if "-posts" in user_info:
            posts = user_profile.get_posts()
            if len(posts) > 0:
                for i, post in enumerate(posts):
                    print(f"Post {i + 1}: {post.get_entry()}")
            else:
                print("No posts available.")

        if "-all" in user_info:
            print(f"Username: {user_profile.username}")
            print(f"Password: {user_profile.password}")
            print(f"Bio: {user_profile.bio}")
            print("Posts:")
            posts = user_profile.get_posts()
            for i, post in enumerate(posts):
                print(f"Posts {i + 1}: {post.get_entry()}")

        if "-post" in user_info.split():
            split_user_info = user_info.split()
            find_int_index = split_user_info.index("-post") + 1
            post_id_str = split_user_info[find_int_index].strip()
            post_id = int(post_id_str)
            posts = user_profile.get_posts()
            if 1 <= post_id <= len(posts):
                print(f"Post {post_id}: {posts[post_id - 1].get_entry()}")
            else:
                print("Invalid post ID.")

    except Exception as e:
        print(f"An error occurred: {e}")


def display_intro():
    """
    Display the introductory message.

    Returns:
        str: The mode selected by the user.
    """
    print("Welcome to the DSU File Manager!")
    print("Available commands:")
    print("C - Create a new DSU file")
    print("L - List files in directory")
    print("D - Delete a specified file")
    print("R - Read file contents")
    print("E - Edit DSU file")
    print("P - Print profile data")
    print("O - Open an existing DSU file")
    print("Q - Quit the program")
    mode = input("Create or load DSU file (C: create, O: load): ")
    return mode


def print_edit_options():
    """
    Print the edit options.

    Returns:
        None
    """
    print("Edit options (can do one or more options):")
    print("Example: -usr [username] -pwd [password] -bio [bio] -addpost [NEWPOST] -delpost [id]")
    print("-usr: Edit username")
    print("-pwd: Edit password")
    print("-bio: Edit bio")
    print("-addpost: Add a new post")
    print("-delpost <post_id>#: Delete a post by specifying the post #")
    # Print information about available keywords
    print("\nAvailable keywords for new posts:")
    print("@weather: Inserts the current weather information in Irvine (Unless user changes zipcode)")
    print("@lastfm: Inserts information about a top track by SZA (an artist) unless user changes")


def print_print_options():
    """
    Print the print command options.

    Returns:
        None
    """
    print("Profile options:")
    print("Example: -usr [username] -pwd [password] -bio [bio] -post [id] -posts -all")
    print("-usr: View username.")
    print("-pwd: View password")
    print("-bio: View bio")
    print("-posts: View all posts")
    print("-post <post_id#>: View a specific post")
    print("-all: View all profile information")


def print_list_options():
    """
    Print the list command options.

    Returns:
        None
    """
    print("Options of the 'L' command, press ENTER if you don't want any additional options")
    print("example: [[-]OPTION] [INPUT]")
    print("-r: Output directory content recursively.")
    print("-f: Output only files, excluding directories in the results.")
    print("-s: Output only files that match a given file name. Ex: -s filename")
    print("-e: Output only files that match a given file extension. Ex: -e extensionname")


def admin_mode():
    """
    Activate admin mode.

    Returns:
        None
    """
    print("Admin mode activated. Enter 'Q' to exit admin mode.")


def handle_publishing(p, post_id, new_bio=None):
    """
    Publishes a change to bio independent of posts or
    at the same time as a post.

    Args:
        p (str): The file path of the DSU file.
        post_id (int): The ID of the post to publish.
        new_bio (str, optional): The new bio content. Defaults to None.

    Returns:
        None
    """
    try:
        user_profile = Profile()
        user_profile.load_profile(p)
        # first save bio to file also
        if new_bio != None:
            user_profile.bio = new_bio
            user_profile.save_profile(p)
        posts = user_profile.get_posts()
        if 1 <= int(post_id) <= len(posts):
            post_content = posts[post_id - 1].get_entry()
        else:
            print("Post number entered is out of range, could not publish")
            return
        if new_bio:
            user_profile.bio = new_bio
        send(user_profile.dsuserver, PORT_NUMBER, user_profile.username, user_profile.password, post_content, user_profile.bio)
    except Exception as e:
        print("An error occurred while publishing.")
        print(f"Error details: {e}")


def collect_publish_command_info():
    """
    Collects information from the user to publish a change to bio or a post.

    This function prompts the user to enter the file path of the DSU file,
    select a post to publish, and optionally update the bio content.

    Returns:
        None
    """
    print("Please enter the file path you want to read your posts from: ")
    user_path = input()
    new_path = Path(user_path)

    if new_path.is_file() and new_path.suffix == ".dsu":
        # prints all current posts to user
        print("Here are all your current posts:  ")
        print_profile_data("P -posts", new_path)
        print("Which post number would you like to publish? ")
        post_number = input()
        while True:
            try:
                post_number_int = int(post_number)
                break  # Exit the loop if conversion to int succeeds
            except ValueError:
                print("Invalid input. Please enter a valid integer.")
                post_number = input("Which post number would you like to publish? ")

        print("Do you want to publish with a new bio? (y/n): ")
        update_bio_choice = input().lower()
        if update_bio_choice == "y":
            print("Enter your new bio: ")
            new_bio_info = input()
            # check bio if empty
            if not new_bio_info.strip():
                print("Error: Bio cannot be empty or contain only whitespace. Did NOT publish")
                return
        else:
            new_bio_info = None
    else:
        print("Not a valid DSU file path. Enter a new command")
        return

    handle_publishing(user_path, post_number_int, new_bio_info)


def configure_weather_settings():
    """
    Configure settings for accessing weather data.

    Asks the user if they want to change the U.S. zip code
    of the weather region and provide their own OpenWeather API key.
    """
    try:
        print("Would you like to change the U.S. zip code of the weather region? (y/n)")
        user_zipcode_choice = input().lower()
 
        if user_zipcode_choice == "y":
            user_zipcode = input("Enter a 5-digit zipcode: ")
            if not user_zipcode.strip().isdigit() or len(user_zipcode.strip()) != 5:
                print("Error: Invalid zipcode. DEFAULT zipcode (Irvine) used.")
                user_zipcode = "92697"
        else:
            user_zipcode = "92697"

        print("Would you like to provide your own OpenWeather API key? (y/n)")
        user_apikey_choice = input().lower()

        if user_apikey_choice == "y":
            user_apikey = input("Enter a valid API key: ")
            if not user_apikey.strip():
                print("Error: API key cannot be empty or contain only whitespace. DEFAULT API key used.")
                user_apikey = OPEN_WEATHER_API_KEY
        else:
            user_apikey = OPEN_WEATHER_API_KEY

        return user_zipcode, user_apikey

    except ValueError as e:
        print(f"Error: {e}. Using default settings.")
        return "92697", OPEN_WEATHER_API_KEY


def configure_lastfm_settings():
    """
    Configure settings for accessing LastFM data.

    Asks the user if they want to provide their own LastFM API key
    and artist for top tracks.
    """
    try:
        print("Would you like to provide your own LastFM API key? (y/n)")
        user_apikey_choice = input().lower()

        if user_apikey_choice == "y":
            user_apikey = input("Enter a valid LastFM API key: ")
            if not user_apikey.strip():
                raise ValueError("API key cannot be empty.")
        else:
            user_apikey = LAST_FM_API_KEY

        print("Would you like to provide your own artist for LastFM top track? (y/n)")
        use_own_artist_choice = input().lower()

        if use_own_artist_choice == "y":
            artist_name = input("Enter the name of the artist for LastFM: ")
            if not artist_name.strip():
                raise ValueError("Artist name cannot be empty. Default artist (SZA) used")
        else:
            artist_name = "SZA"

        return user_apikey, artist_name

    except ValueError as e:
        print(f"Error: {e}. Using default settings.")
        return LAST_FM_API_KEY, "SZA"


if __name__ == "__main__":
    main()
