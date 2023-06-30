from redbot.core.bot import Red

from .feedback import Feedback

__red_end_user_data_statement__: str = (
    "This cog does not persistently store data about users."
)


async def setup(bot: Red) -> None:
    await bot.add_cog(Feedback(bot))
