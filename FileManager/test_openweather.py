"""
Module for testing the OpenWeather class and its
integration with the OpenWeatherMap API.
"""
# Christine Oladapo

# test_openweather.py

import pytest
from OpenWeather import OpenWeather
import os
from dotenv import load_dotenv


load_dotenv()
# Get API key from environment variable
OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")
# print(f"weatherapi {OPEN_WEATHER_API_KEY}")

# Test case for load_data function
def test_load_data():
    """
    Test case to verify the functionality of the 
    load_data function in the OpenWeather class.
    """
    zipcode = "90210"
    ccode = "US"
    openweather_instance = OpenWeather(zipcode, ccode)
    openweather_instance.set_apikey(OPEN_WEATHER_API_KEY)
    openweather_instance.load_data()
    assert openweather_instance.temperature is not None


# Test case for transclude function
def test_transclude():
    """
    Test case to verify the functionality of the
    transclude function in the OpenWeather class.
    """
    zipcode = "90210"
    ccode = "US"
    openweather_instance = OpenWeather(zipcode, ccode)
    openweather_instance.set_apikey(OPEN_WEATHER_API_KEYs)
    message = "Testing the weather: @weather"
    transcluded_message = openweather_instance.transclude(message)
    assert isinstance(transcluded_message, str)


def test_api():
    """
    Test case to verify the functionality of the OpenWeather API integration.
    """
    # Create an instance of OpenWeather
    openweather_instance = OpenWeather()

    # Set the API key for testing
    openweather_instance.set_apikey(OPEN_WEATHER_API_KEY)

    # Message containing "@weather" keyword
    message = "@weather"

    # Load weather data
    openweather_instance.load_data()

    # Transclude weather information into the message
    result = openweather_instance.transclude(message)

    # Print the transcluded message
    print(result)
