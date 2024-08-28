# Christine Oladapo

# ds_protocol.py


"""
ds_protocol.py
"""

import json
from collections import namedtuple
import time
import socket

DataTuple = namedtuple('DataTuple', ['type', 'message', 'token'])


def extract_json(json_msg: str) -> DataTuple:
    '''
    Call the json.loads function on a json string and convert
    it to a DataTuple object
    '''
    try:
        json_obj = json.loads(json_msg)
        response = json_obj['response']
        return DataTuple(response['type'], response['message'], response.get('token', ''))
    except json.JSONDecodeError:
        print("Json cannot be decoded.")


def join_command(username, password, send, recv):
    """
    Join a server with the provided username and password.

    Args:
        username (str): The username for joining the server.
        password (str): The password for joining the server.
        send (socket.socket): The socket for sending data.
        recv (socket.socket): The socket for receiving data.

    Returns:
        str: The token received upon successful
        join, or None if there's an error.
    """
    join_msg = {"join": {"username": username, "password": password, "token": ""}}
    join_json = json.dumps(join_msg)

    send.write(join_json + '\r\n')
    send.flush()

    resp = recv.readline()
    socket_response = extract_json(resp)
    if socket_response.type == "ok":
        return socket_response.token
    else:
        print(f"Error joining server: {socket_response.message}")
        return None


def post_command(token, message, send, recv, time_default=time.time()):
    """
    Post a message to the server with the provided token.

    Args:
        token (str): The token for authorization.
        message (str): The message to post.
        send (socket.socket): The socket for sending data.
        recv (socket.socket): The socket for receiving data.
        time_default (float, optional): The timestamp
        for the post. Defaults to current time.

    Returns:
        bool: True if the message is successfully posted, False otherwise.
    """
    try:
        if not message.strip():
            print("Error: Post cannot be empty or contain only whitespace. Did NOT publish")
            return False

        post_method = {"token": token, "post": {"entry": message, "timestamp": time_default}}
        json_object = json.dumps(post_method, indent=0)

        send.write(json_object + '\r\n')
        send.flush()

        resp = recv.readline()
        extract_json(resp)

    except (json.JSONDecodeError, socket.error) as e:
        print(f"Error during communication: {e}")
        return False


def bio_command(token, bio, send, recv):
    """
    Update user's bio on the server with the provided token.

    Args:
        token (str): The token for authorization.
        bio (str): The new bio content.
        send (socket.socket): The socket for sending data.
        recv (socket.socket): The socket for receiving data.

    Returns:
        bool: True if the bio is successfully updated, False otherwise.
    """
    if not bio.strip():
        print("Error: Bio cannot be empty or contain only whitespace. Did NOT publish")
        return False

    bio_msg = {"token": token, "bio": {"entry": bio, "timestamp": time.time()}}
    send.write(json.dumps(bio_msg) + '\r\n')
    send.flush()

    resp = recv.readline()
    handle_response(resp)


def handle_response(recv):
    """
    Handle the response received from the server.

    Args:
        recv (socket.socket): The socket for receiving data.

    Returns:
        None
    """
    socket_response = extract_json(recv)
    if socket_response.type == 'ok':
        print("Bio sent successfully")
    elif socket_response.type == 'error':
        print(f"Error: {socket_response.message}")
