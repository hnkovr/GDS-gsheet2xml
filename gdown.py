# https://chat.openai.com/chat/24b94b6b-0795-43c6-8c24-ef5c29553123

import os
import re
from typing import Optional

import requests

from config import CONFIG
from util import load_key

API_KEY = os.getenv('API_KEY', load_key(CONFIG.YAML, 'API_KEY'))

class GDown:
    """Class for downloading Google Drive files

    This class uses the Google Drive API to download a file from Google Drive.

    Example:
        >>> file_url = 'https://drive.google.com/open?id=1ZfDb563PlFAGgDpBOXtF5247OAfdoUGN'
        >>> gdown = GDown(file_url, API_KEY)
        >>> gdown.download()
        '/content/example_file.txt'
    """

    def __init__(self, file_url: str, api_key: str) -> None:
        """Initialize the class with the Google Drive file URL and API Key

        Args:
            file_url (str): The URL of the Google Drive file to be downloaded.
            api_key (str): The API key for accessing the Google Drive API.
        """
        self.file_url = file_url
        self.file_id = re.search("(?<=id=)[a-zA-Z0-9-_]*", file_url).group(0)

        from googleapiclient.discovery import build
        from googleapiclient import errors
        self.service = build('drive', 'v3', developerKey=api_key)
        self.filename = None

        try:
            file = self.service.files().get(fileId=self.file_id, fields='name').execute()
            self.filename = file['name']
        except errors.HttpError as error:
            print(f'An error occurred: {error}')

    def download(self, filename: Optional[str] = None) -> str:
        """Download the Google Drive file

        Args:
            filename (str, optional): The name to save the downloaded file as. If not provided, the file's original name is used.

        Returns:
            str: The path to the downloaded file.
        """
        if not filename:
            filename = self.filename

        download_url = f'https://drive.google.com/uc?id={self.file_id}'
        response = requests.get(download_url)
        with open(filename, 'wb') as f:
            f.write(response.content)
        return filename


def gdown(file_url: str, *, api_key: str = API_KEY):
    return GDown(file_url, api_key).download()


def demo():
    # Example usage
    file_url = 'https://drive.google.com/open?id=1ZfDb563PlFAGgDpBOXtF5247OAfdoUGN'
    file_path = gdown(file_url)
    if file_path:
        print(f'File is downloaded to: {file_path}')
    else:
        print("Could not download file. Please check your URL and try again.")


if __name__ == '__main__':
    demo()
