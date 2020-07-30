# -*- coding: utf-8 -*-
#add lib here
import os
#import json
import wikipedia
import discord
from discord import utils
from discord.ext import commands


prefix = '!'                                    #var for prefix

client = commands.Bot(command_prefix = prefix)  #add prefix

client.remove_command('help')                   #remove default help command


actdata = 'Поймай хвост'                        #active info
token = os.environ.get('DisToken')              #get token
debug = True                                    #debug mode
roleid = 677605549478510614                     #access role
categoryid = 678251330040627228                 #private-room category
voiceid = 678249786859585537                    #channel id for Add room
partroleid = 695628636971204700                 #role of partner
partrolecanid = 696422735135375530              #who can add partner role
bumpbot = 315926021457051650                    #id of bump bot(need for ping command)
messbumpbot = 'Pong!'                           #response of bump bot


@client.event
async def on_ready():

    await client.change_presence(               #set activity
        activity=discord.Activity(
            name=actdata, 
            type=discord.ActivityType.playing
            )
        )

    print('logged on as {0.user}!'.format(client))

@client.event
async def on_message(message):
    #delete message from bump bot with content in var messbumpbot
    if message.author.id == bumpbot and message.content[:] == messbumpbot:
        await message.delete()

    #send message content for check if it command
    await client.process_commands(message)

#help command
@client.command()
async def help(ctx):
    await ctx.send('**Команды бота** \n *Для выполнения команды необходимо перед её названием поставить* `' + prefix + '` \n :gear: *В разработке* :gear:')
    
    role_q = client.get_guild(ctx.guild.id).get_role(roleid)
    role_w = client.get_guild(ctx.guild.id).get_role(partrolecanid)
    haverole = ctx.author.roles
    if role_q in haverole or role_w in haverole:
        await ctx.author.send('**А для тебя есть ещё дополнительные команды :3** \n *Для выполнения команды необходимо перед её названием поставить* `' + prefix + '` \n `s` Бот повторит за тобой \n `sd` Бот тоже повторит за тобой, но теперь уже удалит исходное сообщение \n `partner @user` при использовании этой команды, вы объявляете о сотрудничестве. @user - это пользователь, с которым вы будете сотрудничать')

#say command
@client.command()
async def s(ctx, *args):
    role_q = client.get_guild(ctx.guild.id).get_role(roleid)
    role_w = client.get_guild(ctx.guild.id).get_role(partrolecanid)
    haverole = ctx.author.roles
    if role_q in haverole or role_w in haverole:
        lens = len(prefix) + len('s') + len(' ')
        response = ctx.message.content[lens:]
        await ctx.send(response)

#say and delete command
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

#add partner role command
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

#ping command
@client.command()
async def ping(ctx):
    botping = round(client.latency * 1000)
    await ctx.send('Состаяние бота: работает исправно :white_check_mark: \nЗадержка интернет соеденения:' + str(botping) + ' ms')

#execute command
'''
@client.command()
async def execute(ctx):
    role_q = client.get_guild(ctx.guild.id).get_role(roleid)
    haverole = ctx.author.roles
    if role_q in haverole:
        if 'os' in ctx.message.content[:] or 'token' in ctx.message.content[:]:
            await ctx.send('Данная инструкция не может быть выполнена, так как она может повлиять на работоспособность бота')
            await ctx.message.add_reaction('⛔')
        else:
            eval(ctx.message.content[:], globals=None, locals=None)
            await ctx.add_reaction('✅')
'''
#edit message command(not work in production)
'''
@client.command()
async def ed(ctx):
    message = await client.get_channel(678228305131995176).fetch_message(684473465054822432)

    await message.edit(ctx.message.content)
'''
@client.command()
async def wiki(ctx, *, args):
    try:
        wikipedia.set_lang("ru")
        new_page = wikipedia.page(f'{args}')
        summ = wikipedia.summary(f'{args}', sentences=5)
        embed = discord.Embed(title=new_page.title, description=f"{summ}", color=0xc582ff)
        embed.add_field(name="Для полного ознакомления со статьей, перейдите по ссылке:", value=f"[M]({new_page.url})")
        await ctx.send(embed=embed)
    except Exception:
        return await ctx.send('Неоднозначный аргумент, уточните статью', delete_after=10)


#private room code
#-------------begin---------------
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
#-------------end------------------


#reaction-role code
#note:
#you can use only external emoji
#-----------------begin----------
messageID01 = 685103322683670537    #id of message with reactions
messageID02 = 685103723361468446
messageID03 = 696789901911392347

@client.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    
    #if it message number 1
    if message_id == messageID01:

        #get server id
        guild_id = payload.guild_id

        #get server by id
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)
        
        #add var for role
        role = None

        #reaction number 1
        if payload.emoji.name == 'book4':
            #get role
            role = discord.utils.get(guild.roles, name = 'Читатель')
        #reaction number 2
        elif payload.emoji.name == 'tv4':
            #get role
            role = discord.utils.get(guild.roles, name = 'Зритель')
        
        #if all ok
        if role is not None:
            #get member
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            #IF ALL OK
            if member is not None:
                #give role
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

#here we delete role from member if he remove reaction
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
                #here we delete role
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
#-----------------end---------------



#start bot
client.run(token)