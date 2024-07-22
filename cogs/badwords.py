from discord.ext import commands
from discord.ext.commands import Context
import discord


class Badwords(commands.Cog, name="badwords detecter"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.bad_words = ["fuck", "nigga", "asshole", "Fuck off", "stfu", "nigger", "blackass", "ass", "rape", "raped", "nude", "sex", "porn", "sexual", "nudity", "nsfw", "shit", "naked", "naked woman" ]

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        for word in self.bad_words:
            if word in message.content.lower():
                await message.delete()
                embed = discord.Embed(title="Bad Word Detected", description=f"Your message contained a bad word, {message.author.mention}. Please refrain from using such language.", color=0xff0000)
                await message.channel.send(embed=embed, delete_after=5)

async def setup(bot) -> None:
    await bot.add_cog(Badwords(bot))