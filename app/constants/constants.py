import os

SECRET_KEY = os.getenv("APIKEY")

_KEYWORDS = os.getenv("KEYWORDS")
KEYWORDS = _KEYWORDS.split(",")

#Linkedin credentials
EMAIL = os.getenv("LINKEDIN_EMAIL")
PSW = os.getenv("LINKEDIN_PSW")
