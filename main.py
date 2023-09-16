import discord
from discord.ext import voice_recv
import asyncio
from discord import Member, Message, VoiceState
from config import TOKEN, GUILD_ID, TEXT_CHANNEL_ID


client = discord.Client(intents=discord.Intents.all())
    
speaking = False

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')


@client.event
async def on_member_join(member: Member):
    await member.send(f'Hi {member.name}, welcome to {member.guild.name}')
    # await member.kick()
    await member.guild.system_channel.send(f'Welcome {member.global_name}!')


@client.event
async def on_message(message: Message):
    if message.author == client.user:
        return
    if message.content == '!узнать speaking':
        await message.channel.send(f'{speaking}')
        return
    if message.content == '!отключить слушателя':
        voice_client.stop_listening() 
    await message.channel.send(f'{message.author.name} сказал: {message.content}')
        

@client.event
async def on_voice_state_update(member: Member, before: VoiceState, after: VoiceState):
    if before.channel is None and after.channel is not None and not after.channel.guild.voice_client:
        voice_channel = client.get_channel(after.channel.id)
        voice_client = await voice_channel.connect(cls=voice_recv.VoiceRecvClient)
        print('Мешаю!')
        global speaking
        def callback(user, data: voice_recv.VoiceData):global speaking; speaking = True
        voice_client.listen(voice_recv.BasicSink(callback))
        await asyncio.sleep(5)
        voice_client.stop_listening() # Остановка
        speaking = False
        await client.get_channel(TEXT_CHANNEL_ID).send(f'{member.global_name} заговорил в {after.channel.name}!')
    elif before.channel is not None and after.channel is None and before.channel.guild.voice_client:
        await before.channel.guild.voice_client.disconnect()
        await client.close()


client.run(TOKEN)