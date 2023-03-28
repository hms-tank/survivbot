import discord
from discord.ext import commands
import aiofiles
import asyncio

class xp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.leaderboard = dict()
        self.leaderboard_load_event = asyncio.Event()
        self.syncboards_lock = asyncio.Lock()
    
    async def cog_check(self, ctx):
        if not self.leaderboard_load_event.is_set():
            await ctx.reply('Please wait for the leaderboard to load.')
        await self.leaderboard_load_event.wait()
        return True
    
    async def cog_load(self):
        print('Loading XP data')
        async with aiofiles.open('board.txt') as f:
            content = await file.read()
            leaderboard = [int(i.strip()) for i in content.splitlines()]
        async with aiofiles.open('xp.txt') as f:
            content = await file.read()
            xp = [int(i.strip()) for i in content.splitlines()]
        async with aiofiles.open('time.txt') as f:
            content = await file.read()
            timestamps = [int(i.strip()) for i in content.splitlines()]
        assert len(leaderboard) == len(xp) == len(timestamps)
        for i in range(len(leaderboard)):
            self.leaderboard[leaderboard[i]] = {xp: xp[i], time: timestamps[i]}
        self.leaderboard_load_event.set()
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        self.leaderboard[member.id] = {'xp': 0, 'time': round(time.time())}
        await self.syncboards()

    @commands.command()
    @commands.is_owner()
    async def awardxp(self, ctx, user, amount: int):
        self.leaderboard[user.id]['xp'] += amount
        await self.syncboards()
        await ctx.send(f"<@!{user.id}> has been awarded {amount} XP!")
    
    async def syncboards(self):
        await self.leaderboard_load_event.wait()
        # The lock is to try to prevent concurrent file writing,
        # although it probably shouldn't matter. All the syncboards
        # requests will stack up and once one is done, the next one will
        # start writing. Using a database will drastically reduce
        # complexity. I suggest using the motor library for MongoDB.
        await self.syncboards_lock.acquire()
        async with aiofiles.open("board.txt", 'w') as f:
            await f.write(
                '\n'.join(
                    [str(x) for x in self.leaderboard.keys()]
                )
            )
            await f.write('\n')
        async with aiofiles.open("xp.txt", 'w') as f:
            await f.write(
                '\n'.join(
                    [str(x['xp']) for x in self.leaderboard.values()]
                )
            )
            await f.write('\n')
        async with aiofiles.open("time.txt", 'w') as f:
            await f.write(
                '\n'.join(
                    [str(x['time']) for x in self.leaderboard.values()]
                )
            )
            await f.write('\n')
        self.syncboards_lock.release()

async def setup(bot):
    await bot.add_cog(xp(bot))