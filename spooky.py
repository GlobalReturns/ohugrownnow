import discord
import os
import requests
from discord.ext import commands, tasks

# Discord Bot Token
TOKEN = 'PLACETOKENHERE'

# Discord Server ID where you want the notifications
SERVER_ID = '1209762359875473450'

# Roblox API Endpoint
ROBLOX_API_URL = 'https://api.roblox.com/users/get-by-username?username='

# List of players to monitor
players_to_monitor = ['NKTGlobal', '4hqu', '3hqu']

intents = discord.Intents.default()
intents.members = True
intents.messages = True  # Add this line to enable MESSAGE_CONTENT intent
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    # Start monitoring for players joining games
    check_players.start()

@tasks.loop(seconds=30)  # Check every 30 seconds
async def check_players():
    for player in players_to_monitor:
        player_data = requests.get(ROBLOX_API_URL + player)
        if player_data.status_code == 200:
            player_id = player_data.json()['Id']
            game_info = requests.get(f'https://api.roblox.com/users/{player_id}/currently-playing')
            if game_info.status_code == 200:
                game_name = game_info.json()['Game']['Name']
                guild = bot.get_guild(int(SERVER_ID))
                if guild:
                    channel = discord.utils.get(guild.text_channels, name='general')
                    if channel:
                        await channel.send(f'{player} is playing {game_name}!')

@bot.event
async def on_error(event, *args, **kwargs):
    print('An error occurred!')

# Run the bot
bot.run(TOKEN)
