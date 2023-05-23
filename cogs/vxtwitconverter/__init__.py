from .vxtwitconverter import VxTwitConverter
from redbot.core.bot import Red


async def setup(bot: Red):
    """Add the cog to the bot."""
    await bot.add_cog(VxTwitConverter(bot))
