import requests
import datetime
import telegram


from pathlib import Path
from urllib import parse
from os import path, environ
from dotenv import load_dotenv

load_dotenv()

def image_download(img_url, save_to):
    response = requests.get(img_url)
    response.raise_for_status()

    with open(save_to, 'wb') as file:
        file.write(response.content)


def fetch_spacex_last_launch(dir_name):
    spacex_url = 'https://api.spacexdata.com/v4/launches/5eb87d1fffd86e000604b36b'
    try:
        spacex_response = requests.get(spacex_url)
        spacex_response.raise_for_status()
    except:
        print('SpaceX server is not available')

    launch_info = spacex_response.json()
    launch_img_links = launch_info['links']['flickr']['original']

    for link in launch_img_links:
        img_url = link
        img_name = link.split('/')[-1]
        Path(dir_name).mkdir(exist_ok=True)
        img_path = f'{dir_name}/{img_name}'

        image_download(img_url, img_path)


def get_img_extension(img_url):
    url_components = parse.urlsplit(img_url)
    img_path = parse.unquote(url_components.path)
    img_extension = path.splitext(img_path)[-1]
    return img_extension


def fetch_nasa_img(dir_name):
    nasa_url = 'https://api.nasa.gov/planetary/apod'
    nasa_api_key = environ.get('NASA_API')
    days_range = 31
    today = datetime.date.today()
    starting_date = today - datetime.timedelta(days=days_range)

    nasa_params = {
        'api_key': f'{nasa_api_key}',
        'start_date': f'{starting_date}',
        'end_date': '',
    }

    try:
        nasa_response = requests.get(nasa_url, params=nasa_params)
        nasa_response.raise_for_status()
    except:
        print('NASA server is not available')

    nasa_response_info = nasa_response.json()
    img_number = 1
    for img in nasa_response_info:
        img_url = img['url']
        img_extension = get_img_extension(img_url)
        if img_extension:
            img_name = f'nasa_{img_number}{img_extension}'
            img_number += 1
            Path(dir_name).mkdir(exist_ok=True)
            img_path = f'{dir_name}/{img_name}'

            image_download(img_url, img_path)


def fetch_epic_earth(dir_name):
    epic_url = 'https://api.nasa.gov/EPIC/api/natural'
    nasa_api = environ.get('NASA_API')
    epic_params = {
        'api_key': f'{nasa_api}'
    }

    try:
        epic_response = requests.get(epic_url, params=epic_params)
        epic_response.raise_for_status()
    except:
        print('Epic server is not available')

    epic_info = epic_response.json()

    for info in epic_info:
        img_date = info['date']
        date_url = img_date[:10].replace('-', '/')
        img_name = f"{info['image']}.png"
        download_img_url = 'https://api.nasa.gov/EPIC/archive/natural'

        img_link = f'{download_img_url}/{date_url}/png/{img_name}'
        download_request = requests.get(img_link, params=epic_params)

        Path(dir_name).mkdir(exist_ok=True)
        img_path = f'{dir_name}/{img_name}'

        image_download(download_request.url, img_path)


if __name__ == '__main__':

    fetch_spacex_last_launch('spaceX')
    fetch_nasa_img('nasa')
    fetch_epic_earth('epic_earth')

    bot_token = environ.get('TELEGRAM_BOT_TOKEN')
    bot = telegram.Bot(token=bot_token)

    test_text = 'это тестовое сообщение'
    test_chat_id = bot.get_updates()[-1].my_chat_member.chat.id
    print(test_chat_id)
    bot.send_message(text=test_text, chat_id=test_chat_id)