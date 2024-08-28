# Christine Oladapo

# ds_client.py


"""
This module provides functions to interact with the ICS 32 DS server
for sending messages and updating user bio.
"""

import socket
from ds_protocol import join_command, post_command, bio_command


def send(server: str, port: int, username: str, password: str, message: str, bio: str = None) -> bool:
    '''
    The send function joins a ds server and sends a message, bio, or both

    :param server: The ip address for the ICS 32 DS server.
    :param port: The port where the ICS 32 DS server is accepting connections.
    :param username: The user name to be assigned to the message.
    :param password: The password associated with the username.
    :param message: The message to be sent to the server.
    :param bio: Optional, a bio for the user.
    :return: True if the operation was successful, False otherwise.
    '''
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((server, port))
            send_file = client.makefile('w')
            recv_file = client.makefile('r')
            token = join_command(username, password, send_file, recv_file)
            post_command(token, message, send_file, recv_file)
            if bio is not None:
                bio_command(token, bio, send_file, recv_file)

            return True

    except ConnectionRefusedError:
        print("Connection unsuccessful")
        return False
    except socket.timeout:
        print("Socket operation timed out")
        return False
    except socket.error as e:
        print(f"Socket error: {e}")
        return False
