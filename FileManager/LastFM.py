# last_fm.py

# Christine Oladapo

"""
Module to interact with the Last.fm API.
"""

import json
import urllib.request
import urllib.error
import random
from WebAPI import WebAPI
import os
from dotenv import load_dotenv


load_dotenv()
# Get API key from environment variable
LAST_FM_API_KEY = os.getenv("LAST_FM_API_KEY")


# URL for the Last.FM API method artist.getTopTracks
api_url = f"http://ws.audioscrobbler.com/2.0/?method=artist.gettoptracks&artist=cher&api_key={LAST_FM_API_KEY}&format=json"


class LastFM(WebAPI):
    """
    Class to interact with the Last.fm API.
    """

    def __init__(self):
        super().__init__()
        self.base_url = "http://ws.audioscrobbler.com/2.0/"


    def load_data(self, artist: str = "SZA", page: int = 1, limit: int = 50) -> dict:
        """
        Retrieves data from Last.fm for the specified artist.

        :param artist: The name of the artist. Defaults to "SZA".
        :param page: The page number to fetch. Defaults to the first page.
        :param limit: The number of results to fetch per page. Defaults to 50.
        :return: A dictionary containing the retrieved data.
        """
        method = "artist.gettoptracks"
        encoded_artist = urllib.parse.quote(artist)
        api_format = "json"
        url = f"{self.base_url}?method={method}&artist={encoded_artist}&api_key={self.apikey}&format={api_format}&page={page}&limit={limit}"
        try:
            data = self._download_url(url)
            return data

        except urllib.error.HTTPError as e:
            print(f"HTTP Error: {e.code} - {e.reason}")
        except urllib.error.URLError as e:
            print(f"URL Error: {e.reason}")
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
        return None


    def get_top_tracks(self, artist: str = "SZA", page=1, limit=50) -> dict:
        """
        Retrieves the top tracks by an artist from Last.fm.

        :param artist: The name of the artist. Defaults to "SZA".
        :param page: The page number to fetch. Defaults to the first page.
        :param limit: The number of results to fetch per page. Defaults to 50.
        :return: A list of dictionaries containing information about the top tracks.
        """

        try:
            data = self.load_data(artist, page, limit)
            if data is not None:
                if 'toptracks' not in data or 'track' not in data['toptracks']:
                    raise ValueError("Invalid data format received from Last.fm")

            tracks = data['toptracks']['track']
            if not tracks:
                raise ValueError("No top tracks found for the artist")
            if len(tracks) < 1:
                raise ValueError("No tracks available for the artist")

            random_index = random.randint(0, len(tracks) - 1)
            return tracks[random_index]

        except ValueError as ve:
            print(ve)


    def transclude(self, message: str, artist: str = "SZA") -> str:
        """
        Replaces keywords in a message with associated LastFM data for the specified artist.

        :param message: The message to transclude.
        :param artist: The name of the artist. Defaults to "SZA".
        :return: The transcluded message.
        """
        # Check if the message contains the keyword "@lastfm"
        if "@lastfm" in message:
            # Get the top track for a specified artist (you need to
            # modify this part based on your implementation)
            top_track_data = self.get_top_tracks(artist)
            if top_track_data:
                # Select the first track from the list
                top_track_data = top_track_data['name']
                # Replace the "@lastfm" keyword with the top track information
                transcluded_message = message.replace("@lastfm", top_track_data)
                return transcluded_message
            else:
                # If no top track data is found, replace "@lastfm" with an error message
                message = message.replace("@lastfm", "No top track data found")
                return message
