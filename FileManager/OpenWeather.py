"""
This module provides a class, OpenWeather, which is used for accessing weather data
from the OpenWeatherMap API.
"""
# openweather.py


# Christine Oladapo

import urllib
import json
from WebAPI import WebAPI

class OpenWeather(WebAPI):
    """
    Represents a class for accessing weather data from the OpenWeather API.
    """
    def __init__(self, zipcode: str = "92697", ccode: str = "US") -> None:
        super().__init__()
        self.zipcode = zipcode
        self.ccode = ccode
        self.temperature = None
        self.high_temperature = None
        self.low_temperature = None
        self.longitude = None
        self.latitude = None
        self.description = None
        self.humidity = None
        self.sunset = None
        self.city = None


    def load_data(self) -> None:
        '''
        Calls the web api using the required values and stores
        the response in class data attributes.
        '''
        response = None  # Initialize response outside of try block
        if self.apikey is None:
            raise ValueError("API key is not set. Please set the API key using set_apikey method.")

        url = f"http://api.openweathermap.org/data/2.5/weather?zip={self.zipcode},{self.ccode}&appid={self.apikey}"

        try:
            weather_data = self._download_url(url)
            if weather_data is None:
                raise ValueError("Failed to fetch weather data. API key may be invalid or unauthorized.")
            # Extract relevant data
            self.temperature = weather_data['main']['temp']
            self.high_temperature = weather_data['main']['temp_max']
            self.low_temperature = weather_data['main']['temp_min']
            self.longitude = weather_data['coord']['lon']
            self.latitude = weather_data['coord']['lat']
            self.description = weather_data['weather'][0]['description']
            self.humidity = weather_data['main']['humidity']
            self.sunset = weather_data['sys']['sunset']
            self.city = weather_data['name']

        except urllib.error.HTTPError as e:
            if e.code == 404:
                print("The requested resource was not found (404). Please check the URL.")
            elif e.code == 503:
                print("The service is temporarily unavailable (503). Please try again later.")
            elif e.code == 401:
                raise ValueError("Unauthorized access. Please check your API key.") from e
            else:
                print(f"Failed to download contents of URL. Status code: {e.code}")
        except urllib.error.URLError as e:
            print(f"Failed to establish a connection to the server: {e.reason}")
        except json.JSONDecodeError:
            print("Invalid data formatting from the remote API.")
        finally:
            if response is not None:
                response.close()


    def transclude(self, message: str) -> str:
        """
        Replaces keywords in a message with associated weather data.
        :param message: The message to transclude
        :return: The transcluded message
        """
        # Check if @weather keyword is present in the message
        if "@weather" in message:
            # Load weather data
            self.load_data()
            # Replace @weather keyword with weather description
            message = message.replace("@weather", self.description)

        return message

