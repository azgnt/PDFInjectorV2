import discord

client = discord.Client()

# Replace 'YOUR_TOKEN' with your bot's token
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        await message.channel.send('Hello! How can I help you?')

client.run('YOUR_TOKEN')
