from environs import Env

config = Env()
config.read_env()

MANGANATO_API_URL: str = config("MANGANATO_API_URL")
SQL_URL: str = config("SQL_URL")
REDIS_URL: str = config("REDIS_URL")
ORIGINS: str = config("ORIGINS")
IMAGEKIT_PUBLIC_KEY: str = config("IMAGEKIT_PUBLIC_KEY")
IMAGEKIT_PRIVATE_KEY: str = config("IMAGEKIT_PRIVATE_KEY")
IMAGEKIT_URL_ENDPOINT: str = config("IMAGEKIT_URL_ENDPOINT")
