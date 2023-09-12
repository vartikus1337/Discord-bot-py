import discord
from config import TOKEN, GUILD_ID

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    guild = client.get_guild(GUILD_ID)
    await guild.text_channels[0].send('Hello world!')

client.run(TOKEN)