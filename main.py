import telebot
import mysql.connector
import random
import requests
# Инициализация бота с вашим токеном
bot = telebot.TeleBot('')

# Подключение к базе данных MySQL
db = mysql.connector.connect(
    host="",
    user="",
    password="",
    database="menu_db"
)

# Функция для получения случайного блюда из базы данных(MySQL)
def get_random_dish():
    cursor = db.cursor()
    
    # Выбор случайного блюда из соответствующих таблиц
    cursor.execute("SELECT name FROM breakfast")
    breakfast_dishes = cursor.fetchall()
    random_breakfast = random.choice(breakfast_dishes)[0]
    
    cursor.execute("SELECT name FROM lunch")
    lunch_dishes = cursor.fetchall()
    random_lunch = random.choice(lunch_dishes)[0]
    
    cursor.execute("SELECT name FROM dinner")
    dinner_dishes = cursor.fetchall()
    random_dinner = random.choice(dinner_dishes)[0]
    
    return random_breakfast, random_lunch, random_dinner

# Функция для получения погоды в Санкт-Петербурге(Open weather)
def get_weather():
    city = 'Saint%20Petersburg'
    API = ''
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric&lang=ru'
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        return f" Погода в Санкт-Петербурге:  {weather_description}\nТемпература:  {temperature} °C"
    else:
        return "Не удалось получить данные о погоде."

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1)
    menu_button = telebot.types.KeyboardButton('Показать меню')
    weather_button = telebot.types.KeyboardButton('Показать погоду')
    markup.add(menu_button, weather_button)
    bot.send_message(message.chat.id, "Добро пожаловать! Выберите действие:", reply_markup=markup)

# Обработчики нажатия кнопок
@bot.message_handler(func=lambda message: message.text == 'Показать меню')
def show_menu(message):
    dish = get_random_dish()
    bot.send_message(
    message.chat.id, 
    f"\n<b><i>Завтрак</i></b>\n{dish[0]}\n\n<b><i>Обед</i></b>\n{dish[1]}\n\n<b><i>Ужин</i></b>\n{dish[2]}", 
    parse_mode='HTML')

@bot.message_handler(func=lambda message: message.text == 'Показать погоду')
def show_weather(message):
    weather = get_weather()
    bot.send_message(message.chat.id, weather)

# Обработчик письменных сообщений
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_message(message.chat.id, "Извините, но я не отвечаю на сообщения. Пожалуйста, нажмите кнопку.")

bot.polling()