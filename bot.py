# -*- coding: utf-8 -*-

import os
import discord
from discord import utils
from discord.ext import commands


prefix = '!'

client = commands.Bot(command_prefix = prefix)

client.remove_command('help')


actdata = 'Поймай хвост'
token = os.environ.get('DisToken')
debug = True
prefix = '!'
roleid = 677605549478510614
categoryid = 678251330040627228
voiceid = 678249786859585537
partroleid = 695628636971204700
partrolecanid = 696422735135375530
bumpbot = 315926021457051650
messbumpbot = 'Pong!'


@client.event
async def on_ready():

    await client.change_presence(
        activity=discord.Activity(
            name=actdata, 
            type=discord.ActivityType.playing
            )
        )

    print('logged on as {0.user}!'.format(client))

@client.event
async def on_message(message):

    if message.author.id == bumpbot and message.content[:] == messbumpbot:
        await message.delete()

    await client.process_commands(message)

@client.command()
async def help(ctx):
    await ctx.send('**Команды бота** \n *Для выполнения команды необходимо перед её названием поставить* `' + prefix + '` \n :gear: *В разработке* :gear:')
    
    role_q = client.get_guild(ctx.guild.id).get_role(roleid)
    role_w = client.get_guild(ctx.guild.id).get_role(partrolecanid)
    haverole = ctx.author.roles
    if role_q in haverole or role_w in haverole:
        await ctx.author.send('**А для тебя есть ещё дополнительные команды :3** \n *Для выполнения команды необходимо перед её названием поставить* `' + prefix + '` \n `s` Бот повторит за тобой \n `sd` Бот тоже повторит за тобой, но теперь уже удалит исходное сообщение \n `partner @user` при использовании этой команды, вы объявляете о сотрудничестве. @user - это пользователь, с которым вы будете сотрудничать')

@client.command()
async def s(ctx, *args):
    role_q = client.get_guild(ctx.guild.id).get_role(roleid)
    role_w = client.get_guild(ctx.guild.id).get_role(partrolecanid)
    haverole = ctx.author.roles
    if role_q in haverole or role_w in haverole:
        lens = len(prefix) + len('s') + len(' ')
        response = ctx.message.content[lens:]
        await ctx.send(response)

@client.command()
async def sd(ctx, *args):
    role_q = client.get_guild(ctx.guild.id).get_role(roleid)
    role_w = client.get_guild(ctx.guild.id).get_role(partrolecanid)
    haverole = ctx.author.roles
    if role_q in haverole or role_w in haverole:
        lens = len(prefix) + len('sd') + len(' ')
        response = ctx.message.content[lens:]
        await ctx.send(response)
        await ctx.message.delete()

@client.command()
async def partner(ctx):
    role_q = client.get_guild(ctx.guild.id).get_role(roleid)
    role_w = client.get_guild(ctx.guild.id).get_role(partrolecanid)
    haverole = ctx.author.roles
    if role_q in haverole or role_w in haverole:
        role = discord.utils.get(ctx.guild.roles, id = partroleid)
        cont = ctx.message.content[:]
        conts = cont.split('<@!')
        partid = conts[1][:len(conts[1]) - 1]
        partid = int(partid)
        partner = discord.utils.find(lambda m : m.id == partid, ctx.guild.members)
        await partner.add_roles(role)
        await ctx.message.add_reaction('✅')
        await ctx.message.add_reaction('🤝')

@client.command()
async def ping(ctx):
    botping = round(client.latency * 1000)
    await ctx.send('Состаяние бота: работает исправно :white_check_mark: \nЗадержка интернет соеденения:' + str(botping) + ' ms')

@client.event
async def on_voice_state_update(member, before, after):

    if(member.bot):
        return

    if(after.channel and after.channel.category.id == categoryid and after.channel.id == voiceid):

        voiceChannel = await member.guild.create_voice_channel(
            f"SHIRO ┇ {member.name}", 
            overwrites={
                member: discord.PermissionOverwrite(connect=True, speak=True, move_members=True, manage_channels=True, manage_roles=True, use_voice_activation=True)
                }, 
            category=after.channel.category, 
            reason="Голосовая комната."
        )

        await member.edit(voice_channel=voiceChannel, reason="Перенос участника в его голосовую комнату.")

    for channel in client.get_channel(voiceid).category.voice_channels:

        if(channel.id == voiceid or len(channel.members) != 0): continue
        await channel.delete(reason="В голосовой комнате 0 людей!")

messageID01 = 685103322683670537
messageID02 = 685103723361468446
messageID03 = 696789901911392347

@client.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    
    if message_id == messageID01:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)
        
        role = None

        if payload.emoji.name == 'book4':
            role = discord.utils.get(guild.roles, name = 'Читатель')
        elif payload.emoji.name == 'tv4':
            role = discord.utils.get(guild.roles, name = 'Зритель')
        
        if role is not None:
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            if member is not None:
                await member.add_roles(role)
            
            
    if message_id == messageID02:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)
        
        role = None

        if payload.emoji.name == 'male4':
            role = discord.utils.get(guild.roles, name = 'Жрец')
        elif payload.emoji.name == 'female4':
            role = discord.utils.get(guild.roles, name = 'Жрица')
        
        if role is not None:
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            if member is not None:
                await member.add_roles(role)


    if message_id == messageID03:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)
        
        role = None

        if payload.emoji.name == 'butterwow':
            role = discord.utils.get(guild.roles, name = '🦋')
        
        if role is not None:
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            if member is not None:
                await member.add_roles(role)

@client.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    
    if message_id == messageID01:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)
        
        role = None

        if payload.emoji.name == 'book4':
            role = discord.utils.get(guild.roles, name = 'Читатель')
        elif payload.emoji.name == 'tv4':
            role = discord.utils.get(guild.roles, name = 'Зритель')
        
        if role is not None:
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            if member is not None:
                await member.remove_roles(role)
            
            
    if message_id == messageID02:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)
        
        role = None

        if payload.emoji.name == 'male4':
            role = discord.utils.get(guild.roles, name = 'Жрец')
        elif payload.emoji.name == 'female4':
            role = discord.utils.get(guild.roles, name = 'Жрица')
        
        if role is not None:
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            if member is not None:
                await member.remove_roles(role)
            
            
    if message_id == messageID03:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)
        
        role = None

        if payload.emoji.name == 'butterwow':
            role = discord.utils.get(guild.roles, name = '🦋')
        if role is not None:
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            if member is not None:
                await member.remove_roles(role)





client.run(token)
