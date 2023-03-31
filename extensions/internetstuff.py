import discord
from discord.ext import commands
import httpx
from http.client import responses

TIMEOUT = 10

# NON-STANDARD CODES
responses[419] = "CSRF Token Missing or Expired"
responses[420] = "Enhance Your Calm"
responses[440] = "Login Time-out"
responses[444] = "No Response"
responses[449] = "Retry With"
responses[450] = "Blocked by Windows Parental Controls"
responses[460] = "Client closed the connection with AWS Elastic Load Balancer"
responses[463] = "The load balancer received an X-Forwarded-For request header with more than 30 IP addresses"
responses[494] = "Request header too large"
responses[495] = "SSL Certificate Error"
responses[496] = "SSL Certificate Required"
responses[497] = "HTTP Request Sent to HTTPS Port"
responses[498] = "Invalid Token (Esri)"
responses[499] = "Client Closed Request"

responses[520] = "Web Server Returned an Unknown Error"
responses[521] = "Web Server Is Down"
responses[522] = "Connection Timed out"
responses[523] = "Origin Is Unreachable"
responses[524] = "A Timeout Occurred"
responses[525] = "SSL Handshake Failed"
responses[526] = "Invalid SSL Certificate"
responses[527] = "Railgun Error"
responses[530] = "Origin DNS Error"
responses[561] = "Unauthorized (AWS Elastic Load Balancer)"

responses[609] = "Nice."
responses[999] = (
    f"The connection timed out after {TIMEOUT} seconds. "
    "This means the server most likely is down, "
    "or it spun out into an infinite loop. "
    f"(The bot killed url_status() after {TIMEOUT} seconds!)"
)

class InternetStuff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sites = [
            r'https://taskjourney.org:449',
            r'https://survivreloaded.com',
            r'https://resurviv.io'
        ]

    # I will refactor this later using httpx instead because I can't
    # find a nice way to make requests async (I don't understand
    # grequests)
    @commands.command()
    async def serverstatus(self, ctx):
        text = (
            f'Checking {len(self.sites)} site(s)\n'
            'Note: This may or may not be accurate. '
            # Then what's the point of the command??
            'Do not trust these results.\n'
        )
        for site in self.sites:
            response_code, response_name = await self.url_status(site)
            text += f'*{site}*\n'
            if response_code != 200:
                text += (
                    "The server sent an abnormal response. "
                    "If it's 301 or 302, the server redirected the bot. "
                    "If it's not those, the server might be down. "
                    "The HTTP code sent was: "
                    f"{response_code}. ({response_name})\n"
                )
            else:
                text += (
                    "The server is currently up. "
                    "(It sent a response code of 200 OK)\n"
                    "If your game is frozen, "
                    "it's most likely that the client froze or crashed. "
                    "The game is still relatively unstable, "
                    "you'll have to reload the game.\n"
                )
        embed = discord.Embed(
            title="Surviv Reloaded Status",
            description=text.strip(),
            color=0x00FF00
        )
        await ctx.send(embed=embed)
    
    # This command could expose the server's IP to an attacker. Why does
    # this even exist? Who would need to use a discord bot to check some
    # random website's status?
    @commands.command()
    async def checkurl(self, ctx, site):
        response_code, response_name = await self.url_status(site)
        if(response_code != 200):
            await ctx.send(
                "The server is currently down or unresponsive. "
                f"The HTTP code sent was: {response_code}. ({response_name})"
            )
        else:
            await ctx.send(
                "The server is currently up. "
                "(It sent a response code of 200 OK)"
            )

    async def url_status(self, site):
        with httpx.AsyncClient() as client:
            try:
                r = await client.head(site, timeout=TIMEOUT)
            except httpx.TimeoutException:
                return (999, responses[999])
        return (
            r.status_code if r.status_code else None,
            responses.get(
                r.status_code if r.status_code else None,
                'Web Server Returned an Unknown Error'
            )
        )

async def setup(bot):
    await bot.add_cog(InternetStuff(bot))