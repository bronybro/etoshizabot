import json
from environs import Env


# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов
IP = env.str("ip")  # айпи адреса хоста
URL_TWITTER = env.str("URL_TWITTER")
URL_TELEGRAM = env.str("URL_TELEGRAM")
LIST_EMOJI = env.int("list_emoji_length")

def config_text(filename: str = "help"):
    try:
        with open(f"data/{filename}.json", encoding='utf8') as data:
            return json.load(data)
    except FileNotFoundError:
        raise FileNotFoundError("JSON file wasn't found")

