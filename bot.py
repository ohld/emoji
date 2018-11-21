import os
import logging
import requests
import telegram
from telegram.error import NetworkError, Unauthorized
from time import sleep

from imageGenerator import generate_random_emoji_cover

update_id = None

def main():
    """Run the bot."""
    global update_id
    # Telegram Bot Authorization Token
    bot = telegram.Bot(os.environ['TELEGRAM_TOKEN'])

    # get the first pending update_id, this is so we can skip over it in case
    # we get an "Unauthorized" exception.
    try:
        update_id = bot.get_updates()[0].update_id
    except IndexError:
        update_id = None

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    while True:
        try:
            send_emojicover(bot)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            # The user has removed or blocked the bot.
            update_id += 1


def send_emojicover(bot):
    global update_id
    # Request updates after the last update_id
    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1
        if update.message:  # your bot can receive updates without messages
            chat_id = update.message["chat"]["id"]
            img_path = generate_random_emoji_cover()
            bot.send_photo(chat_id=chat_id, photo=open(img_path, 'rb'))


if __name__ == '__main__':
    main()