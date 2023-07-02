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
from typing import Union

try:
    from emoji import UNICODE_EMOJI_ENGLISH as EMOJI_DATA  # emoji<2.0.0
except ImportError:
    from emoji import EMOJI_DATA  # emoji>=2.0.0

from redbot.core.utils.chat_formatting import box, humanize_list
from .view import SuggestView

# Taken from Kuro's osu's cog
# https://github.com/Kuro-Rui/Kuro-Cogs/blob/6258b80d130a1ab41373dbcc975e25441d175d53/osu/converters.py#L37-L42
class Emoji(commands.EmojiConverter):
    async def convert(self, ctx: commands.Context, argument: str) -> Union[str, int]:
        if argument in EMOJI_DATA:
            return argument
        emoji = await super().convert(ctx, argument)
        return emoji.id

class Suggestion(commands.Cog):
    """Customizable suggestion cog to various purposes."""

    __authors__: typing.List[str] = ["MAX", "AAA3A"]
    __version__: str = "1.0.0"
    __docs__: str = "https://github.com/ltzmax/maxcogs/blob/master/suggestion/README.md"

    def __init__(self, bot: Red):
        self.bot: Red = bot

        self.config: Config = Config.get_conf(self, identifier=78631113035100160)
        default_guild: typing.Dict[str, typing.Union[int, str, bool, typing.Dict[str, typing.List[int]]]] = {
            "channel": None,
            "default_title": "Suggestion",
            "react": False,
            "members_votes": {},
            "up_emoji": "👍",
            "down_emoji": "👎"
        }
        self.config.register_guild(**default_guild)

    async def cog_load(self) -> None:
        self.bot.add_view(SuggestView(self.bot, None, None))

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """Thanks Sinbad!"""
        pre = super().format_help_for_context(ctx)
        return f"{pre}\n\nAuthors: {humanize_list(self.__authors__)}\nCog Version: {self.__version__}\nDocs: {self.__docs__}"

    def cooldown(ctx):
        return commands.Cooldown(1, 15)

    @commands.guild_only()
    @commands.bot_has_permissions(embed_links=True)
    @commands.dynamic_cooldown(cooldown, type=commands.BucketType.user)
    @commands.command(aliases=["sendmessage", "sendmsg"])
    async def send(self, ctx: commands.Context, *, message: str) -> None:
        """Send your message to the set channel.

        **Example:**
        - `[p]send This is my suggestion!` - This will send your message to the set channel.
        """
        config = await self.config.guild(ctx.guild).all()
        channel = config["channel"]
        if channel is None:
            # await self.send.reset_cooldown(ctx)
            return await ctx.send("Channel is not set.")
        channel = self.bot.get_channel(channel)
        # Check if the bot can send messages and embeds in the channel
        # Just in case they disable one of the permissions after setting the channel
        if (
            not channel.permissions_for(ctx.me).send_messages
            and not channel.permissions_for(ctx.me).embed_links
        ):
            # await self.send.reset_cooldown(ctx)
            return await ctx.send(
                "I don't have permissions to `send_message` or `embed_links` in that channel."
            )
        title = config["default_title"]
        if len(message) > 2000:
            # await self.send.reset_cooldown(ctx)
            return await ctx.send(f"{title} must be 2000 characters or less.")
        embed = discord.Embed(
            title=title, description=message, color=await ctx.embed_color()
        )
        embed.set_author(
            name=ctx.author.display_name, icon_url=ctx.author.display_avatar
        )
        embed.set_footer(text=f"User ID: {ctx.author.id}")
        if config["react"]:
            await channel.send(embed=embed, view=SuggestView(self.bot, config["up_emoji"], config["down_emoji"]))
        else:
            await channel.send(embed=embed)
        await ctx.tick()

    @commands.guild_only()
    @commands.admin_or_permissions(manage_guild=True)
    @commands.group(aliases=["suggestset", "setsuggest"])
    async def suggestionset(self, ctx: commands.Context) -> None:
        """Manage suggestion settings."""

    @suggestionset.command()
    async def channel(
        self, ctx: commands.Context, channel: discord.TextChannel = None
    ) -> None:
        """Set or clear the channel.

        If no channel is provided, it will clear the channel.

        **Example:**
        - `[p]suggestionset channel #suggestions` - This will set the channel to #suggestions.
        - `[p]suggestionset channel` - This will clear the channel.
        """
        if (
            channel is not None
            and not channel.permissions_for(ctx.me).send_messages
            and not channel.permissions_for(ctx.me).embed_links
        ):
            return await ctx.send(
                "I don't have permissions to `send_messages` or `embed_links` in that channel."
            )
        if channel:
            await self.config.guild(ctx.guild).channel.set(channel.id)
            await ctx.send(f"Channel has been set to {channel.mention}.")
        else:
            await self.config.guild(ctx.guild).channel.clear()
            await ctx.send("Channel has been cleared.")

    @suggestionset.command()
    async def title(self, ctx: commands.Context, *, title: str = None) -> None:
        """Set or reset the title.

        This is the title of the embed where it's currently set to "Suggestion".
        If no title is provided, it will reset the title.
        The title must be 256 characters or less.

        **Example:**
        - `[p]suggestionset title My Suggestion` - This will set the title to "My Suggestion".
        - `[p]suggestionset title` - This will reset the title to "Suggestion".
        """
        if title is not None and len(title) > 256:
            return await ctx.send("Title must be 256 characters or less.")
        if title:
            await self.config.guild(ctx.guild).default_title.set(title)
            await ctx.send(f"Title has been set to {title}.")
        else:
            await self.config.guild(ctx.guild).default_title.clear()
            await ctx.send("Title has been cleared.")

    @suggestionset.command(aliases=["react"])
    async def buttons(self, ctx: commands.Context, toggle: bool = None) -> None:
        """Toggle whether to up/down vote.

        It is disabled by default.
        If no toggle is provided, it will toggle the current setting.
        """
        if toggle is None:
            toggle = not await self.config.guild(ctx.guild).react()
        await self.config.guild(ctx.guild).react.set(toggle)
        if toggle:
            await ctx.send("I will now add upvote and downvote reactions.")
        else:
            await ctx.send("I will no longer add upvote and downvote reactions.")

    @suggestionset.group()
    async def emoji(self, ctx: commands.Context) -> None:
        """Manage the emojis for the buttons."""

    @emoji.command(name="up")
    async def emoji_up(self, ctx: commands.Context, *, emoji: Emoji = None) -> None:
        """Set or reset the upvote emoji.

        If no emoji is provided, it will reset the emoji.

        **Example:**
        - `[p]suggestionset emoji up :thumbsup:` - This will set the upvote emoji to :thumbsup:.
        - `[p]suggestionset emoji up` - This will reset the upvote emoji.
        """
        if emoji:
            await self.config.guild(ctx.guild).up_emoji.set(emoji)
            await ctx.send(f"Upvote emoji has been set to {emoji}.")
        else:
            await self.config.guild(ctx.guild).up_emoji.clear()
            await ctx.send("Upvote emoji has been cleared.")

    @emoji.command(name="down")
    async def emoji_down(self, ctx: commands.Context, *, emoji: Emoji = None) -> None:
        """Set or reset the downvote emoji.

        If no emoji is provided, it will reset the emoji.

        **Example:**
        - `[p]suggestionset emoji down :thumbsdown:` - This will set the downvote emoji to :thumbsdown:.
        - `[p]suggestionset emoji down` - This will reset the downvote emoji.
        """
        if emoji:
            await self.config.guild(ctx.guild).down_emoji.set(emoji)
            await ctx.send(f"Downvote emoji has been set to {emoji}.")
        else:
            await self.config.guild(ctx.guild).down_emoji.clear()
            await ctx.send("Downvote emoji has been cleared.")

    @suggestionset.command()
    async def view(self, ctx: commands.Context) -> None:
        """View the current settings."""
        data = await self.config.guild(ctx.guild).all()
        channel = self.bot.get_channel(data["channel"])
        title = data["default_title"]
        react = data["react"]
        channel = "Not Set" if channel is None else channel.mention
        embed = discord.Embed(
            title="Current Settings",
            description=f"`{'Channel':<8}`: {channel}\n`{'Buttons':<8}`: {react}\n`{'Title':<8}`: {title}",
            color=await ctx.embed_color(),
        )
        await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @suggestionset.command()
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

    @suggestionset.command()
    async def help(self, ctx: commands.Context) -> None:
        """Explain how to use the cog."""
        title = await self.config.guild(ctx.guild).default_title()
        msg = (
            f"This cog allows users to send {title} to a set channel.\n"
            f"The bot will add upvote and downvote button reactions to {title} if a person with manage_guild have enabled it. "
            "You will also be able to customize for your own needs. i.e you want to use this to provide feedback for a game, server or for anything."
        )
        embed = discord.Embed(
            title="Suggestion Help",
            description=msg,
            color=await ctx.embed_color(),
        )
        embed.add_field(
            name="[p]send <message>",
            value="This will send a suggestion to the set channel.",
            inline=False,
        )
        embed.add_field(
            name="[p]suggestionset channel <#channel>",
            value="This will set the channel to send suggestions to.",
            inline=False,
        )
        embed.add_field(
            name="[p]suggestionset title <title>",
            value="This will set the title of the embed. Default is `Suggestion`.",
            inline=False,
        )
        embed.add_field(
            name="[p]suggestionset buttons",
            value="This will toggle whether to add upvote and downvote reactions.",
            inline=False,
        )
        embed.add_field(
            name="[p]suggestionset view",
            value="This will show the current settings.",
        )
        embed.set_footer(text="Change of button emojis is not possible.")
        await ctx.send(embed=embed)
