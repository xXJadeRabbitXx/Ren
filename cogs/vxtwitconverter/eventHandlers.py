from discord import Message

from .eventsCore import EventsCore
from redbot.core import commands


class EventHandlers(EventsCore):
    @commands.Cog.listener("on_message")
    async def twit_replacer(self, message: Message):
        await self._twit_replacer(message)
