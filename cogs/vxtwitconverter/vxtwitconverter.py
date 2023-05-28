import logging
import os

from discord import Message, channel
from urlextract import URLExtract

from redbot.core import commands, data_manager
from redbot.core.bot import Red


class VxTwitConverter(commands.Cog):
    """Converts Twitter link to VxTwitter for better video embeds"""

    def __init__(self, bot: Red):
        super().__init__()
        self.bot = bot

        # Initialize logger, and save to cog folder.
        save_folder = data_manager.cog_data_path(cog_instance=self)
        self.logger = logging.getLogger("red.luicogs.vxtwitconverter")
        if not self.logger.handlers:
            log_path = os.path.join(save_folder, "info.log")
            handler = logging.FileHandler(filename=log_path, encoding="utf-8", mode="a")
            handler.setFormatter(
                logging.Formatter("%(asctime)s %(message)s", datefmt="[%d/%m/%Y %H:%M:%S]")
            )
            self.logger.addHandler(handler)

    @commands.Cog.listener("on_message")
    async def twit_replacer(self, message: Message):
        # skips if the message is sent by any bot
        if message.author.bot:
            return

        # skips if message is in dm
        if isinstance(message.channel, channel.DMChannel):
            return

        # skips if the message has no embeds
        if not any(embed.video for embed in message.embeds):
            return

        # the actual code part
        vx_twit_links = [
            result.replace("https://twitter.com", "https://vxtwitter.com")
            for result in URLExtract().find_urls(message.content)
            if "https://twitter.com" in result
        ]

        # if we can't find any twitter links
        if not vx_twit_links:
            self.logger.debug("Embed found, but cannot find any valid links in the message")
            return

        # constructs the message and replies with a mention
        ok = await message.reply(
            "OwO what's this?\n"
            "*notices your terrible twitter embeds*\n"
            "Here's a better alternative:\n" + "\n".join(vx_twit_links),
        )

        # Remove embeds from user message if reply is successful
        if ok:
            await message.edit(suppress=True)
