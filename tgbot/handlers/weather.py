import pymorphy2 as pymorphy2
import requests
from aiogram import types, Dispatcher
from tgbot.config import load_config

config = load_config(".env")

DEGREE_SIGN = u'\N{DEGREE SIGN}'

weather_token = config.misc.weather_token
morph = pymorphy2.MorphAnalyzer()


def get_request_link(city_from_user: str, weather_token: str) -> str:
    return (f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={city_from_user}&lang=ru&appid={weather_token}&units=metric")


def change_declension(city_name: str) -> str:
    split_by_space = city_name.split(' ')
    try:
        transformed_city_name = ' '.join(
            [morph.parse(i)[0].inflect({'loct'}).word.capitalize() for i in split_by_space]
        )
    except AttributeError:
        return city_name
    if "-" in transformed_city_name:
        capitalize_dash_city_name = '-'.join(
            [i.capitalize() for i in transformed_city_name.split('-')]
        )
        return capitalize_dash_city_name
    return transformed_city_name


async def bot_weather(message: types.Message):
    request_link = get_request_link(message.text, weather_token)
    content = requests.get(request_link).json()
    try:
        city_name = content['name']
    except KeyError:
        await message.answer(
            'Прости, но я не знаю такого города. Попробуй еще раз!'
        )
    weather_description = content['weather'][0]['description']
    temp_min = content['main']['temp_min']
    temp_max = content['main']['temp_max']
    feels_like = content['main']['feels_like']
    current_temp = content['main']['temp']
    transformed_city_name = change_declension(city_name)
    wind_speed = content['wind']['speed']
    country = content['sys']['country']
    text = (f'Сегодня в {transformed_city_name} ({country}) {weather_description}. '
            f'Температура воздуха составляет {current_temp} градусов по Цельсию '
            f'(ощущется как {feels_like}{DEGREE_SIGN}C) '
            f'Температура колеблется между {temp_min} и {temp_max}{DEGREE_SIGN}С. '
            f'Скорость ветра составляет {wind_speed} м/c.')
    await message.answer(text)


def register_weather(dp: Dispatcher):
    dp.register_message_handler(bot_weather)
