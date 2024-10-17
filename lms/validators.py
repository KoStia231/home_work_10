import re

from rest_framework import serializers


class YouTubeURLValidator:
    """
    Валидатор для проверки, что ссылка ведет только на YouTube.
    """

    def __init__(self, field):
        self.field = field

    def __call__(self, data):
        youtube_regex = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.+'
        url = data.get(self.field)
        if url and not re.match(youtube_regex, url):
            raise serializers.ValidationError(f'Поле {self.field} должно содержать ссылку только на YouTube.')
