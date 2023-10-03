# Импортируем нужные библиотеки
import os
from googleapiclient.discovery import build
import isodate
import datetime


class PlayList:
    """
    Инициализация класса PlayList с атрибутами: название плейлиста и ссылка на плейлист
    """
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.title = self.get_playlist_title()
        self.url = "https://www.youtube.com/playlist?list=" + self.playlist_id

    def get_video_stats(self):
        """
        Получение статистику из плейлиста
        """

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in
                                self.get_info_playlist()['items']]
        video_response = self.get_service().videos().list(part='contentDetails,statistics',
                                                          id=','.join(video_ids)
                                                          ).execute()
        return video_response


    @property
    def total_duration(self):
        """
        Получение суммарной длительности плейлиста
        """
        total_time = []
        for video in self.get_video_stats()['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_time.append(duration)
            sum_time = sum(total_time, datetime.timedelta())
        return sum_time

    def get_service(self):
        """
        Получение информации о сервисе
        """
        api_key: str = os.getenv('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def get_info_playlist(self):
        """
        Получение информации о плейлисте
        """
        playlist_videos = self.get_service().playlistItems().list(playlistId=self.playlist_id,
                                                                  part='contentDetails, snippet',
                                                                  maxResults=50,
                                                                  ).execute()
        return playlist_videos

    def get_playlist_title(self):
        """
        Получение названия плейлиста
        """
        channel_id = self.get_info_playlist()["items"][0]["snippet"]["channelId"]
        playlists = self.get_service().playlists().list(channelId=channel_id,
                                                        part='snippet',
                                                        maxResults=50,
                                                        ).execute()
        for playlist in playlists['items']:
            if self.playlist_id == playlist["id"]:
                playlist_title = playlist["snippet"]["title"]
                break
        return playlist_title


    def show_best_video(self):
        """
        Получение ссылки на самое популярное видео из плейлиста (по количеству лайков)
        """
        video_likes = []
        for likes in self.get_video_stats()["items"]:
            video_likes.append(int(likes["statistics"]["likeCount"]))
        max_likes_video = max(video_likes)
        for likes in self.get_video_stats()["items"]:
            if int(likes["statistics"]["likeCount"]) == max_likes_video:
                most_liked_video = "https://youtu.be/" + likes["id"]

        return most_liked_video