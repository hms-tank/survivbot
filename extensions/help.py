import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @client.command()
    async def help(self, ctx):
        embed = discord.Embed(title="help", color=0xFF0000)
        embed.add_field(
            name="$explain",
            value="Explains this server and lists FAQ."
        )
        embed.add_field(
            name="$links",
            value="Lists various links related to the project."
        )
        embed.add_field(
            name="$serverstatus",
            value=(
                "Checks whether the game server (or at least website) is up. "
                "It checks all websites on which the game is hosted. "
                "Not too reliable, might return 502 errors."
            )
        )
        embed.add_field(
            name="$getxp",
            value="This command shows the amount of XP the sender has."
        )
        embed.add_field(
            name="$getleaderboard",
            value=(
                "This command lists the 5 members of the server "
                "with the most XP!. (6 including bot)"
            )
        )
        embed.add_field(
            name="$checkurl",
            value="Checks the connectivity of any URL."
        )
        embed.add_field(
            name="$help",
            value="This command."
        )
        embed.add_field(
            name="Bot GitHub",
            value="https://github.com/Killaship/survivbot"
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))