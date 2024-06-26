import requests
from bs4 import BeautifulSoup
import telebot

# URL das páginas web dos serviços
division2_url = "http://ubistatic-a.akamaihd.net/0115/tctd2/status.html"
locaweb_url = "https://statusblog.locaweb.com.br/"

# Token do seu bot Telegram
bot_token = ""

# Criar uma instância do bot
bot = telebot.TeleBot(bot_token)
last_status = {}
# Função para obter o status do serviço
def get_service_status(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    if url == division2_url:
        div_pc = soup.find("div", {"id": "dvPC"})
        image_pc = div_pc.find("img", {"id": "maintenancePC"}) if div_pc else None

        if image_pc and "hidden" in image_pc.get("class", []):
            new_image_pc = div_pc.find("img", {"id": "onlinePC"}) if div_pc else None
            if new_image_pc:
                return "Servidor de The Division 2 está Online"
            else:
                return "O servidor de The Division 2 está passando por problemas técnicos"
        else:
            return "Manutenção em andamento no servidor de The Division 2."
    
    elif url == locaweb_url:
        div_component = soup.find("div", {"data-component-id": "b1fghzyns25r"})
        
        if div_component:
            spans = div_component.find_all("span")
            for span in spans:
                if span.get("class") == ["name"] and span.text.strip() == "Email":
                    status_span = div_component.find("span", {"class": "component-status"})
                    if status_span and status_span.text.strip() == "Operational":
                        return "Servidor Email Locaweb Online"
        
        return "Servidor email Locaweb está offline"

    else:
        return "URL inválida."

# Lidar com o comando /status
@bot.message_handler(commands=['status'])
def handle_status(message):
    # Criar o teclado inline
    keyboard = telebot.types.InlineKeyboardMarkup()
    button1 = telebot.types.InlineKeyboardButton(text="The Division 2 Server", callback_data="division2")
    button2 = telebot.types.InlineKeyboardButton(text="Locaweb Email", callback_data="locaweb")
    keyboard.add(button1, button2)
    
    # Enviar a mensagem com o teclado inline
    bot.send_message(message.chat.id, "Selecione uma opção:", reply_markup=keyboard)

# Lidar com os callbacks dos botões
@bot.callback_query_handler(func=lambda call: True)
def handle_button_callback(call):
    user_id = call.from_user.id
    if user_id in last_status and last_status[user_id] == call.data:
        return
    
    if call.data == "division2":
        status = get_service_status(division2_url)
    elif call.data == "locaweb":
        status = get_service_status(locaweb_url)
    else:
        status = "Serviço inválido."
    last_status[user_id] = call.data
    # Enviar a mensagem com o status
    bot.send_message(call.message.chat.id, status)

# Iniciar o bot
bot.polling()
