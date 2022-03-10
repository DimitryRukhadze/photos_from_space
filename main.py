import telegram
import time


from os import environ, listdir
from dotenv import load_dotenv
from fetch_nasa import fetch_nasa_images, fetch_epic_earth_images
from fetch_spacex import fetch_spacex_last_launch


def count_sleep_time(time_measure='', delay_time=1):
    env_delay = environ.get('POSTING_DELAY')
    if not time_measure:
        return float(env_delay)
    elif time_measure == 'hour':
        env_delay = (float(env_delay)/24)*delay_time
        return env_delay
    elif time_measure == 'minute':
        env_delay = ((float(env_delay)/24)/60)*delay_time
        return env_delay
    elif time_measure == 'second':
        env_delay = (((float(env_delay)/24)/60)/60)*delay_time
        return env_delay


if __name__ == '__main__':

    load_dotenv()

    space_x_dir = 'spaceX'
    fetch_spacex_last_launch(space_x_dir)

    nasa_dir = 'nasa'
    fetch_nasa_images(nasa_dir)

    epic_dir = 'epic_earth'
    fetch_epic_earth_images(epic_dir)

    bot_token = environ.get('TELEGRAM_BOT_TOKEN')
    bot = telegram.Bot(token=bot_token)

    test_chat_id = bot.get_updates()[-1].my_chat_member.chat.id

    while True:
        posting_delay = count_sleep_time(time_measure='second', delay_time=10)
        dirs = listdir('.')

        for directory in dirs:
            if directory == space_x_dir or dir == nasa_dir or dir == epic_dir:
                files = listdir(directory)
                file_paths = [f'{dir}/{file}' for file in files]
                for path in file_paths:
                    try:
                        bot.send_document(chat_id=test_chat_id, document=open(path, 'rb'))
                    except telegram.TelegramError:
                        continue
                    time.sleep(posting_delay)
