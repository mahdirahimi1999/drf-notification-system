from rest_framework.parsers import JSONParser


class PlainTextParser(JSONParser):
    media_type = "text/plain"
