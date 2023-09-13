import discord
from config import TOKEN, GUILD_ID, TEXT_CHANNEL_ID

client = discord.Client(intents=discord.Intents.all())


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')


@client.event
async def on_member_join(member: discord.Member):
    await member.send(f'Hi {member.name}, welcome to {client.get_guild(GUILD_ID).name}')
    # await member.kick()
    await client.get_channel(TEXT_CHANNEL_ID).send(f'Welcome {member.global_name}!')


client.run(TOKEN)
