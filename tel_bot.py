import requests
from bs4 import BeautifulSoup
import telebot
import time

# URL da página web
url = "http://ubistatic-a.akamaihd.net/0115/tctd2/status.html"

# Obtendo o conteúdo da página web

# Inicializando o bot do Telegram
bot_token = "6010277135:AAHqSfHKnZPChtmCzScXd8aadZ8bF1R_LNw"
bot = telebot.TeleBot(bot_token)


@bot.message_handler(commands=['status'])
def check_status(message):
    # Obtendo o conteúdo da página web
    response = requests.get(url)
    html_content = response.text

    # Analisando o HTML com BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Verificando se a imagem de manutenção está presente
    div_pc = soup.find("div", {"id": "dvPC"})
    image_pc = div_pc.find("img", {"id": "maintenancePC"}) if div_pc else None

    if image_pc and "hidden" in image_pc.get("class", []):
        new_image_pc = div_pc.find("img", {"id": "onlinePC"}) if div_pc else None
        if new_image_pc:
            # Enviando mensagem para o chat
            chat_id = message.chat.id
            response_message = "A manutenção foi encerrada."
            bot.send_message(chat_id, response_message)
        
    else:
        response_message = "Manutenção em andamento."
        bot.send_message(message.chat.id, response_message)


bot.polling()