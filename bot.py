import asyncio
import os
import platform
import matplotlib.pyplot as plt
import discord
from discord.ext import commands
from wand.image import Image as WandImage



client = commands.Bot(command_prefix='!', intents=discord.Intents.all())


@client.command()
async def hello(ctx):
    await ctx.send('Hello.')


@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')
    print(f'Bot ID: {client.user.id}')
    print('------')
    print(f'Discord.py Version: {discord.__version__}')
    print(f'Python Version: {platform.python_version()}')
    print(f'Running on: {platform.system()} {platform.release()} ({os.name})')
    print('------')


@client.command(aliases=['stop'])
async def shutdown(ctx):
    await ctx.send('Shutting down.')
    await client.close()


@client.command(aliases=['whois', 'who', 'user', 'info'])
async def userinfo(ctx, member: discord.Member = None):
    if member == None:
        member = ctx.author
    embed = discord.Embed(title="User Info", description=f'This is the info of {member.mention}',
                          color=discord.Color.dark_blue(), timestamp=ctx.message.created_at)
    embed.set_thumbnail(url=member.avatar)
    embed.add_field(name="Username", value=member.name, inline=False)
    embed.add_field(name='Nickname', value=member.display_name)
    embed.add_field(name='ID', value=member.id)
    embed.add_field(name='Status', value=member.status)
    embed.add_field(name='Account Created', value=member.created_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'))
    embed.add_field(name='Joined Server', value=member.joined_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'))
    embed.add_field(name='Role', value=member.top_role.mention, inline=False)
    embed.set_footer(text=f'Requested by {ctx.author.name}')
    embed.add_field(name='Messages', value='0')

    await ctx.send(embed=embed)

@client.command(aliases=['labs', 'lab'])
async def lab_test(ctx):
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and int(msg.content) in range(1, 13)

    await ctx.send("Do you want to look at particular lab instructions? Please enter a number between 1 and 12.")
    try:
        msg = await client.wait_for("message", check=check, timeout=30)
        num = int(msg.content)
        with WandImage(filename=f'./Labs/Lab {num}.pdf', resolution=200) as img:
            files = []
            for i, page in enumerate(img.sequence):
                with WandImage(page) as single_page:
                    single_page.format = 'png'
                    single_page.save(filename=f'page{i}.png')
                    files.append(discord.File(f'page{i}.png'))
                    if len(files) == 10:
                        await ctx.send(files=files)
                        files = []
            if files:
                await ctx.send(files=files)
    except asyncio.TimeoutError:
        await ctx.send("Sorry, you didn't reply in time!")





client.run('MTE3OTAwMTY4MzE1MDM4OTI2OQ.G2WYB-.96LfRnHg_TCdafaFg-Rfhh2fWFlIDsoS5YZds0')
