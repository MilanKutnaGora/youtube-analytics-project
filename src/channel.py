import json
import os
from pprint import pprint

from googleapiclient.discovery import build
import isodate



api_key: str = os.getenv('API_KEY')


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""

        self.__channel_id = channel_id
        youtube = build('youtube', 'v3', developerKey=api_key)
        channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = channel['items'][0]['snippet']['title']
        self.sub_count = channel['items'][0]['statistics']['subscriberCount']
        self.url = "https://www.youtube.com/channel/" + channel_id



    def get_service(self):
        """ Получение информации о сервисе"""
        api_key: str = os.getenv('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def __str__(self):
        return f"{self.title}, ({self.url})"

    def __add__(self, other):
        return int(self.sub_count) + int(other.sub_count)
        # print (moscowpython + highload)

    def __sub__(self, other):
        return int(self.sub_count) - int(other.sub_count)

    def __gt__(self, other):
        return int(self.sub_count) > int(other.sub_count)

    def __ge__(self, other):
        return int(self.sub_count) >= int(other.sub_count)


    @property
    def chanel_id(self):
        return self.__channel_id








