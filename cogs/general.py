import platform
import random
import json
import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
import aiohttp


class General(commands.Cog, name="general"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.context_menu_user = app_commands.ContextMenu(
            name="Grab ID", callback=self.grab_id
        )
        self.bot.tree.add_command(self.context_menu_user)
        self.context_menu_message = app_commands.ContextMenu(
            name="Remove spoilers", callback=self.remove_spoilers
        )
        self.bot.tree.add_command(self.context_menu_message)

    async def send_cog_help(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(
            title="General Commands",
            description="List of available commands in the General category:",
            color=0x7289DA
        )
        commands_list = []
        for command in self.get_commands():
            commands_list.append(f"**/{command.name}**: {command.description}")

        embed.add_field(name="Commands", value="\n".join(commands_list))
        await interaction.response.edit_message(embed=embed, view=None)

    # Message context menu command
    async def remove_spoilers(
        self, interaction: discord.Interaction, message: discord.Message
    ) -> None:
        """
        Removes the spoilers from the message. This command requires the MESSAGE_CONTENT intent to work properly.

        :param interaction: The application command interaction.
        :param message: The message that is being interacted with.
        """
        spoiler_attachment = None
        for attachment in message.attachments:
            if attachment.is_spoiler():
                spoiler_attachment = attachment
                break
        embed = discord.Embed(
            title="Message without spoilers",
            description=message.content.replace("||", ""),
            color=0xBEBEFE,
        )
        if spoiler_attachment is not None:
            embed.set_image(url=attachment.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    # User context menu command
    async def grab_id(
        self, interaction: discord.Interaction, user: discord.User
    ) -> None:
        """
        Grabs the ID of the user.

        :param interaction: The application command interaction.
        :param user: The user that is being interacted with.
        """
        embed = discord.Embed(
            description=f"The ID of {user.mention} is `{user.id}`.",
            color=0xBEBEFE,
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)


    @commands.hybrid_command(
            name="botinfo",
            description="Get some useful (or not) information about the bot.",
        )
    async def botinfo(self, context: Context) -> None:
            """
            Get some useful (or not) information about the bot.

            :param context: The hybrid command context.
            """
            embed = discord.Embed(
                description="",
                color=0xBEBEFE,
            )
            embed.set_author(
                name="Bot Information",
                icon_url=self.bot.user.avatar.url,  # Add this line
            )
            embed.add_field(name="Owner:", value="**__Blocktune Services__**", inline=True)
            embed.add_field(
                name="Python Version:", value=f"{platform.python_version()}", inline=True
            )
            embed.add_field(
                name="Prefix:",
                value=f"/ (Slash Commands) or {self.bot.config['prefix']} for normal commands",
                inline=False,
            )
            embed.add_field(
                name="",
                value=f"Developed by **__Techvy__**.",
                inline=False,
            )
            embed.add_field(
                name="",
                value=f"*Do /help for more commands*",
                inline=False,
            )
            embed.set_footer(text=f"Requested by {context.author}", icon_url=f"{context.author.display_avatar.url}?size=128")
            await context.send(embed=embed)
    @commands.hybrid_command(
        name="serverinfo",
        description="Get some useful (or not) information about the server.",
    )
    async def serverinfo(self, context: Context) -> None:
        """
        Get some useful (or not) information about the server.

        :param context: The hybrid command context.
        """
        try:
            guild = context.guild
            roles = [role.name for role in guild.roles]
            num_roles = len(roles)
            if num_roles > 50:
                roles = roles[:50]
                roles.append(f">>>> Displaying [50/{num_roles}] Roles")
            roles = ", ".join(roles)
            
            embed = discord.Embed(
                title="**__Server Information__**",
                color=0xBEBEFE
            )
        
            embed.set_thumbnail(url=self.bot.user.avatar.url)
            embed.set_author(
                name="Blocktune Development",
                icon_url=self.bot.user.avatar.url if self.bot.user.avatar else None
            )
            
            # Server Details
            embed.add_field(
                name="**Server Details**",
                value=f"```Name: {guild.name}\nID: {guild.id}\nOwner: {guild.owner}\nCreated at: {guild.created_at.strftime('%Y-%m-%d %H:%M:%S')}```",
                inline=False
            )
            
            # Server Stats
            embed.add_field(
                name="**Server Stats**",
                value=f"```Member Count: {guild.member_count}\nRole Count: {num_roles}\nChannel Count: {len(guild.channels)}\nEmoji Count: {len(guild.emojis)}\nSticker Count: {len(guild.stickers)}```",
                inline=False
            )
            
            # Boosting
            embed.add_field(
                name="**Boosting**",
                value=f"```Level: {guild.premium_tier}\nBoost Count: {guild.premium_subscription_count}```",
                inline=False
            )

            embed.set_footer(text=f"Requested by {context.author}", icon_url=f"{context.author.display_avatar.url}?size=128")
            
            await context.send(embed=embed)
        
        except Exception as e:
            await context.send(f"An error occurred: {e}")

    @commands.hybrid_command(
        name="ping",
        description="Check if the bot is alive.",
    )
    async def ping(self, context: Context) -> None:
        """
        Check if the bot is alive.

        :param context: The hybrid command context.
        """
        embed = discord.Embed(
            title="Pong!",
            description=f"The bot latency is {round(self.bot.latency * 1000)}ms.",
            color=0xBEBEFE,
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="8ball",
        description="Ask any question to the bot.",
    )
    @app_commands.describe(question="The question you want to ask.")
    async def eight_ball(self, context: Context, *, question: str) -> None:
        """
        Ask any question to the bot.

        :param context: The hybrid command context.
        :param question: The question that should be asked by the user.
        """
        answers = [
            "It is certain.",
            "It is decidedly so.",
            "You may rely on it.",
            "Without a doubt.",
            "Yes - definitely.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now",
            "Cannot predict now.",
            "Concentrate and ask again later.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful.",
        ]
        embed = discord.Embed(
            title="8-Ball",
            description=f"**Question:** {question}\n**My Answer:** {random.choice(answers)}",
            color=0xBEBEFE,
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="mcstatus",
        description="Get information about a Minecraft server.",
    )
    async def mcstats(self, context: Context, serverip: str) -> None:
        """
        Get information about a Minecraft server.

        :param context: The hybrid command context.
        :param server_ip: The IP address of the Minecraft server.
        """
        await context.defer()  # This will show "Bot is thinking..." until the command is finished
        
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.mcsrvstat.us/2/{serverip}") as response:
                if response.status != 200:
                    await context.send(f"Could not fetch data for {serverip}. Please make sure the server IP is correct.")
                    return
                
                data = await response.json()
                
                if not data.get("online"):
                    await context.send(f"The server {serverip} is currently offline.", ephemeral=True)
                    return
                
                icon_url = None
                async with session.get(f"https://eu.mc-api.net/v3/server/favicon/{serverip}") as icon_response:
                    if icon_response.status == 200:
                        icon_url = f"https://eu.mc-api.net/v3/server/favicon/{serverip}"
                
                embed = discord.Embed(
                    title=f"**Minecraft Server Stats for __{serverip}__**",
                    color=0x00FF00
                )
                
                # Add server stats to the embed
                embed.add_field(name="Server IP", value=serverip, inline=False)
                embed.add_field(name="Online Players", value=data["players"]["online"], inline=True)
                embed.add_field(name="Max Players", value=data["players"]["max"], inline=True)
                embed.add_field(name="Version", value=data["version"], inline=True)
                
                if "list" in data["players"]:
                    player_names = ", ".join(data["players"]["list"])
                    embed.add_field(name="Players", value=player_names, inline=False)
                
                if "motd" in data:
                    motd = "\n".join(data["motd"]["clean"])
                    embed.add_field(name="Description", value=motd, inline=False)
                
                if icon_url:
                    embed.set_thumbnail(url=icon_url)
                
                embed.set_footer(text=f"Requested by {context.author}", icon_url=f"{context.author.display_avatar.url}?size=128")
                await context.send(embed=embed)

async def setup(bot) -> None:
    await bot.add_cog(General(bot))
