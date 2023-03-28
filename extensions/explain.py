import discord
from discord.ext import commands

class Explain(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @client.command()
    async def explain(self, ctx):
        embed = discord.Embed(
            title="Explanation of This:tm:",
            color=0xFF0000
        )
        # I was very annoyed that the explanations went beyond the line
        # length limit, so I am using implicit C-style joining to make
        # them fit. I am trying to preserve each logical section of the
        # sentences on each line to make them as readable as possible.
        embed.add_field(
            name="What is this server?",
            value=(
                "This Discord Server is the community area for "
                "Surviv Reloaded, open-source server for the "
                "defunct online game surviv.io."
            )
        )
        embed.add_field(
            name="What is this bot?",
            value=(
                "This bot was made by Killaship to save the hassle "
                "of explaining what this is to everyone."
            )
        )
        embed.add_field(
            name="What is Surviv Reloaded?",
            value=(
                "It's an open-source server hosting the original client. "
                "In other words, it's the original surviv.io, "
                "just hosted by a different server. "
                "It's not a clone of Surviv.io."
            )
        )
        embed.add_field(
            name="Where can I get more info?",
            value="https://github.com/SurvivReloaded"
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Explain(bot))