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
from redbot.core import commands, Config
from redbot.core.bot import Red
import discord
import typing

from redbot.core.utils.chat_formatting import box, humanize_list

from .view import FeedbackView

class Feedback(commands.Cog):
    """Give feedback about something!"""

    __authors__: typing.List[str] = ["MAX", "AAA3A"]
    __version__: str = "1.0.0"
    __docs__: str = "https://github.com/ltzmax/maxcogs/blob/master/feedback/README.md"

    def __init__(self, bot: Red):
        self.bot: Red = bot

        self.config: Config = Config.get_conf(self, identifier=78631113035100160)
        default_guild: typing.Dict[str, typing.Union[int, str, bool]] = {"channel": None, "feedbacktitle": "New Feedback", "react": False}
        self.config.register_guild(**default_guild)

        self.views: typing.List[discord.ui.View] = []

    async def cog_unload(self) -> None:
        for view in self.views:
            await view.on_timeout()
            view.stop()

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """Thanks Sinbad!"""
        pre = super().format_help_for_context(ctx)
        return f"{pre}\n\nAuthors: {humanize_list(self.__authors__)}\nCog Version: {self.__version__}\nDocs: {self.__docs__}"

    @commands.guild_only()
    @commands.cooldown(1, 60, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    @commands.command()
    async def feedback(self, ctx: commands.Context, *, feedback: str) -> None:
        """Give feedback about something."""
        config = await self.config.guild(ctx.guild).all()
        channel = config["channel"]
        if channel is None:
            return await ctx.send("Channel is not set.")
        channel = self.bot.get_channel(channel)
        # Check if the bot can send messages and embeds in the channel
        # Just in case they disable one of the permissions after setting the channel
        if (
            not channel.permissions_for(ctx.me).send_messages
            and not channel.permissions_for(ctx.me).embed_links
        ):
            return await ctx.send(
                "I don't have permissions to `send_message` or `embed_links` in that channel."
            )
        title = config["feedbacktitle"]
        if len(feedback) > 1024:
            return await ctx.send(f"{title} must be 1024 characters or less.")
        embed = discord.Embed(
            title=title, description=feedback, color=await ctx.embed_color()
        )
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
        embed.set_footer(text=f"User ID: {ctx.author.id}")
        if config["react"]:
            view = FeedbackView()
            view._message = await channel.send(embed=embed, view=view)
            self.views.append(view)
        else:
            await channel.send(embed=embed)
        await ctx.tick()

    @commands.guild_only()
    @commands.admin_or_permissions(manage_guild=True)
    @commands.group(aliases=["feedbackset"])
    async def setfeedback(self, ctx: commands.Context) -> None:
        """Manage settings."""

    @setfeedback.command()
    async def channel(self, ctx: commands.Context, channel: discord.TextChannel = None) -> None:
        """Set or clear the channel."""
        if (
            not channel.permissions_for(ctx.me).send_messages
            and not channel.permissions_for(ctx.me).embed_links
        ):
            return await ctx.send(
                "I don't have permissions to `send_message` or `embed_links` in that channel."
            )
        if channel.id == await self.config.guild(ctx.guild).channel():
            return await ctx.send("That channel is already set.")
        if channel:
            await self.config.guild(ctx.guild).channel.set(channel.id)
            await ctx.send(f"Channel has been set to {channel.mention}.")
        else:
            await self.config.guild(ctx.guild).channel.clear()
            await ctx.send("Channel has been cleared.")

    @setfeedback.command()
    async def title(self, ctx: commands.Context, *, title: str = None) -> None:
        """Set or reset the title."""
        if title is not None and len(title) > 256:
            return await ctx.send("Feedback title must be 256 characters or less.")
        if title:
            await self.config.guild(ctx.guild).feedbacktitle.set(title)
            await ctx.send(f"Title has been set to {title}.")
        else:
            await self.config.guild(ctx.guild).feedbacktitle.clear()
            await ctx.send("Title has been cleared.")

    @setfeedback.command()
    async def react(self, ctx: commands.Context, toggle: bool = None) -> None:
        """Toggle whether to up/down vote."""
        if toggle is None:
            toggle = not await self.config.guild(ctx.guild).react()
        await self.config.guild(ctx.guild).react.set(toggle)
        if toggle:
            await ctx.send("I will now add upvote and downvote reactions.")
        else:
            await ctx.send("I will no longer add upvote and downvote reactions.")

    @setfeedback.command()
    async def view(self, ctx: commands.Context) -> None:
        """View the current settings."""
        data = await self.config.guild(ctx.guild).all()
        channel = self.bot.get_channel(data["channel"])
        title = data["feedbacktitle"]
        channel = "Not Set" if channel is None else channel.mention
        embed = discord.Embed(
            title="Settings",
            description=f"`{'Channel':<8}`: {channel}\n`{'Title':<8}`: {title}",
            color=await ctx.embed_color(),
        )
        await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @setfeedback.command()
    async def version(self, ctx: commands.Context) -> None:
        """Shows the version of the cog."""
        version = self.__version__
        authors = self.__authors__
        embed = discord.Embed(
            title="Cog Information",
            description=box(
                f"{'Cog Authors':<11}: {humanize_list(authors)}\n{'Cog Version':<10}: {version}",
                lang="yaml",
            ),
            color=await ctx.embed_color(),
        )
        await ctx.send(embed=embed)
