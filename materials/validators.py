from rest_framework import serializers


class ProhibitedUrlValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        data_url = dict(value).get(self.field)

        if data_url is not None and "https://www.youtube.com/" not in data_url:
            raise serializers.ValidationError("Запрещено использовать ссылки на сторонние ресурсы")
