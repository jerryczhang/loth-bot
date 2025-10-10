import os

from dotenv import load_dotenv

from loth_bot import bot

if __name__ == "__main__":
    load_dotenv()
    bot.run(os.getenv("TOKEN"))
