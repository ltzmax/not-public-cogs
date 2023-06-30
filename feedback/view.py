import discord
import typing

class FeedbackView(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)
        self.up_count: int = 0
        self.down_count: int = 0
        self.members: typing.Dict[typing.Literal["👍", "👎"], typing.Set] = {"👍": set(), "👎": set()}
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
            self.members["👎"].remove(interaction.user)
            self.down_button.label = f"{self.down_count} votes" if self.down_count != 0 else None
        if interaction.user not in self.members["👍"]:
            self.up_count += 1
            self.members["👍"].add(interaction.user)
        else:
            self.up_count -= 1
            self.members["👍"].remove(interaction.user)
        button.label = f"{self.up_count} votes" if self.up_count != 0 else None
        await interaction.response.edit_message(view=self)

    @discord.ui.button(emoji="👎", custom_id="feedback_down_button")
    async def down_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        if interaction.user in self.members["👍"]:
            self.up_count -= 1
            self.members["👍"].remove(interaction.user)
            self.up_button.label = f"{self.up_count} votes" if self.up_count != 0 else None
        if interaction.user not in self.members["👎"]:
            self.down_count += 1
            self.members["👎"].add(interaction.user)
        else:
            self.down_count -= 1
            self.members["👎"].remove(interaction.user)
        button.label = f"{self.down_count} votes" if self.down_count != 0 else None
        await interaction.response.edit_message(view=self)
