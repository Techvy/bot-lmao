import discord
from discord.ext import commands

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="help", description="Get help with the bot")
    async def help(self, ctx: commands.Context):
        embed = discord.Embed(title="__Help Menu__:", description="**Categories**\n- <:moderation:1263092343461117974> Moderation\n- <:general:1263092233079361607> General\n- <:utility:1263092448352145419> Utility\n- <:fun:1263166738762174588> Fun", color=0x6064f4)
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.set_footer(text="Select a category from the dropdown menu")
        select = discord.ui.Select(placeholder="Choose a category to view its commands")

        select.add_option(label="General", emoji="<:general:1263092233079361607>", description="General commands")
        select.add_option(label="Moderation", emoji="<:moderation:1263092343461117974>", description="Moderation commands")
        select.add_option(label="Utility", emoji="<:utility:1263092448352145419>", description="Utility commands")
        select.add_option(label="Fun", emoji="<:fun:1263166738762174588>", description="Fun commands")

        async def select_callback(interaction):
            if select.values[0] == "General":
                embed.title = "**<:general:1263092233079361607> __General Category__**"
                embed.description = ""
                embed.clear_fields()
                embed.add_field(name="Commands:", value="""  
- `Botinfo`
- `Serverinfo`
- `Ping`
- `Levels`
- `lvltop`
- `Invtop`
- `Suggest`
- `Mcstatus`
- `Help`
""", inline=False)
            elif select.values[0] == "Moderation":
                embed.title = "<:moderation:1263092343461117974> **__Moderation Category__**"
                embed.description = ""
                embed.clear_fields()
                embed.add_field(name="Commands:", value="""
- `Mute`
- `Unmute`
- `Deafen`
- `Undeafen`
- `Warn`
- `Unwarn`
- `Timeout`
- `Untimeout`
- `Ban`
- `Unban`
""", inline=False)
            elif select.values[0] == "Utility":
                embed.title = "**<:utility:1263092448352145419> __Utility Category__**"
                embed.description = ""
                embed.clear_fields()
                embed.add_field(name="Commands:", value="""
- `Nick`
- `Unnick`
- `Lock`
- `Unlock`
- `Slowmode`
- `noslowmode`
- `Embed`
- `Say`
- `Reload`
- `Unreload` 
- `Archive`
""", inline=False)
            elif select.values[0] == "Fun":
                embed.title = "**<:fun:1263166738762174588> __Fun Category__**"
                embed.description = ""
                embed.clear_fields()
                embed.add_field(name="Commands:", value="""
- `TicTacToe`
""", inline=False)
            await interaction.response.edit_message(embed=embed)

        select.callback = select_callback

        view = discord.ui.View()
        view.add_item(select)

        if ctx.interaction:
            await ctx.send(embed=embed, view=view)
        else:
            await ctx.send(embed=embed, view=view)

async def setup(bot) -> None:
    await bot.add_cog(HelpCog(bot))