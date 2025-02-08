import logging
import discord
from discord.ext import commands, tasks
import requests
import os
from dotenv import load_dotenv

load_dotenv()
# logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# Initialize the bot with intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
TWITCH_CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
TWITCH_CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")
TWITCH_USERNAME = os.getenv("TWITCH_USERNAME")
ANNOUNCE_CHANNEL_ID = os.getenv("ANNOUNCE_CHANNEL_ID")


twitch_access_token = None
is_live = False

def get_twitch_access_token():
    url = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": TWITCH_CLIENT_ID,
        "client_secret": TWITCH_CLIENT_SECRET,
        "grant_type": "client_credentials"
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    return response.json()["access_token"]
def check_twitch_stream():
    global twitch_access_token, is_live
    logger.info("Checking Twitch stream status...")
    if not twitch_access_token:
        twitch_access_token = get_twitch_access_token()

    headers = {
        "Client-ID": TWITCH_CLIENT_ID,
        "Authorization": f"Bearer {twitch_access_token}"
    }
    url = f"https://api.twitch.tv/helix/streams?user_login={TWITCH_USERNAME}"
    response = requests.get(url, headers=headers)

    if response.status_code == 401:  # Token expired, refresh it
        twitch_access_token = get_twitch_access_token()
        headers["Authorization"] = f"Bearer {twitch_access_token}"
        response = requests.get(url, headers=headers)

    response.raise_for_status()
    data = response.json()["data"]

    # Debug: Print the API response
    logger.info(f"Twitch API response for live status: {data}")

    if data:  # Stream is live
        if not is_live:
            is_live = True
            return True, data[0]  # Returning stream data
    else:  # Stream is offline
        is_live = False

    return False, None

@tasks.loop(minutes=1)
async def monitor_twitch():
    is_now_live, stream_data = check_twitch_stream()

    if is_now_live:
        print(f"Stream is live! Sending announcement: {stream_data['title']}")  # Add more logging
        channel = bot.get_channel(int(ANNOUNCE_CHANNEL_ID))
        if channel:
            title = stream_data["title"]
            url = f"https://www.twitch.tv/{TWITCH_USERNAME}"
            await channel.send(f"🎉 {TWITCH_USERNAME} is now live on Twitch!\n**{title}**\nWatch here: {url}")
        else:
            print("Failed to find the channel!")
    else:
        print("Stream is not live.")

@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user}!")
    
    # Log a confirmation that the bot is ready
    logger.info(f"Bot {bot.user} is ready!")

    # Send a hello message to the Discord channel
    channel = bot.get_channel(int(ANNOUNCE_CHANNEL_ID))
    if channel:
        await channel.send("Watching you endlessly, master!!!")

    # Start the Twitch monitoring task loop
    monitor_twitch.start()

# @bot.event
# async def on_disconnect():
#     # Safeguard: Ensure this runs only if the channel exists
#     channel = bot.get_channel(ANNOUNCE_CHANNEL_ID)
#     if channel:
#         await channel.send(f"🚨 {bot.user} has gone offline. I'll be back when {TWITCH_USERNAME} goes live again!")

bot.run(DISCORD_TOKEN)