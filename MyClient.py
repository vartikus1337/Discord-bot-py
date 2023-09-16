import discord

from discord import Member, Message, VoiceState, flags
from discord.ext import voice_recv

from config import TOKEN


class MyClient(discord.Client):
    def __init__(self, intents: flags.Intents):
        super().__init__(intents=intents)
        self.check_speak = False
        self.voice_client = None

    async def on_ready(self):
        print(f'{self.user.name} has connected to Discord!')

    async def on_member_join(self, member: Member):
        await member.send(f'Hi {member.name}, welcome to {member.guild.name}')
        await member.guild.system_channel.send(f'Welcome {member.name}!')

    async def on_message(self, message: Message):
        if message.author == self.user: return
        if message.content == 'check_speak': await message.channel.send(self.check_speak); return
        await message.channel.send(f'{message.author.name} сказал: {message.content}')

    def checked_speak(self, user, data):
        self.check_speak = True

    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState):
        if before.channel is None and after.channel is not None and not after.channel.guild.voice_client:
            voice_channel = self.get_channel(after.channel.id)
            self.voice_client = await voice_channel.connect(cls=voice_recv.VoiceRecvClient)
            self.voice_client.listen(voice_recv.BasicSink(self.checked_speak))
        elif before.channel is not None and after.channel is None and before.channel.guild.voice_client:
            self.check_speak = False; await member.guild.voice_client.disconnect(); await client.close()


client = MyClient(intents=discord.Intents.all())
client.run(TOKEN)
