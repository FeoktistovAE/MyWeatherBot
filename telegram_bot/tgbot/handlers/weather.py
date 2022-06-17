import pymorphy2 as pymorphy2
import requests
from aiogram import types, Dispatcher

WEATHER_TOKEN = '285ba8bc2114b38a35af79d844bb77d7'
morph = pymorphy2.MorphAnalyzer()
degree_sign= u'\N{DEGREE SIGN}'


def transform_city_name(city_name):
    split_by_space = city_name.split(' ')
    try:
        transformed_city_name = ' '.join([morph.parse(i)[0].inflect({'loct'}).word.capitalize() for i in split_by_space])
    except AttributeError:
        return city_name
    if "-" in transformed_city_name:
        capitalize_dash_city_name = '-'.join([i.capitalize() for i in transformed_city_name.split('-')])
        return capitalize_dash_city_name
    return transformed_city_name



async def bot_weather(message: types.Message):
    city_from_user = message.text
    API_link = f"https://api.openweathermap.org/data/2.5/weather?q={city_from_user}&lang=ru&appid={WEATHER_TOKEN}&units=metric"
    updates = requests.get(API_link).json()
    try:
        city_name = updates['name']
    except KeyError:
        await message.answer('Прости, но я не знаю такого города. Попробуй еще раз!')
    weather_description = updates['weather'][0]['description']
    temp_min = updates['main']['temp_min']
    temp_max = updates['main']['temp_max']
    feels_like = updates['main']['feels_like']
    current_temp = updates['main']['temp']
    transformed_city_name = transform_city_name(city_name)
    wind_speed = updates['wind']['speed']
    country = updates['sys']['country']
    text = f'Сегодня в {transformed_city_name} ({country}) {weather_description}.' \
           f' Температура воздуха составляет {current_temp} градусов по Цельсию (ощущется как {feels_like}{degree_sign}C)' \
           f' Температура колеблется между {temp_min} и {temp_max}{degree_sign}С. Скорость ветра составляет {wind_speed} м/c.'
    await message.answer(text)



def register_weather(dp: Dispatcher):
    dp.register_message_handler(bot_weather)
