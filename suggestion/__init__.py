from redbot.core.bot import Red

from .suggestion import Suggestion

__red_end_user_data_statement__: str = (
    "This cog does not persistently store data about users."
)


async def setup(bot: Red) -> None:
    await bot.add_cog(Suggestion(bot))
