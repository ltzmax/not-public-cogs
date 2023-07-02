"""
MIT License

Copyright (c) 2022-present ltzmax

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import typing
import functools

import discord
from redbot.core.bot import Red

if typing.TYPE_CHECKING:
    from .suggestion import Suggestion


class UpVoteButton(discord.ui.Button):
    def __init__(
        self, emoji: str | None, callback, custom_id="UPVOTE:BUTTON"
    ):
        super().__init__(
            emoji=emoji,
            style=discord.ButtonStyle.green,
            custom_id=custom_id,
        )
        self.callback = functools.partial(callback, self)


class DownVoteButton(discord.ui.Button):
    def __init__(
        self, emoji: str | None, callback, custom_id="DOWNVOTE:BUTTON"
    ):
        super().__init__(
            emoji=emoji,
            style=discord.ButtonStyle.green,
            custom_id=custom_id,
        )
        self.callback = functools.partial(callback, self)


class SuggestView(discord.ui.View):
    def __init__(self, bot: Red, up_emoji: None, down_emoji: None) -> None:
        super().__init__(timeout=None)
        self.bot: Red = bot
        self.add_item(UpVoteButton(up_emoji, self._up_button))
        self.add_item(DownVoteButton(down_emoji, self._down_button))

    @staticmethod
    async def _up_button(
        self: UpVoteButton, interaction: discord.Interaction
    ) -> None:
        cog = self.view.cog
        members_votes = await cog.config.guild(interaction.guild).members_votes.get_raw(f"{interaction.channel.id}-{interaction.message.id}", default={"👍": [], "👎": []})
        up_count = len(members_votes["👍"])
        down_count = len(members_votes["👎"])
        if interaction.user.id in members_votes["👎"]:
            down_count -= 1
            members_votes["👎"].remove(interaction.user.id)
            self.view._down_button.label = (
                f"{down_count} votes" if down_count != 0 else None
            )
        if interaction.user.id not in members_votes["👍"]:
            up_count += 1
            members_votes["👍"].append(interaction.user.id)
        else:
            up_count -= 1
            members_votes["👍"].remove(interaction.user.id)
        await cog.config.guild(interaction.guild).members_votes.set_raw(f"{interaction.channel.id}-{interaction.message.id}", value=members_votes)
        self.label = f"{up_count} votes" if up_count != 0 else None
        await interaction.response.edit_message(view=self.view)

    @staticmethod
    async def _down_button(
        self: DownVoteButton, interaction: discord.Interaction
    ) -> None:
        cog: "Suggestion" = self.view.cog
        members_votes = await cog.config.guild(interaction.guild).members_votes.get_raw(f"{interaction.channel.id}-{interaction.message.id}", default={"👍": [], "👎": []})
        up_count = len(members_votes["👍"])
        down_count = len(members_votes["👎"])
        if interaction.user.id in members_votes["👍"]:
            up_count -= 1
            members_votes["👍"].remove(interaction.user.id)
            self.view._up_button.label = (
                f"{up_count} votes" if up_count != 0 else None
            )
        if interaction.user.id not in members_votes["👎"]:
            down_count += 1
            members_votes["👎"].append(interaction.user.id)
        else:
            down_count -= 1
            members_votes["👎"].remove(interaction.user.id)
        await cog.config.guild(interaction.guild).members_votes.set_raw(f"{interaction.channel.id}-{interaction.message.id}", value=members_votes)
        self.label = f"{down_count} votes" if down_count != 0 else None
        await interaction.response.edit_message(view=self.view)
        
    @property
    def cog(self):
        return self.bot.get_cog("Suggestion")
