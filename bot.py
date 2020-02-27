# -*- coding: utf-8 -*-

import discord
from discord import utils


production = True


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



client.run(DisToken)