import os

SECRET_KEY = os.getenv("APIKEY")

_KEYWORDS = os.getenv("KEYWORDS")
KEYWORDS = _KEYWORDS.split(",")