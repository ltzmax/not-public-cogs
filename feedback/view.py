from redbot.core import commands
from redbot.core.bot import Red
import discord
import typing

class FeedbackView(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)
        self.up_count: int = 0
        self.down_count: int = 0
        self.members: typing.Dict[typing.Literal["👍", "👎"]] = {"👍": [], "👎": []}
        self._message: discord.Message = None

    async def on_timeout(self) -> None:
        self.up_button.disabled = True
        self.down_button.disabled = True
        try:
            await self._message.edit(view=self)
        except discord.HTTPException:
            pass

    @discord.ui.button(emoji="👍", custom_id="feedback_up_button")
    async def up_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        if interaction.user in self.members["👎"]:
            self.down_count -= 1
            self.down_button.label = f"({self.down_count})"
        if interaction.user not in self.members["👍"]:
            self.up_count += 1
            self.members["👍"].append(interaction.user)
        else:
            self.up_count -= 1
            self.members["👍"].remove(interaction.user)
        button.label = f"({self.up_count})"
        await interaction.response.edit_message(view=self)

    @discord.ui.button(emoji="👎", custom_id="feedback_down_button")
    async def down_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        if interaction.user in self.members["👍"]:
            self.up_count-= 1
            self.up_button.label = f"({self.up_count})"
        if interaction.user not in self.members["👎"]:
            self.down_count += 1
            self.members["👎"].append(interaction.user)
        else:
            self.down_count -= 1
            self.members["👎"].remove(interaction.user)
        button.label = f"({self.down_count})"
        await interaction.response.edit_message(view=self)
