from twitchio.ext import commands
from utils import Utils
import config

bot = commands.Bot(
    token=config.PASS,
    client_id=config.SECRET,
    nick=config.NICK,
    prefix='!',
    initial_channels=config.CHAN
)


@bot.command(name='дуэль')
async def duel(ctx):
    txt = utils.duel(ctx)
    await ctx.send(txt)


@bot.command(name='кусь')
async def bite(ctx):
    txt = utils.bite(ctx)
    await ctx.send(txt)


if __name__ == "__main__":
    utils = Utils(config.CHAN[0])
    bot.run()
