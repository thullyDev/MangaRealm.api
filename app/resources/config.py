from environs import Env

config = Env()
config.read_env()

MANGANATO_API_URL: str = config("MANGANATO_API_URL")
SQL_URL: str = config("SQL_URL")
REDIS_URL: str = config("REDIS_URL")
ORIGINS: str = config("ORIGINS")
