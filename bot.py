import discord
import time
import asyncio

# server id = 277902232761139207

messages = joined = 0


def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


token = read_token()

client = discord.Client()


async def update_stats():
    await client.wait_until_ready()
    global messages, joined

    while not client.is_closed():
        try:
            with open("stats.txt", "a") as f:
                f.write(f"Time:  {int(time.time())}, Messages: {messages}, Members Joined: {joined}\n")

                messages = 0
                joined = 0

                await asyncio.sleep(86400)
        except Exception as e:
            print(e)
            await asyncio.sleep(86400)


''''@client.event
async def on_member_update(before, after):
    n = after.nick
    if n:
        if n.lower().count("NaRwHaL") > 0:
            last = before.nick
            if last:
                after.edit(nick=last)
            else:
                await after.edit(nick="Not tonight brother")'''


@client.event
async def on_member_join(member):
    global joined
    joined += 1
    for channel in member.server.channels:
        if str(channel) == "general":
            await client.send_message(f"""Welcome to the server {member.mention}""")


@client.event
async def on_message(message):
    global messages
    messages += 1
    id = client.get_guild(277902232761139207)
    channels = ["commands"]
    valid_users = ["NaRwHaL#9942"]

    if message.content == "!help":
        embed = discord.Embed(title="BOT help", description="Some useful commands")
        embed.add_field(name="!hello", value="Greets the user")
        embed.add_field(name="!user", value="Prints number of users")
        await message.channel.send(content=None, embed=embed)

    if str(message.channel) in channels and str(message.author) in valid_users:
        if message.content.startswith('!hello'):
            await message.channel.send("Hi")
        elif message.content == "!users":
            await message.channel.send(f"""Number of Members: {id.member_count}""")
    else:
        print(f"""User: {message.author} tried to do command {message.content}, in channel {message.channel}""")


client.loop.create_task(update_stats())
client.run(token)
