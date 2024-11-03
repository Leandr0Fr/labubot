import os

# Gemini
SECRET_KEY = os.getenv("APIKEY")

# CV
CV = os.getenv("CV")

# Keywords
_KEYWORDS = os.getenv("KEYWORDS")
KEYWORDS = _KEYWORDS.split(",")

# Linkedin credentials
EMAIL = os.getenv("LINKEDIN_EMAIL")
PSW = os.getenv("LINKEDIN_PSW")
