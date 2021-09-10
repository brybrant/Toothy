import asyncio

import discord
from discord.ext import commands


class ToothyContext(commands.Context):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def get_answer(self,
                         prompt=None,
                         *,
                         timeout=120,
                         timeout_message="No response in time",
                         check=None,
                         delete_answer=False,
                         return_full=False):

        if prompt:
            await self.send(prompt)
        if not check:

            def check(message):
                return (message.author == self.author
                        and message.channel == self.channel)

        try:
            answer = await self.bot.wait_for("message",
                                             timeout=timeout,
                                             check=check)
        except asyncio.TimeoutError:
            if timeout_message:
                await self.send(timeout_message)
            return None
        if delete_answer:
            try:
                await answer.delete()
            except discord.HTTPException:
                pass
        if return_full:
            return answer
        return answer.content

    async def get_reaction(self, message, emojis, *, timeout=120, check=None):
        def reaction_check(reaction, user):
            if user.bot:
                return False
            emoji = reaction.emoji
            if emoji not in emojis:
                return False
            return reaction.message.id == message.id and user == self.author

        try:
            reaction, _ = await self.bot.wait_for("reaction_add",
                                                  check=reaction_check,
                                                  timeout=timeout)
        except asyncio.TimeoutError:
            return None
        return reaction
