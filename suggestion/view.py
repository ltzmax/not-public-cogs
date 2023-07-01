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
        self.up_count: int = 0
        self.down_count: int = 0
        self.members: typing.Dict[typing.Literal["👍", "👎"], typing.Set] = {
            "👍": set(),
            "👎": set(),
        }
        self._message: discord.Message = None

    async def on_timeout(self) -> None:
        self.up_button.disabled = True
        self.down_button.disabled = True
        try:
            await self._message.edit(view=self)
        except discord.HTTPException:
            pass

    @discord.ui.button(
        emoji="👍", custom_id="suggest_up_button", style=discord.ButtonStyle.blurple
    )
    async def up_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        if interaction.user in self.members["👎"]:
            self.down_count -= 1
            self.members["👎"].remove(interaction.user)
            self.down_button.label = (
                f"{self.down_count} votes" if self.down_count != 0 else None
            )
        if interaction.user not in self.members["👍"]:
            self.up_count += 1
            self.members["👍"].add(interaction.user)
        else:
            self.up_count -= 1
            self.members["👍"].remove(interaction.user)
        button.label = f"{self.up_count} votes" if self.up_count != 0 else None
        await interaction.response.edit_message(view=self)
        await interaction.followup.send("You pressed Up Vote.", ephemeral=True)

    @discord.ui.button(
        emoji="👎", custom_id="suggest_down_button", style=discord.ButtonStyle.blurple
    )
    async def down_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        if interaction.user in self.members["👍"]:
            self.up_count -= 1
            self.members["👍"].remove(interaction.user)
            self.up_button.label = (
                f"{self.up_count} votes" if self.up_count != 0 else None
            )
        if interaction.user not in self.members["👎"]:
            self.down_count += 1
            self.members["👎"].add(interaction.user)
        else:
            self.down_count -= 1
            self.members["👎"].remove(interaction.user)
        button.label = f"{self.down_count} votes" if self.down_count != 0 else None
        await interaction.response.edit_message(view=self)
        await interaction.followup.send("You pressed Down Vote.", ephemeral=True)
