from os import environ 

class Config:
    API_ID = int(environ.get("API_ID", "34059790")) # Add all env variables in deployment server
    API_HASH = environ.get("API_HASH", "99f6bded8d3691f3abe6696e96aaae73") # Add all env variables in deployment server
    BOT_TOKEN = environ.get("BOT_TOKEN", "8764331971:AAFIE2g_WHTaoJWXLf6JoauKeMvYHEzxYxc") # Add all env variables in deployment server
    BOT_SESSION = environ.get("BOT_SESSION", "vjbot")  # Add all env variables in deployment server
    DATABASE_URI = environ.get("DATABASE_URI", "mongodb+srv://AutoForwardBot:j4amtf25dMuJuJec@cluster0.fpdzert.mongodb.net/?appName=Cluster0") # Add all env variables in deployment server
    DATABASE_NAME = environ.get("DATABASE_NAME", "vj-forward-bot") # Add all env variables in deployment server
    BOT_OWNER = int(environ.get("BOT_OWNER", "7689365869")) # Add all env variables in deployment server

# Add all env variables in deployment server

class temp(object): 
    lock = {}
    CANCEL = {}
    forwardings = 0
    BANNED_USERS = []
    IS_FRWD_CHAT = []
