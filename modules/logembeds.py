import discord
import asyncio

async def message_delete(message):
    if message:
        embed = discord.Embed(
            description=message.content,
            color=0xAD6F49
        )
        embed.set_author(
            name="%s#%s | %s | %s" % (message.author.name, message.author.discriminator,
                                      message.author.display_name, str(message.author.id)),
            icon_url=message.author.avatar_url
        )
        embed.set_footer(
            text="Message deleted in #%s" % (message.channel.name)
        )
        return embed
    else:
        return None


async def message_edit(before, after):
    if before:
        embed = discord.Embed(
            description="**Before**:\n%s\n\n**After:**\n%s" % (
                before.content, after.content),
            color=0x9ACDA5
        )
        embed.set_author(
            name="%s#%s | %s | %s" % (before.author.name, before.author.discriminator,
                                      before.author.display_name, str(before.author.id)),
            icon_url=before.author.avatar_url
        )
        embed.set_footer(
            text="Message edited in #%s" % (before.channel.name)
        )
        return embed
    else:
        return None


async def member_join(member):
    if member:
        embed = discord.Embed(
            description="%s\n%s" % (member.mention, str(member.id)),
            color=0x299880
        )
        embed.set_author(
            name="%s#%s" % (member.name, member.discriminator)
        )
        embed.set_footer(
            text="User joined"
        )
        embed.set_thumbnail(url=member.avatar_url)
        return embed
    else:
        return None


async def member_remove(member):
    if member:
        embed = discord.Embed(
            description="%s\n%s" % (member.mention, str(member.id)),
            color=0x523104
        )
        embed.set_author(
            name="%s#%s" % (member.name, member.discriminator)
        )
        embed.set_footer(
            text="User left or got kicked"
        )
        embed.set_thumbnail(url=member.avatar_url)
        return embed
    else:
        return None


async def member_voice_join_left(member, channel, action):
    if member:
        embed = discord.Embed(
            color=0x419400,
            description="has %s **%s**" % (action, channel.name)
        )
        embed.set_author(
            name="%s" % (member.display_name),
            icon_url=member.avatar_url
        )
        return embed
    else:
        return None


async def member_voice_switch(member, beforechannel, afterchannel):
    if member:
        embed = discord.Embed(
            color=0x419400,
            description="has switched from **%s** to **%s**" % (
                beforechannel.name, afterchannel.name)
        )
        embed.set_author(
            name="%s" % (member.display_name),
            icon_url=member.avatar_url
        )
        return embed
    else:
        return None


async def role_change(member, desc):
    if member:
        embed = discord.Embed(
            description=desc,
            color=0xAABBBB
        )
        embed.set_author(
            name="%s#%s | %s | %s" % (member.name, member.discriminator, member.display_name, str(member.id)),
            icon_url=member.avatar_url
        )
        embed.set_footer(
            text="Role Changes"
        )
        return embed
    else:
        return None


async def name_change(user, before, after):
    if user:
        embed = discord.Embed(
            description="**Before**:\n%s\n\n**After:**\n%s" % (before, after),
            color=0xAACCEE
        )
        embed.set_author(
            name="%s#%s | %s" % (user.name, user.discriminator, str(user.id)),
            icon_url=user.avatar_url
        )
        embed.set_footer(
            text="Username Change"
        )
        return embed
    else:
        return None