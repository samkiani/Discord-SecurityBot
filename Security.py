import os
import discord
from discord.ext import commands
from discord.utils import get
from asyncio import sleep
from datetime import datetime
from colorama import Fore


class CONFIG:
        TOKEN = '' #str
        PREFIX = '' #str
        GUILD_ID = 0 #int
        CHANNEL_ID = 0 #int


client = commands.Bot(command_prefix = CONFIG.PREFIX , help_command = None , intents = discord.Intents.all())


@client.event
async def on_ready():
        guild = client.get_guild(CONFIG.GUILD_ID)
        channel = guild.get_channel(CONFIG.CHANNEL_ID)
        await channel.connect(reconnect = True)
        print(datetime.today().replace(microsecond=0) ,'\n\nBot is online\nDeveloped by ErfanNJZ')

@client.event
async def on_ready():
        if os.name == 'nt':
                os.system('cls')
        else:
                os.system('clear')

        print(Fore.GREEN + """


░██████╗███████╗░█████╗░██╗░░░██╗██████╗░██╗████████╗████████╗██╗░░░██╗
██╔════╝██╔════╝██╔══██╗██║░░░██║██╔══██╗██║╚══██╔══╝╚══██╔══╝╚██╗░██╔╝
╚█████╗░█████╗░░██║░░╚═╝██║░░░██║██████╔╝██║░░░██║░░░░░░██║░░░░╚████╔╝░
░╚═══██╗██╔══╝░░██║░░██╗██║░░░██║██╔══██╗██║░░░██║░░░░░░██║░░░░░╚██╔╝░░
██████╔╝███████╗╚█████╔╝╚██████╔╝██║░░██║██║░░░██║░░░░░░██║░░░░░░██║░░░
╚═════╝░╚══════╝░╚════╝░░╚═════╝░╚═╝░░╚═╝╚═╝░░░╚═╝░░░░░░╚═╝░░░░░░╚═╝░░░  
-----------------------------------------------------------------------
        """ + Fore.RESET)
        print(datetime.today().replace(microsecond=0) ,'\n\nBot Is Online\nDeveloped by ErfanNJZ')


async def change_presence():
        await client.wait_until_ready()
        guild = client.get_guild(CONFIG.GUILD_ID)
        while not client.is_closed():
            botcounter = len([i for i in guild.members if i.bot])
            members = guild.member_count - botcounter
            botscount =  botcounter - 1
            counter = 0
            for v in guild.voice_channels:
                    onmic = v.members
                    counter = counter + len(onmic)
            statuses = [f'{guild.name} Server ►►► Developed by Nex1x' , f'{members} members' , f'{botscount} bots' , f'{counter} onmic']
            counter = 0
            for s in statuses:
                    await client.change_presence(activity = discord.Activity(type = discord.ActivityType.watching , name = s))
                    await sleep(5)
                    continue


@client.event
async def on_command_error(ctx , error):
        if isinstance(error , commands.CommandNotFound):
                pass
        elif isinstance(error, commands.CommandOnCooldown):
                await ctx.send(f"**On cooldown , wait {error.retry_after : .2f} seconds!**" , delete_after = 5)


@client.event
async def on_message(message):
        if "discord.gg" in message.content.lower() or "@everyone" in message.content.lower() or "@here" in message.content.lower():
                if not message.author.guild_permissions.administrator:
                        await message.delete()
        else:
                await client.process_commands(message)


@client.command(name = 'info')
@commands.has_permissions(administrator = True) 
async def info(ctx , user: discord.Member):
        embed = discord.Embed(title = 'User Info' , colour = 0x66F948)
        embed.add_field(name = 'Nickname :' , value = f'`{user.nick}`' , inline = False)
        embed.add_field(name = 'Username :' , value = f'`{user}`' , inline = False)
        embed.add_field(name = 'ID :' , value = f'`{user.id}`' , inline = False)
        embed.add_field(name = 'Status :' , value = f'`{user.status}`' , inline = False)
        embed.add_field(name = 'Account Created In :' , value = f'`{user.created_at:%A, %d %B %Y %H:%M:%S}`' , inline = False)
        embed.add_field(name = 'Joined Server In :' , value = f'`{user.joined_at:%A, %d %B %Y %H:%M:%S}`' , inline = False)
        embed.set_thumbnail(url = user.avatar_url)
        await ctx.send(embed = embed)


@client.command(name = 'avatar')
@commands.has_permissions(administrator = True) 
async def avatar(ctx , user: discord.Member):
        embed = discord.Embed(title = 'User Avatar' , colour = 0x66F948)
        embed.add_field(name = 'Username :' , value = f'`{user}`')
        embed.set_image(url = user.avatar_url)
        await ctx.send(embed = embed)


@client.command(name = 'clear')
@commands.has_permissions(manage_messages = True)
@commands.cooldown(1 , 20 , commands.BucketType.user)
async def clear(ctx , count):
        count = int(count)
        await ctx.channel.purge(limit = count + 1)
        await ctx.send(f'>>> {count} Messages deleted' , delete_after = 5)


@client.command(name= 'kick')
@commands.has_permissions(kick_members = True)
async def kick(ctx , user: discord.Member , * , reason):
    await ctx.guild.kick(user , reason = reason)
    await ctx.send(f'>>> {user.mention}  kicked.')


@client.command(name = 'ban')
@commands.has_permissions(ban_members = True)
async def ban(ctx , user: discord.Member , * , reason):
        await ctx.guild.ban(user , reason = reason)
        await ctx.send(f'>>> {user.mention}  banned.')


@client.command(name = 'unban')
@commands.has_permissions(ban_members = True)
async def unban(ctx , user : discord.User):
        guild = ctx.guild
        bans = await ctx.guild.bans()
        for i in bans:
                if user in i:  
                        await guild.unban(user = user)
                        await ctx.send(f'>>> {user.mention}  unbanned.')


@client.command(name = 'unbanall')
@commands.has_permissions(administrator = True)
async def unbanall(ctx):
        guild = ctx.guild
        bans = await ctx.guild.bans()
        for banEntry in bans:
                await guild.unban(user = banEntry.user)
        await ctx.send('>>> All users unbanned.')


@client.command(name = 'shutdown')
@commands.is_owner()
async def shutdown(ctx):
        await ctx.client.logout()



client.loop.create_task(change_presence())
client.run(CONFIG.TOKEN)