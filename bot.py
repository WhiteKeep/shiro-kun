# -*- coding: utf-8 -*-

import discord
from discord import utils


production = False


if production is not True:

    import configer

    DisToken = str(configer.DisToken)
    debug = bool(configer.debug)
    actData = str(configer.actData)
    servId = int(configer.servId)
    roleId = int(configer.roleId)
    voiceID = int(configer.voiceID)
    categoryID = int(configer.categoryID)
    prefix = str(configer.prefix)
    helpName = str(configer.helpName)
    helpData01 = str(configer.helpData01)
    #helpData02 = str(configer.helpData02)
else:
    import config

    DisToken = str(config.DisToken)
    debug = bool(config.debug)
    actData = str(config.actData)
    servId = int(config.servId)
    roleId = int(config.roleId)
    voiceID = int(config.voiceID)
    categoryID = int(config.categoryID)
    prefix = str(config.prefix)
    helpName = str(config.helpName)
    helpData01 = str(config.helpData01)
    #helpData02 = str(config.helpData02)


client = discord.Client()


@client.event
async def on_ready():

    await client.change_presence(
        activity=discord.Activity(
            name=actData, 
            type=discord.ActivityType.playing
            )
        )

    print('logged on as {0.user}!'.format(client))



@client.event
async def on_message(message):

    if debug is True:
        print('Message from {0.author}: {0.content}'.format(message))

    mess = message.content[:]

    if mess == helpName:
        await message.channel.send(helpData01 + '`' + prefix + '`')
        #await message.channel.send(helpData02)

    role_pio = client.get_guild(servId).get_role(roleId)
    whohaverole = message.author.roles
    if role_pio in whohaverole:
        i = 0
        i = len(prefix)
        t = 0
        while i > 0:
            if mess[t] == prefix[t]:
                i = i - 1
                t = t + 1
            else:
                i = 0
        if t == len(prefix):

            mtext = mess[len(prefix):]
            await message.channel.send(mtext)




@client.event
async def on_voice_state_update(member, before, after):
    if(member.bot):return
    if(after.channel and after.channel.category.id == categoryID and after.channel.id == voiceID):

        voiceChannel = await member.guild.create_voice_channel(f"SHIRO ┇ {member.name}", overwrites={
            member: discord.PermissionOverwrite(
                connect=True, speak=True, move_members=True, manage_channels=True, manage_roles=True, use_voice_activation=True)
        }, category=after.channel.category, reason="Голосовая комната.")

        await member.edit(voice_channel=voiceChannel, reason="Перенос участника в его голосовую комнату.")
    for channel in client.get_channel(voiceID).category.voice_channels:
        if(channel.id == voiceID or len(channel.members) != 0): continue
        await channel.delete(reason="В голосовой комнате 0 людей!")
        
        
        
messageID01 = 685103322683670537
messageID02 = 685103723361468446
messageID03 = 696789901911392347

@client.event
async def on_raw_reaction_add(payload):
    print('event')
    message_id = payload.message_id
    
    if message_id == messageID01:
        print('message indetifical01')
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)
        
        role = None

        if payload.emoji.name == 'book4':
            print('ok')
            role = discord.utils.get(guild.roles, name = 'Читатель')
        elif payload.emoji.name == 'tv4':
            role = discord.utils.get(guild.roles, name = 'Зритель')
        
        if role is not None:
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            if member is not None:
                await member.add_roles(role)
                print('done')
            else:
                print('member not found')
        else:
            print('role not found')
            
            
    if message_id == messageID02:
        print('message indetifical02')
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
                print('done')
            else:
                print('member not found')
        else:
            print('role not found')


    if message_id == messageID03:
        print('message indetifical03')
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)
        
        role = None

        if payload.emoji.name == 'butterwow':
            role = discord.utils.get(guild.roles, name = '🦋')
        
        if role is not None:
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            if member is not None:
                await member.add_roles(role)
                print('done')
            else:
                print('member not found')
        else:
            print('role not found')

            
            
            
            
@client.event
async def on_raw_reaction_remove(payload):
    print('event')
    message_id = payload.message_id
    
    if message_id == messageID01:
        print('message indetifical01')
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)
        
        role = None

        if payload.emoji.name == 'book4':
            print('ok')
            role = discord.utils.get(guild.roles, name = 'Читатель')
        elif payload.emoji.name == 'tv4':
            role = discord.utils.get(guild.roles, name = 'Зритель')
        
        if role is not None:
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            if member is not None:
                await member.remove_roles(role)
                print('done')
            else:
                print('member not found')
        else:
            print('role not found')
            
            
    if message_id == messageID02:
        print('message indetifical02')
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
                print('done')
            else:
                print('member not found')
        else:
            print('role not found')
            
            
    if message_id == messageID03:
        print('message indetifical03')
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)
        
        role = None

        if payload.emoji.name == 'butterwow':
            role = discord.utils.get(guild.roles, name = '🦋')
        if role is not None:
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            if member is not None:
                await member.remove_roles(role)
                print('done')
            else:
                print('member not found')
        else:
            print('role not found')


client.run(DisToken)