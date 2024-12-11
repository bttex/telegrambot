# Monitoramento de Serviços com Telegram Bot

Este projeto implementa um bot no Telegram para monitorar o status de servidores de serviços como The Division 2, Locaweb Email e AnyDesk. O bot permite que o usuário verifique o status de cada serviço e o seu endereço IP público.

## Funcionalidades

- **Status dos Serviços**: O bot retorna o status dos servidores de serviços como "The Division 2", "Locaweb Email" e "AnyDesk".
- **IP Público**: O bot também retorna o endereço IP público do dispositivo.
- **Comandos**:
  - `/status`: Exibe um menu para escolher entre os serviços disponíveis.
  - `/ip` ou "ip": Exibe o IP público do dispositivo.
  - "status locaweb", "status anydesk", "status division2": Retorna o status diretamente de cada serviço.

## Requisitos

1. Python 3.x
2. Telegram Bot Token configurado no `.env`.
3. URLs dos serviços configuradas no `.env` (The Division 2, Locaweb, AnyDesk).

## Configuração

1. **Crie um arquivo `.env` no diretório do projeto:**

   ```
   division2_url = <url>
    locaweb_url = <url>
    anydesk_url = "<url
    bot_token = <token>
   ```

   - Substitua `<seu_token_do_bot>` pelo token do seu bot no Telegram.
   - Substitua `<id_do_chat>` pelo ID do chat onde deseja receber as notificações.
   - Certifique-se de que as URL estão corretas.

2. **Instale as Dependências:**
   ```bash
   pip install -r requirements.txt
   ```

## Uso

Execute o script para iniciar o monitoramento:

```bash
python tel_bot_update.py
```


## Contribuições

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do repositório.
2. Crie uma branch para sua feature ou correção:
   ```bash
   git checkout -b minha-feature
   ```
3. Envie um Pull Request para revisão.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
