from os import environ 

class Config:
    API_ID = int(environ.get("API_ID", "")) # Add all env variables in deployment server
    API_HASH = environ.get("API_HASH", "") # Add all env variables in deployment server
    BOT_TOKEN = environ.get("BOT_TOKEN", "") # Add all env variables in deployment server
    BOT_SESSION = environ.get("BOT_SESSION", "vjbot")  # Add all env variables in deployment server
    DATABASE_URI = environ.get("DATABASE_URI", "") # Add all env variables in deployment server
    DATABASE_NAME = environ.get("DATABASE_NAME", "vj-forward-bot") # Add all env variables in deployment server
    BOT_OWNER = int(environ.get("BOT_OWNER", "")) # Add all env variables in deployment server

# Add all env variables in deployment server

class temp(object): 
    lock = {}
    CANCEL = {}
    forwardings = 0
    BANNED_USERS = []
    IS_FRWD_CHAT = []
