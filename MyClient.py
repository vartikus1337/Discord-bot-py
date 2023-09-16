import discord, argparse

from discord import Member, Message, VoiceState, flags
from discord.ext import voice_recv


class MyClient(discord.Client):
    def __init__(self, intents: flags.Intents):
        super().__init__(intents=intents)

    async def on_ready(self):
        print(f'{self.user.name} has connected to Discord!')

    async def on_member_join(self, member: Member):
        await member.send(f'Hi {member.name}, welcome to {member.guild.name}')
        await member.guild.system_channel.send(f'Welcome {member.name}!')

    async def on_message(self, message: Message):
        if message.author == self.user: return
        await message.channel.send(f'{message.author.name} сказал: {message.content}')

    def checked_speak(self, user, data: voice_recv.VoiceData):
        data = data.packet.extension_data.get(voice_recv.ExtensionID.audio_power)
        power = 127 - (int.from_bytes(data) & 127)
        print('#' * int(power * (79/128)))

    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState):
        if before.channel is None and after.channel is not None and not after.channel.guild.voice_client:
            voice_channel = self.get_channel(after.channel.id)
            voice_client = await voice_channel.connect(cls=voice_recv.VoiceRecvClient)
            voice_client.listen(voice_recv.BasicSink(self.checked_speak))
        elif before.channel is not None and after.channel is None and before.channel.guild.voice_client:
            await member.guild.voice_client.disconnect(); await self.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--token', help='Token here')
    args = parser.parse_args()
    client = MyClient(intents=discord.Intents.all())
    client.run(args.token)


if __name__ == '__main__':
    main()
