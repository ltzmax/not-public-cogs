import logging

from typing import Dict, Optional, Any, TYPE_CHECKING, Union

from emoji import EMOJI_DATA
from redbot.core import commands

log: logging.Logger = logging.getLogger("red.maxcogs.suggestions")


class Emoji:
    def __init__(self, data: Dict[str, Any]) -> None:
        self.name = data["name"]
        self.id = data.get("id", None)
        self.animated = data.get("animated", None)
        self.custom = self.id is not None
        
    @classmethod
    def from_data(cls, data: Union[str, Dict[str, Any]]):
        log.debug(data)
        if not data:
            return None
        if isinstance(data, str):
            return cls({"name": data})
        return cls(data)
    
    def to_dict(self) -> Dict[str, Any]:
        return {"name": self.name, "id": self.id}
    
    def as_emoji(self) -> str:
        if not self.custom:
            return self.name
        animated = "a" if self.animated else ""
        return f"<{animated}:{self.name}:{self.id}>"


if TYPE_CHECKING:
    EmojiConverter = Optional[Emoji]
else:
    class EmojiConverter(commands.PartialEmojiConverter):
        async def convert(self, ctx: commands.Context, arg: str) -> Optional[Emoji]:
            if arg.lower() == "none":
                return None
            arg = arg.strip()
            data = arg if arg in EMOJI_DATA.keys() else await super().convert(ctx, arg)
            data = getattr(data, "to_dict", lambda: data)()
            return Emoji.from_data(data)
