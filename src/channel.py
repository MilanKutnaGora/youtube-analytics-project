import json
import os
from pprint import pprint

from googleapiclient.discovery import build
import isodate



api_key: str = os.getenv('API_KEY')
#
# youtube = build('youtube', 'v3', developerKey=api_key)


# channel_id = 'UC-OVMPlMA3-YCIeg4z5z23A'  # MoscowPython
# channel = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
# print(channel)

class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""

        self.__channel_id = channel_id
        youtube = build('youtube', 'v3', developerKey=api_key)
        channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = channel['items'][0]['snippet']['title']
        self.video_count = channel['items'][0]['statistics']['videoCount']
        self.url = "https://www.youtube.com/" + channel['items'][0]['snippet']['customUrl']
        pprint(channel)
        pprint(self.title)
        pprint(self.video_count)
        pprint(self.url)

    @classmethod
    def get_service(cls):
        """ Получение информации о сервисе"""
        api_key: str = os.getenv('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube


    def to_json(self, j_file):
        data = {"channel_id": self.__channel_id,
                "video_count": self.video_count,
                "url": self.url}
        with open(j_file, "w", encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

    @property
    def chanel_id(self):
        return self.__channel_id

if __name__ == '__main__':
    moscowpython = Channel('UC-OVMPlMA3-YCIeg4z5z23A')
    moscowpython.to_json("Moscowpyton.json")






