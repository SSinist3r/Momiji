from modules import permissions
from discord.ext import commands


class AIMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="aimod_add", brief="Ban a word")
    @commands.check(permissions.is_admin)
    @commands.check(permissions.is_not_ignored)
    @commands.guild_only()
    async def aimod_add(self, ctx, *, word):
        """
        This command will add a passed string into a blacklist.
        Every message will be checked for this string,
        and if the message contains this string,
        the message will be automatically deleted.
        Checks are case-insensitive.
        """

        try:
            await ctx.message.delete()
        except:
            pass

        await self.bot.db.execute("INSERT INTO aimod_blacklist VALUES (?)", [str(word).lower().strip()])
        await self.bot.db.commit()

        await ctx.send(":ok_hand:", delete_after=3)

    async def content_filter(self, message):
        async with await self.bot.db.execute("SELECT word FROM aimod_blacklist") as cursor:
            aimod_blacklist = await cursor.fetchall()

        for word in aimod_blacklist:
            if not (word[0] in message.content.lower()):
                continue

            try:
                await message.delete()
            except Exception as e:
                print(e)

    @commands.Cog.listener()
    async def on_message(self, message):
        await self.content_filter(message)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        await self.content_filter(after)


def setup(bot):
    bot.add_cog(AIMod(bot))
