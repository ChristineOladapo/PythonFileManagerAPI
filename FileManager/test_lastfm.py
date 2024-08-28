"""
This module contains test cases for the LastFM class.
"""
# Christine Oladapo

# test_lastfm.py

import pytest
from LastFM import LastFM
import os
from dotenv import load_dotenv


load_dotenv()
# Get API key from environment variable
LAST_FM_API_KEY = os.getenv("LAST_FM_API_KEY")

# Fixture to create an instance of the LastFM class for testing


@pytest.fixture
def lastfm_instance():
    """
    Fixture to create an instance of the LastFM class for testing.

    Returns:
        LastFM: An instance of the LastFM class.
    """
    return LastFM()


def test_load_data_success(lastfm_instance):
    """
    Test case to verify successful data retrieval from Last.fm API.
    """
    # Set the API key for testing
    lastfm_instance.set_apikey(LAST_FM_API_KEY)

    # Load data for a specific artist
    data = lastfm_instance.load_data(artist="SZA", page=1, limit=50)

    # Assert that data is not None
    assert data is not None


def test_load_data_invalid_artist(lastfm_instance):
    """
    Test case to verify handling of invalid artist name in load_data method.
    """
    # Set the API key for testing
    lastfm_instance.set_apikey(LAST_FM_API_KEY)

    # Attempt to load data for an invalid artist
    data = lastfm_instance.load_data(artist="InvalidArtistName", page=1, limit=50)

    # Additional assertions to check the error message in the data
    assert 'error' in data
    assert data['error'] == 6
    assert 'message' in data
    assert data['message'] == 'The artist you supplied could not be found'


def test_get_top_tracks_success(lastfm_instance):
    """
    Test case to verify successful retrieval of top tracks for an artist.
    """
    # Set the API key for testing
    lastfm_instance.set_apikey(LAST_FM_API_KEY)

    # Get top tracks for a specific artist
    top_tracks = lastfm_instance.get_top_tracks(artist="SZA", page=1, limit=50)

    # Assert that top_tracks is not None
    assert top_tracks is not None


def test_transclude_success(lastfm_instance):
    """
    Test case to verify successful transclusion of Last.fm data into a message.
    """
    # Set the API key for testing
    lastfm_instance.set_apikey(LAST_FM_API_KEY)

    # Message containing "@lastfm" keyword
    message = "Testing LastFM: @lastfm"

    # Transclude Last.fm data into the message
    transcluded_message = lastfm_instance.transclude(message, artist="SZA")

    # Assert that transcluded_message is not None and contains expected data
    assert transcluded_message is not None
    assert "Testing LastFM: " in transcluded_message


def test_transclude_no_data_found(lastfm_instance):
    """
    Test case to verify transclusion when no Last.fm data is found
    for an artist.
    """
    # Set the API key for testing
    lastfm_instance.set_apikey(LAST_FM_API_KEY)

    # Message containing "@lastfm" keyword
    message = "Testing LastFM: @lastfm"

    # Transclude Last.fm data into the message for an invalid artist
    transcluded_message = lastfm_instance.transclude(message, artist="InvalidArtistName")

    # Assert that transcluded_message contains an error message
    assert "No top track data found" in transcluded_message
