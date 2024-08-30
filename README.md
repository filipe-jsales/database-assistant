# WhatsApp Automation Bot

Este projeto é um bot de automação do WhatsApp que utiliza Selenium para interagir com o WhatsApp Web. Ele pode enviar mensagens, responder a comandos e interagir com uma API externa para gerar respostas com base em prompts específicos.

## Funcionalidades

- **Gerenciamento de Sessão**: Salva e carrega sessões do WhatsApp Web para evitar a necessidade de escanear o QR code repetidamente.
- **Mensagens Automáticas**: Envia mensagens para um grupo específico.
- **Comandos Personalizados**: Responde a comandos personalizados como `!duta` e `!everyone`.
- **Filtragem de Conteúdo**: Filtra palavras proibidas e responde de acordo.
- **Integração com API**: Utiliza uma API externa para gerar respostas com base em prompts dos usuários.
- **Gravação de Áudio**: Grava e envia mensagens de áudio no grupo.

## Instalação

### Pré-requisitos

- Python 3.7+
- Google Chrome
- ChromeDriver (gerenciado automaticamente pelo `webdriver-manager`)

### Configuração

1. Clone o repositório:
    ```bash
    git clone https://github.com/yourusername/whatsapp-automation-bot.git
    cd whatsapp-automation-bot
    ```

2. Crie e ative o ambiente virtual:

    **No Linux/MacOS:**
    ```bash
    python3 -m venv duta
    source duta/bin/activate
    ```

    **No Windows:**
    ```bash
    python -m venv duta
    duta\Scripts\activate
    ```

3. Instale os pacotes Python necessários:
    ```bash
    pip install -r requirements.txt
    ```

4. Execute o bot:
    ```bash
    python bot.py
    ```

## Configuração

- **Nome do Grupo**: Atualize a variável `group_name` no script com o nome do grupo do WhatsApp com o qual deseja interagir.
- **Integração com API**: O script está configurado para interagir com uma API em `https://ollama.chargedcloud.com.br/api/chat` usando o modelo `llama3`. Você pode modificar as variáveis `API_URL` e `API_MODEL` conforme necessário.

## Uso

### Iniciando o Bot

Execute o script e escaneie o QR code no WhatsApp Web. O bot começará a monitorar o grupo para novas mensagens.

### Comandos

- **`!duta <mensagem>`**: Envia um prompt para a API e retorna uma resposta.
- **`!everyone`**: Menciona todos os membros do grupo.
- **Palavras Proibidas**: Se uma mensagem contiver uma palavra proibida, o bot enviará uma mensagem de aviso.
- **Detecção de Bot**: Se uma mensagem contiver palavras como "bot", o bot responderá de forma rude conforme as instruções.

## Gerenciamento de Sessão

O bot salva a sessão do WhatsApp em um arquivo `whatsapp_session.pkl`. Este arquivo permite que o bot retome a sessão sem precisar escanear o QR code novamente.

## Contribuindo

Sinta-se à vontade para abrir issues ou enviar pull requests se quiser contribuir para este projeto.

## Licença

Este projeto é licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.
