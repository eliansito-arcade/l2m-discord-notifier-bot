import os
import sys
from dotenv import load_dotenv
import discord
from discord import FFmpegPCMAudio
from utils import set_channel, Boss
import asyncio
from datetime import datetime as dt
import numpy as np

load_dotenv()
SOUND_PATH = os.getenv('SOUND_PATH')
SOUND_EXTENSION = os.getenv('SOUND_EXTENSION')
TOKEN = sys.argv[1]
CHANNEL = sys.argv[2]

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

global_events = np.genfromtxt('./assets/data/sound_global_events.csv', names=True, delimiter=',', dtype=None, encoding='utf8')

async def play_sound(vc, sound_name):
    source = FFmpegPCMAudio(source=SOUND_PATH+sound_name+SOUND_EXTENSION)
    vc.play(source)
    while vc.is_playing():
        await asyncio.sleep(1)

def load_bosses():
    with open("./assets/data/database",'r',encoding = 'utf-8') as file:
        lines = file.readlines()
        bosses = dict()
        for line in lines:
            boss = Boss.from_export_str(line.strip())
            bosses[boss.name]=boss
        return bosses

async def sound_global_events(hour, minute, vc):
    for (sound_name, globar_hour, globar_minute) in global_events:
        if hour == globar_hour and minute == globar_minute:
            await play_sound(vc, sound_name)
    
async def check_1m_for_sound_notification(vc):
    current_time = dt.now()
    await sound_global_events(current_time.hour, current_time.minute, vc) # ! notifications

    bosses = load_bosses()
    if len(bosses.values()) > 0:
        sorted_bosses = sorted(bosses.values())
        
        soon_bosses = []
        appeared_bosses = []
        for boss in sorted_bosses:
            (hours, minutes, _, is_valid) = boss.last_time()
            if is_valid and hours == 0:
                if minutes == 5:
                    soon_bosses.append(boss)
                elif minutes == 0:
                    appeared_bosses.append(boss)
                else:
                    pass
        
        for boss in soon_bosses:
            await play_sound(vc, boss.sound_5min)  # ! notifications
        for boss in appeared_bosses:
            await play_sound(vc, boss.sound_appear)  # ! notifications

async def sound_notification():
    await client.wait_until_ready()
    voice_channel = set_channel(client, CHANNEL, True)
    vc = await voice_channel.connect()
    while not client.is_closed():
        await check_1m_for_sound_notification(vc)
        await asyncio.sleep(60) # task runs every 1min = 60 seconds

client.loop.create_task(sound_notification())
client.run(TOKEN)

# python sound-bot.py TOKEN CHANNEL
# Voice Boss Notifier | РБ