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
import discord
import typing


class SuggestView(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @discord.ui.button(
        emoji="👍", custom_id="suggest_up_button", style=discord.ButtonStyle.blurple
    )
    async def up_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        members_votes = await interaction.client.get_cog("Suggestion").config.guild(interaction.guild).members_votes.get_raw(f"{interaction.channel.id}-{interaction.message.id}", default={"👍": [], "👎": []})
        up_count = len(members_votes["👍"])
        down_count = len(members_votes["👎"])
        if interaction.user.id in members_votes["👎"]:
            down_count -= 1
            members_votes["👎"].remove(interaction.user.id)
            self.down_button.label = (
                f"{down_count} votes" if down_count != 0 else None
            )
        if interaction.user.id not in members_votes["👍"]:
            up_count += 1
            members_votes["👍"].append(interaction.user.id)
        else:
            up_count -= 1
            members_votes["👍"].remove(interaction.user.id)
        await interaction.client.get_cog("Suggestion").config.guild(interaction.guild).members_votes.set_raw(f"{interaction.channel.id}-{interaction.message.id}", value=members_votes)
        button.label = f"{up_count} votes" if up_count != 0 else None
        await interaction.response.edit_message(view=self)

    @discord.ui.button(
        emoji="👎", custom_id="suggest_down_button", style=discord.ButtonStyle.blurple
    )
    async def down_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        members_votes = await interaction.client.get_cog("Suggestion").config.guild(interaction.guild).members_votes.get_raw(f"{interaction.channel.id}-{interaction.message.id}", default={"👍": [], "👎": []})
        up_count = len(members_votes["👍"])
        down_count = len(members_votes["👎"])
        if interaction.user.id in members_votes["👍"]:
            up_count -= 1
            members_votes["👍"].remove(interaction.user.id)
            self.up_button.label = (
                f"{up_count} votes" if up_count != 0 else None
            )
        if interaction.user.id not in members_votes["👎"]:
            down_count += 1
            members_votes["👎"].append(interaction.user.id)
        else:
            down_count -= 1
            members_votes["👎"].remove(interaction.user.id)
        await interaction.client.get_cog("Suggestion").config.guild(interaction.guild).members_votes.set_raw(f"{interaction.channel.id}-{interaction.message.id}", value=members_votes)
        button.label = f"{down_count} votes" if down_count != 0 else None
        await interaction.response.edit_message(view=self)
