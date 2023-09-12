import discord
from config import TOKEN, GUILD_ID

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    print('guilds: ')
    for guild in client.guilds:
        print(f'name: {guild.name} id: {guild.id}')
    # guild = client.get_guild(GUILD_ID)

client.run(TOKEN)