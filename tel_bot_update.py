import requests
from bs4 import BeautifulSoup
import telebot
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()
# URL das páginas web dos serviços
division2_url = os.getenv('division2_url')
locaweb_url = os.getenv('locaweb_url')
anydesk_url = os.getenv('anydesk_url')

# Token do seu bot Telegram
bot_token = os.getenv('bot_token')

# Criar uma instância do bot
bot = telebot.TeleBot(bot_token)
last_status = {}


def get_public_ip() -> str:
    """
    Esta função usa a biblioteca requests para fazer uma requisição HTTP para o
    endpoint da API do ipify e retorna o endereço IP público do dispositivo. Se a
    solicitação falhar, ela retorna uma mensagem de erro padrão.

    :return: O endereço IP público do dispositivo
    :rtype: str
    """
    try:
        response = requests.get("https://api.ipify.org/?format=json")
        data = response.json()
        ip_address = data["ip"]
        return ip_address
    except:
        return "Não foi possível obter o endereço IP público."


# Função para obter o status do serviço
def get_service_status(url: str) -> str:
    """
    Esta função usa a biblioteca requests e BeautifulSoup para fazer uma requisição
    HTTP e analisar o HTML da página web do serviço especificado. Ela retorna o
    status do serviço como uma string.

    :param url: A URL da página web do serviço
    :type url: str
    :return: O status do serviço
    :rtype: str
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    if url == division2_url:
        div_pc = soup.find("div", {"id": "dvPC"})
        image_pc = div_pc.find("img", {"id": "maintenancePC"}) if div_pc else None

        if image_pc and "hidden" in image_pc.get("class", []):
            new_image_pc = div_pc.find("img", {"id": "onlinePC"}) if div_pc else None
            if new_image_pc:
                return "Servidor The Division 2 está online"
            else:
                return "Possível erro no servidor"
        else:
            return "Manutenção em andamento."

    elif url == locaweb_url:
        div_component = soup.find("div", {"data-component-id": "b1fghzyns25r"})

        if div_component:
            spans = div_component.find_all("span")
            for span in spans:
                if span.get("class") == ["name"] and span.text.strip() == "Email":
                    status_span = div_component.find("span", {"class": "component-status"})
                    if status_span and status_span.text.strip() == "Operational":
                        return "Servidor Locaweb Email está online"

            return "O servidor está offline."

    elif url == anydesk_url:
        div_title = soup.find("div", {"class": "incident-title font-large"})

        if div_title:
            a_tag = div_title.find("a")
            if a_tag and a_tag.text.strip().lower() == "degraded performance":
                return "Manutenção do servidor Anydesk em andamento."

        return "Servidor Anydesk online!"

    else:
        return "URL inválida."


# Lidar com o comando /status
@bot.message_handler(commands=["status"])
def handle_status(message: telebot.types.Message):
    # Criar o teclado inline
    keyboard = telebot.types.InlineKeyboardMarkup()
    button1 = telebot.types.InlineKeyboardButton(
        text="The Division 2 Server", callback_data="division2"
    )
    button2 = telebot.types.InlineKeyboardButton(
        text="Locaweb Email", callback_data="locaweb"
    )
    button3 = telebot.types.InlineKeyboardButton(
        text="AnyDesk", callback_data="anydesk"
    )
    keyboard.add(button1, button2, button3)

    # Enviar a mensagem com o teclado inline
    bot.send_message(
        message.chat.id, "Selecione uma opção:", reply_markup=keyboard
    )


# Lidar com os callbacks dos botões
@bot.callback_query_handler(func=lambda call: True)
def handle_button_callback(call: telebot.types.CallbackQuery):
    user_id = call.from_user.id
    if user_id in last_status and last_status[user_id] == call.data:
        return

    if call.data == "division2":
        status = get_service_status(division2_url)
    elif call.data == "locaweb":
        status = get_service_status(locaweb_url)
    elif call.data == "anydesk":
        status = get_service_status(anydesk_url)
    else:
        status = "Serviço inválido."
    last_status[user_id] = call.data
    # Enviar a mensagem com o status
    bot.send_message(call.message.chat.id, status)


@bot.message_handler(commands=["ip"])
@bot.message_handler(func=lambda message: message.text == "ip")
def handle_ip_command(message: telebot.types.Message):
    ip_address = get_public_ip()
    bot.reply_to(message, f"Seu endereço IP público é: {ip_address}")


@bot.message_handler(func=lambda message: message.text.lower() == "status locaweb")
@bot.message_handler(func=lambda message: message.text.lower() == "status anydesk")
def handle_messages(message: telebot.types.Message):
    if message.text == "status locaweb":
        status = get_service_status(locaweb_url)
        bot.reply_to(message, status)
    elif message.text == "status anydesk":
        status = get_service_status(anydesk_url)
        bot.reply_to(message, status)

    else:
        status = get_service_status(division2_url)
        bot.reply_to(message, status)


# Iniciar o bot
bot.polling()