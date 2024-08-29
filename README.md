# WhatsApp Automation Bot

This project is a WhatsApp automation bot that uses Selenium to interact with WhatsApp Web. It can send messages, respond to commands, and interact with an external API to generate responses based on specific prompts.

## Features

- **Session Management**: Saves and loads WhatsApp Web sessions to avoid repeated QR code scans.
- **Automated Messaging**: Sends messages to a specific group.
- **Custom Commands**: Responds to custom commands like `!duta` and `!everyone`.
- **Content Filtering**: Filters out banned words and responds accordingly.
- **API Integration**: Uses an external API to generate responses based on user prompts.
- **Audio Recording**: Records and sends audio messages in the group.

## Installation

### Prerequisites

- Python 3.7+
- Google Chrome
- ChromeDriver (managed automatically by `webdriver-manager`)

### Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/whatsapp-automation-bot.git
    cd whatsapp-automation-bot
    ```

2. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the bot:
    ```bash
    python bot.py
    ```

## Configuration

- **Group Name**: Update the `group_name` variable in the script with the name of the WhatsApp group you want to interact with.
- **API Integration**: The script is set up to interact with an API at `https://ollama.chargedcloud.com.br/api/chat` using the `llama3` model. You can modify the `API_URL` and `API_MODEL` variables as needed.

## Usage

### Starting the Bot

Run the script and scan the QR code on WhatsApp Web. The bot will start monitoring the group for new messages.

### Commands

- **`!duta <message>`**: Sends a prompt to the API and returns a response.
- **`!everyone`**: Mentions all group members.
- **Banned Words**: If a message contains a banned word, the bot will send a warning message.
- **Bot Detection**: If a message contains words like "bot", the bot will respond rudely as per the instructions.

## Session Management

The bot saves the WhatsApp session in a `whatsapp_session.pkl` file. This file allows the bot to resume the session without needing to scan the QR code again.

## Contributing

Feel free to open issues or submit pull requests if you want to contribute to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
