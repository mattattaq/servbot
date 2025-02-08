# SERVBOT

This project will cover how I created my discord bot along with helpful documentation.

## PROJECT STRUCTURE

```
DISCORD-BOT/
--|.gitignore
--|bot.py
--|requirements.txt
```

## WHAT'S MISSING

You will need to create a .env file in the root directory with the following values.

```
DISCORD_TOKEN={REPLACE_WITH_ACTUAL_VALUE}
TWITCH_CLIENT_ID={REPLACE_WITH_ACTUAL_VALUE}
TWITCH_CLIENT_SECRET={REPLACE_WITH_ACTUAL_VALUE}
TWITCH_USERNAME={REPLACE_WITH_ACTUAL_VALUE}
ANNOUNCE_CHANNEL_ID={REPLACE_WITH_ACTUAL_VALUE}
```

an example would look like this:

```
TWITCH_USERNAME=duida
```

The purpose is to keep account and channel information separate from pushed public code.

## PREREQUISITES

### 1. Create a Discord Bot

To integrate your bot with Discord, you'll need to register it in the **Discord Developer Portal**:

1. **Go to** [Discord Developer Portal](https://discord.com/developers/applications)
2. **Click "New Application"** (top right).
3. **Give your bot a name**, then click **Create**.
4. **Navigate to "Bot" (left sidebar)** and click **"Add Bot"**.
5. Under the **Bot Settings**, enable:
   - `Public Bot` (optional, if you want others to invite it)
   - `Presence Intent`, `Server Members Intent`, and `Message Content Intent` (if needed for your bot’s functionality).
6. **Copy the Bot Token** under **"Click to Reveal Token"**—you'll need this for your `.env` file.

### 2. Invite Your Bot to a Server

1. **Go to "OAuth2" > "URL Generator"** in the Developer Portal.
2. Under **Scopes**, select `bot`.
3. Under **Bot Permissions**, check the permissions your bot needs (e.g., `Send Messages`, `Read Message History`).
4. **Copy the generated URL** and open it in your browser.
5. **Select a server** and click **Authorize** to invite the bot.

### 3. Get Required Credentials

| **Credential**         | **Where to Find It**                                                                                                |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------- |
| `DISCORD_TOKEN`        | Found in **Discord Developer Portal** under **Bot → Click to Reveal Token**                                         |
| `TWITCH_CLIENT_ID`     | Found in **[Twitch Developer Console](https://dev.twitch.tv/console)** under **Applications → Register Your App**   |
| `TWITCH_CLIENT_SECRET` | After registering an app in the **Twitch Developer Console**, click **Manage**, then **Generate Secret**            |
| `ANNOUNCE_CHANNEL_ID`  | Right-click a Discord channel → Click **Copy ID** (Requires Developer Mode enabled in **User Settings → Advanced**) |

### 3. Set Up a Python Environment

Ensure you have **Python 3.8+** installed and **pip** updated:

```sh
python --version
pip install --upgrade pip
```

## HOW DO I RUN THIS LOCALLY?

In a python environment

1. Install dependencies

- pip install -r requirements.txt

2. Make a .env file
3. Run the bot:

```sh
python bot.py
```

## RUNNING ON A RASPBERRY PI

If you want to run this bot on a **Raspberry Pi**, follow these steps:

### 1. Set Up Your Raspberry Pi

Ensure your Raspberry Pi is up to date:

```sh
sudo apt update && sudo apt upgrade -y
```

Install Python 3 and pip if they are not already installed:

```sh
sudo apt install python3 python3-pip -y
```

Verify the installation:

```
python3 --version
pip3 --version
```

### 2. Clone the Project

```sh
git clone https://github.com/your-repo/discord-bot.git
cd discord-bot
```

### 3. Install Dependencies

Use pip to install the required dependencies:

```sh
pip3 install -r requirements.txt
```

### 4. Set Up Environment Variables

Follow the steps in prerequisites to create the `.env` file

### 5. Run the Bot

To start the bot manually:

```sh
python3 bot.py
```

## Bonus 10 billion points if you want to create a service! Here is how!

### Auto-Restart on Boot

To ensure the bot starts automatically after a reboot, create a systemd service:

1. Open a new service file:

```sh
sudo nano /etc/systemd/system/discord-bot.service
```

2. Add the following content:

```ini
[Unit]
Description=Discord Bot
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/discord-bot/bot.py
WorkingDirectory=/home/pi/discord-bot
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
```

Replace `/home/pi/discord-bot/` with the actual path where your bot is stored.

3. Enable and start the service:

```sh
sudo systemctl enable discord-bot
sudo systemctl start discord-bot
```

4. Check the status:

```sh
sudo systemctl status discord-bot
```

You may also run the command below to get more detailed logs.

```sh
sudo journalctl -u discord-bot -f
```

## ADDITIONAL RESOURCES

Further reading if you'd like help imaging your raspberry pi, what you can do with your discord bot, and twitch api documentation:

- **Raspberry Pi Imaging & Setup**: [Raspberry Pi Imager Guide](https://www.raspberrypi.com/software/)
- **Discord Bot Commands & API**: [Discord Developer Portal](https://discord.com/developers/docs/intro)
- **Twitch API & Authentication**: [Twitch Developer Documentation](https://dev.twitch.tv/docs)
- **Systemd for Auto-Restarting Services**: [Systemd Service Configuration](https://www.freedesktop.org/software/systemd/man/systemd.service.html)
