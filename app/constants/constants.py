import os

# Gemini
SECRET_KEY = os.getenv("APIKEY")

# CV
CV = os.getenv("CV")

# Keywords
_KEYWORDS = os.getenv("KEYWORDS_SEARCH")
KEYWORDS = _KEYWORDS.split(",")

# Tags
_TAGS = os.getenv("TAGS")
TAGS = _TAGS.split(",")
_TAGS_BANNED = os.getenv("TAGS_BANNED")
TAGS_BANNED = _TAGS_BANNED.split(",")

# Linkedin credentials
EMAIL = os.getenv("LINKEDIN_EMAIL")
PSW = os.getenv("LINKEDIN_PSW")

# Telegram
TELEGRAM_KEY = os.getenv("TOKEN_TELEGRAM")
TELEGRAM_ID = os.getenv("TELEGRAM_USERID")
