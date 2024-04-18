import asyncio
import logging
import math
import os
import datetime
import requests
from aiogram import Bot, types, Dispatcher
from aiogram.filters.command import Command


logging.basicConfig(level=logging.INFO)

bot = Bot(token="7016822341:AAFvIBrx_b5Q5jeTm5fwmB4_lGglKGmwbyY")
dp = Dispatcher()


@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.reply("Привет! Напиши мне название города и я пришлю сводку погоды")


@dp.message()
async def get_weather(message: types.Message):
    try:
        x = message.text
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={x}&lang=ru&units=metric&appid=19811673e38d7f1d99acfe76f2b0fadc")
        data = response.json()
        city = data["name"]
        cur_temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]

        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])

        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])

        code_to_smile = {
                "Clear": "Ясно \U00002600",
                "Clouds": "Облачно \U00002601",
                "Rain": "Дождь \U00002614",
                "Drizzle": "Дождь \U00002614",
                "Thunderstorm": "Гроза \U000026A1",
                "Snow": "Снег \U0001F328",
                "Mist": "Туман \U0001F32B"
        }

        weather_description = data["weather"][0]["main"]

        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри в окно, я не понимаю, что там за погода..."

        await message.reply(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
                            f"Погода в городе: {city}\nТемпература: {cur_temp}°C {wd}\n"
                            f"Влажность: {humidity}%\nДавление: {math.ceil(pressure / 1.333)} мм.рт.ст\nВетер: {wind} м/с \n"
                            f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
                            f"Хорошего дня!")
    except:
        await message.reply("Проверьте название города!")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())