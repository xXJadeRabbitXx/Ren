from discord import Message

from cogs.vxtwitconverter.eventsCore import EventCore
from redbot.core import commands


class EventHandlers(EventCore):
    @commands.Cog.listener("on_message")
    async def twit_replacer(self, message: Message):
        await self._twit_replacer(message)
