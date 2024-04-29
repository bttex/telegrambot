
# Telegram Service Bot

O código verifica o status de três serviços:
The Division 2 Server (Ubisoft Connect)
Locaweb Email
AnyDesk


Para verificar o status, o código faz uma solicitação HTTP para a página do serviço e analisa o HTML. Ele verifica se há uma imagem específica que indica que o serviço está online ou se há uma imagem específica que indica que o serviço está offline.

O código também verifica se há uma mensagem específica que indica que o servidor está em manutenção.

O código usa uma função para obter o endereço IP público do usuário.

O código usa um botão de status que envia um teclado com três opções para o usuário escolher. Quando o usuário clica em um botão, o código verifica o status do serviço e envia uma mensagem com o status.

O código também usa comandos para obter o endereço IP público e verificar o status de um serviço. Quando o usuário envia um comando, o código verifica o status e envia uma mensagem com o status.

O código usa um botão de IP que envia o endereço IP público do usuário.

O código usa duas funções anônimas para lidar com os comandos e os botões.



## Instalação

Instale a biblioteca beautifulSoup, telebot e requests

```bash
  pip install telebot requests beautifulsoup4
```
Execute o arquivo python e teste no telegram.
