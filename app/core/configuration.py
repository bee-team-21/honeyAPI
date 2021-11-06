import os


APP_VERSION = os.getenv("APP_VERSION", "0.1.0")
APP_GOOGLE_CLIENT_ID = os.getenv("APP_GOOGLE_CLIENT_ID", "")
APP_GOOGLE_CLIENT_SECRET = os.getenv("APP_GOOGLE_CLIENT_SECRET", "")
APP_API_KEY_NAME = os.getenv("APP_API_KEY_NAME", "Authorization")
APP_STATIC_SECRET = os.getenv("APP_STATIC_SECRET", "43e36b7672fadda3df4b158f414ce2b41d2dbb24b639727a1352760bf6133e73")
APP_SECRET_KEY_MIDDLEWARE = os.getenv("APP_SECRET_KEY_MIDDLEWARE", "")
APP_MONGO_DB = os.getenv("APP_MONGO_DB", "db")
APP_MONGO_URI = os.getenv("APP_MONGO_URI", "mongodb://user:password@localhost/db")
APP_TITLE = os.getenv("APP_TITLE",  "App Notify")
APP_DESCRIPTION = os.getenv("APP_DESCRIPTION", "API base to login Bearer using Oauth2 Google")
APP_LANG = os.getenv("APP_LANG", "es.json")
APP_TIME_OFFSET_FIRING = int(os.getenv("APP_TIME_OFFSET_FIRING", "10"))
APP_TIME_OFFSET_RESOLVED = int(os.getenv("APP_TIME_OFFSET_RESOLVED", "5"))
APP_CLICKATELL_URL = os.getenv("APP_CLICKATELL_URL", "https://api.clickatell.com/rest/message")
APP_CLICKATELL_TOKEN = os.getenv("APP_CLICKATELL_TOKEN", "TOKEN")
APP_GRAFANA_TOKEN = os.getenv("APP_GRAFANA_TOKEN", "TOKEN")
APP_ENABLE_SAVE_IMAGES = os.getenv("APP_ENABLE_SAVE_IMAGES", "true") == "true"
APP_CHAT_API_INSTANCE = os.getenv("APP_CHAT_API_INSTANCE", "https://api.chat-api.com/instance1234")
APP_CHAT_API_TOKEN = os.getenv("APP_CHAT_API_TOKEN", "TOKEN")
APP_TELEGRAM_TOKEN = os.getenv("APP_TELEGRAM_TOKEN", "TOKEN")
APP_VERIFY_SSL_IMAGE = os.getenv("APP_VERIFY_SSL_IMAGE", "false") == "true"
APP_TIME_OUT_DOWNLOAD = float(os.getenv("APP_TIME_OUT_DOWNLOAD", "30"))