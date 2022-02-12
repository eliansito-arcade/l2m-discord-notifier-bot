from utils.utils import Boss

def set_channel(client, required_channel, voice=False):
    for guild in client.guilds:
        channels = guild.channels if not voice else guild.voice_channels
        for c in channels:
            if c.name == required_channel:
                return c

def load_bosses():
    with open("assets/data/database",'r',encoding = 'utf-8') as file:
            lines = file.readlines()
            bosses = {}
            for line in lines:
                boss = Boss.from_export_str(line.strip())
                bosses[boss.name]=boss
            return bosses