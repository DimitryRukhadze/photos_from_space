import requests
import datetime


from os import environ, path
from urllib import parse
from pathlib import Path
from dotenv import load_dotenv
from img_download_tools import download_image


def get_img_extension(img_url):
    url_components = parse.urlsplit(img_url)
    img_path = parse.unquote(url_components.path)
    img_extension = path.splitext(img_path)[-1]
    return img_extension


def fetch_nasa_images(dir_name):
    nasa_url = 'https://api.nasa.gov/planetary/apod'
    nasa_api_key = environ.get('NASA_API')
    days_range = 31
    today = datetime.date.today()
    starting_date = today - datetime.timedelta(days=days_range)

    nasa_params = {
        'api_key': nasa_api_key,
        'start_date': starting_date,
        'end_date': '',
    }

    nasa_response = requests.get(nasa_url, params=nasa_params)
    nasa_response.raise_for_status()

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

            download_image(img_url, img_path)


def fetch_epic_earth_images(dir_name):
    epic_url = 'https://api.nasa.gov/EPIC/api/natural'
    nasa_api = environ.get('NASA_API')
    epic_params = {
        'api_key': nasa_api,
    }

    epic_response = requests.get(epic_url, params=epic_params)
    epic_response.raise_for_status()

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

        download_image(download_request.url, img_path)


if __name__ == '__main__':

    load_dotenv()

    nasa_dir = 'nasa'
    try:
        fetch_nasa_images(nasa_dir)
    except requests.HTTPError:
        print('Nasa server is not available.')

    epic_dir = 'epic_earth'
    try:
        fetch_epic_earth_images(epic_dir)
    except requests.HTTPError:
        print("Epic server is not available.")
