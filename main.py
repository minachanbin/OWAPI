import requests
import datetime
import tkinter as tk
from tkinter import messagebox
from config import open_weather_token

def get_weather(city, open_weather_token):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Хмарно \U00002601",
        "Rain": "Дощ \U00002614",
        "Drizzle": "Дощ \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Сніг \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        wd = code_to_smile.get(weather_description, "Сталася помилка, напишіть свій запрос читкіше")

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = sunset_timestamp - sunrise_timestamp

        current_time = datetime.datetime.utcfromtimestamp(data["dt"]) + datetime.timedelta(seconds=data["timezone"])

        messagebox.showinfo(
            "Погода",
            f"***{current_time.strftime('%Y-%m-%d %H:%M')}***\n"
            f"Погода у місті '{city}':\nТемпература: {cur_weather}°C {wd}\n"
            f"Вологість: {humidity}%\nТиск: {pressure} мм.рт.ст\nШвидкість вітру: {wind} м/с\n"
            f"Схід сонця: {sunrise_timestamp.strftime('%H:%M')}\nЗахід сонця: {sunset_timestamp.strftime('%H:%M')}\n"
            f"Тривалість дня: {length_of_the_day}\n"
            f"Гарного дня!"
        )

    except Exception as ex:
        messagebox.showerror("Помилка", f"Сталася помилка: {ex}\nПеревірте назву міста")


def main():
    def on_submit():
        city = city_entry.get()
        get_weather(city, open_weather_token)

    root = tk.Tk()
    root.title("Погодний застосунок")

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    label = tk.Label(frame, text="Введіть назву міста:")
    label.grid(row=0, column=0)

    city_entry = tk.Entry(frame)
    city_entry.grid(row=0, column=1)

    submit_button = tk.Button(frame, text="Отримати погоду", command=on_submit)
    submit_button.grid(row=1, columnspan=2)

    root.mainloop()


if __name__ == '__main__':
    main()
