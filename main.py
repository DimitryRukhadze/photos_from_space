import telegram
import time


from os import environ, listdir
from dotenv import load_dotenv
from fetch_nasa import fetch_nasa_images, fetch_epic_earth_images
from fetch_spacex import fetch_spacex_last_launch
from pathlib import Path


def count_sleep_time(default_delay, time_measure='', delay_time=1):
    if not time_measure:
        return float(default_delay)
    elif time_measure == 'hour':
        user_delay = (float(default_delay)/24)*delay_time
        return user_delay
    elif time_measure == 'minute':
        user_delay = ((float(default_delay)/24)/60)*delay_time
        return user_delay
    elif time_measure == 'second':
        user_delay = (((float(default_delay)/24)/60)/60)*delay_time
        return user_delay


if __name__ == '__main__':

    load_dotenv()
    env_delay = environ.get('POSTING_DELAY')
    nasa_api_key = environ.get('NASA_API')

    space_x_dir = 'spaceX'
    Path(space_x_dir).mkdir(exist_ok=True)
    fetch_spacex_last_launch(space_x_dir)

    nasa_dir = 'nasa'
    Path(nasa_dir).mkdir(exist_ok=True)
    fetch_nasa_images(nasa_dir, nasa_api_key)

    epic_dir = 'epic_earth'
    Path(epic_dir).mkdir(exist_ok=True)
    fetch_epic_earth_images(epic_dir, nasa_api_key)

    bot_token = environ.get('TELEGRAM_BOT_TOKEN')
    bot = telegram.Bot(token=bot_token)

    test_chat_id = bot.get_updates()[-1].channel_post.sender_chat.id

    while True:
        posting_delay = count_sleep_time(env_delay, time_measure='second', delay_time=10)
        dirs = listdir('.')

        for directory in dirs:
            if directory in [space_x_dir, nasa_dir, epic_dir]:
                file_names = listdir(directory)
                file_paths = [f'{directory}/{name}' for name in file_names]
                for filepath in file_paths:
                    try:
                        with open(filepath, 'rb') as document:
                            bot.send_document(chat_id=test_chat_id, document=document)
                    except telegram.TelegramError:
                        continue
                    time.sleep(posting_delay)
