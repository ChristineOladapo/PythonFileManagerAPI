# webapi.py

"""
Code to interact with web API
"""

# Christine Oladapo

from abc import ABC, abstractmethod
import urllib.request
import urllib.error
import json


class WebAPI(ABC):
    """
    Abstract base class for web API interaction.
    """

    def __init__(self):
        self.apikey = None

    def _download_url(self, url: str) -> dict:
        """
        Internal method to download data from a web API.
        """
        try:
            response = urllib.request.urlopen(url)
            data = json.loads(response.read().decode())
            return data
        except urllib.error.HTTPError as e:
            if e.code == 404:
                print("The requested resource was not found (404). Please check the URL.")
            elif e.code == 503:
                print("The service is temporarily unavailable (503). Please try again later.")
            else:
                print(f"Failed to download contents of URL. Status code: {e.code}")
        except urllib.error.URLError as e:
            print(f"Failed to establish a connection to the server: {e.reason}")
        except json.JSONDecodeError:
            print("Invalid data formatting from the remote API.")

    def set_apikey(self, apikey: str) -> None:
        """
        Sets the API key required to make requests to a web API.
        """
        self.apikey = apikey

    @abstractmethod
    def load_data(self):
        """
        Abstract method to load data from the web API.
        """

    @abstractmethod
    def transclude(self, message: str) -> str:
        """
        Abstract method to transclude data into a message.
        """
