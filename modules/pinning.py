import time
import discord
import asyncio
from modules import dbhandler

async def on_raw_reaction_add(client, raw_reaction):
    try:
        guildpinchannel = await dbhandler.query(["SELECT value FROM config WHERE setting = ? AND parent = ?", ["guildpinchannelid", str(raw_reaction.guild_id)]])
        if guildpinchannel:
            if int((guildpinchannel)[0][0]) != raw_reaction.channel_id:
                channell = client.get_channel(raw_reaction.channel_id)
                message = await channell.fetch_message(raw_reaction.message_id)
                reactions = message.reactions
                for reaction in reactions:
                    # onereact = {
                    # 	'count': int(reaction.count),
                    # 	'emoji': str(reaction.emoji),
                    # }
                    if reaction.count >= 6:
                        if not (await dbhandler.query(["SELECT value FROM pinchannelblacklist WHERE value = ?", [str(raw_reaction.channel_id)]])):
                            if not (await dbhandler.query(["SELECT messageid FROM pinned WHERE messageid = ?", [str(raw_reaction.message_id)]])):
                                await dbhandler.query(["INSERT INTO pinned VALUES (?)", [str(raw_reaction.message_id)]])
                                pin_channel_object = client.get_channel(
                                    int((guildpinchannel)[0][0]))
                                await pin_channel_object.send(content="<#%s> %s" % (str(raw_reaction.channel_id), str(reaction.emoji)), embed=await messageembed(message))
    except Exception as e:
        print(time.strftime('%X %x %Z'))
        print("in on_raw_reaction_add")
        print(e)


async def messageembed(message):
    if message:
        if message.embeds:
            embed = message.embeds[0]
        else:
            embed = discord.Embed(
                description=message.content,
                color=0xFFFFFF
            )
            if message.attachments:
                attachment = (message.attachments)[0]
                embed.set_image(
                    url=attachment.url
                )
            embed.set_author(
                name=message.author.display_name,
                icon_url=message.author.avatar_url
            )
        return embed
    else:
        return None