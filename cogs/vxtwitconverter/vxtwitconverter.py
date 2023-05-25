import logging
import os

from discord import Message, channel
from urlextract import URLExtract

from redbot.core import commands, data_manager
from redbot.core.bot import Red


class VxTwitConverter(commands.Cog):
    """Converts twitter link embeds to vxtwitter"""

    def __init__(self, bot: Red):
        super().__init__()
        self.bot = bot

        # Initialize logger, and save to cog folder.
        saveFolder = data_manager.cog_data_path(cog_instance=self)
        self.logger = logging.getLogger("red.luicogs.vxtwitconverter")
        if not self.logger.handlers:
            logPath = os.path.join(saveFolder, "info.log")
            handler = logging.FileHandler(filename=logPath, encoding="utf-8", mode="a")
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
        extractor = URLExtract()

        if extractor.has_urls(message.content):
            results = extractor.find_urls(message.content)
            new_message = [
                result.replace("https://twitter.com", "https://vxtwitter.com")
                for result in results
                if "https://twitter.com" in result
            ]

            if new_message:
                # removed embed from the parent message, and replies with vxtwitter link
                await message.reply(
                    "OwO what's this?\n"
                    "*notices your terrible twitter embeds*\n"
                    "Here's a better alternative:\n" + ",\n".join(new_message)
                )

                await message.edit(suppress=True)
        else:
            self.logger.error("Message contains embed, but cannot find link")
