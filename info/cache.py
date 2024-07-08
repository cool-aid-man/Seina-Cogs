import asyncio
from typing import (
    TYPE_CHECKING,
    Dict,
    Final,
    List,
    Literal,
    Optional,
    Protocol,
    Tuple,
    Union,
    cast,
)

import discord
from redbot.core import Config
from redbot.core.bot import Red

if TYPE_CHECKING:
    from .core import Info

DEFAULT: Final[str] = "❔"

SelectEmoji = Literal["roles", "home", "avatar", "banner", "gavatar"]
StatusEmoji = Literal["online", "away", "dnd", "offline", "streaming"]
DeviceEmoji = Literal[
    "mobile_online",
    "mobile_idle",
    "mobile_dnd",
    "mobile_offline",
    "web_online",
    "web_idle",
    "web_dnd",
    "web_offline",
    "desktop_online",
    "desktop_idle",
    "desktop_dnd",
    "desktop_offline",
]
BadgeEmoji = Literal[
    "staff",
    "early_supporter",
    "verified_bot_developer",
    "active_developer",
    "bug_hunter",
    "bug_hunter_level_2",
    "partner",
    "verified_bot",
    "hypesquad",
    "hypesquad_balance",
    "hypesquad_bravery",
    "hypesquad_brilliance",
    "nitro",
    "discord_certified_moderator",
    "bot_http_interactions",
]


class CacheProtocol(Protocol):
    def __init__(self, cog: "Info") -> None: ...

    def close(self) -> None: ...

    def get_status_emoji(self, name: StatusEmoji) -> str: ...

    def get_device_status_emoji(self, name: DeviceEmoji) -> str: ...

    def get_badge_emoji(self, name: BadgeEmoji) -> str: ...

    def get_select_emoji(self, name: SelectEmoji) -> str: ...

    async def set_status_emoji(self, name: StatusEmoji, emoji: int) -> None: ...

    async def set_device_emoji(self, name: DeviceEmoji, emoji: int) -> None: ...

    async def set_badge_emoji(self, name: BadgeEmoji, emoji: int) -> None: ...

    async def set_select_emoji(self, name: SelectEmoji, emoji: int) -> None: ...

    def get_member_device_status(self, member: discord.Member) -> Tuple[str, str, str]: ...

    def get_special_badges(self, user: discord.Member) -> List[str]: ...

    async def set_special_badge(self, guild: int, role: int, emoji: int) -> None: ...

    async def initialize(self) -> None: ...

    async def get_user_badges(self, user: discord.Member) -> Tuple[str, int]: ...


class Cache(CacheProtocol):
    def __init__(self, cog: "Info") -> None:
        self.bot: Red = cog.bot
        self.config: Config = cog.config
        self.emojis: Dict[
            str,
            Dict[str, Union[Optional[int], Dict[str, Optional[int]], Dict[str, Dict[str, int]]]],
        ] = {"status": {}, "badge": {}, "special": {}, "settings": {}}
        self.task: asyncio.Task[None] = asyncio.create_task(self.initialize(), name="info:cache")

    def close(self) -> None:
        if self.task:
            self.task.cancel()

    def get_status_emoji(self, name: StatusEmoji) -> str:
        if name not in StatusEmoji.__args__:
            raise ValueError
        emoji: Optional[discord.Emoji] = discord.utils.get(
            self.bot.emojis, id=self.emojis["status"].get(name)
        )
        return str(emoji) if emoji else DEFAULT

    def get_device_status_emoji(self, name: DeviceEmoji) -> str:
        if name not in DeviceEmoji.__args__:
            raise ValueError
        emoji: Optional[discord.Emoji] = discord.utils.get(
            self.bot.emojis,
            id=cast(Dict[str, Optional[int]], self.emojis["status"]["device"]).get(name),
        )
        return str(emoji) if emoji else DEFAULT

    def get_badge_emoji(self, name: BadgeEmoji) -> str:
        if name not in BadgeEmoji.__args__:
            raise ValueError
        emoji: Optional[discord.Emoji] = discord.utils.get(
            self.bot.emojis, id=self.emojis["badge"].get(name)
        )
        return str(emoji) if emoji else DEFAULT

    def get_select_emoji(self, name: SelectEmoji) -> str:
        if name not in SelectEmoji.__args__:
            raise ValueError
        emoji: Optional[discord.Emoji] = discord.utils.get(
            self.bot.emojis,
            id=cast(Dict[str, Optional[int]], self.emojis["settings"]["select"]).get(name),
        )
        return str(emoji) if emoji else DEFAULT

    async def set_status_emoji(self, name: StatusEmoji, emoji: int) -> None:
        if name not in StatusEmoji.__args__:
            raise ValueError
        async with self.config.status() as emojis:
            emojis[name] = emoji
        self.emojis["status"][name] = emoji

    async def set_device_emoji(self, name: DeviceEmoji, emoji: int) -> None:
        if name not in DeviceEmoji.__args__:
            raise ValueError
        async with self.config.status.device() as emojis:  # type: ignore
            emojis[name] = emoji
        if "device" not in self.emojis["status"]:
            self.emojis["status"] = {"device": {}}
        cast(Dict[str, int], self.emojis["status"]["device"])[name] = emoji

    async def set_badge_emoji(self, name: BadgeEmoji, emoji: int) -> None:
        if name not in BadgeEmoji.__args__:
            raise ValueError
        async with self.config.badge() as emojis:
            emojis[name] = emoji
        self.emojis["badge"][name] = emoji

    async def set_select_emoji(self, name: SelectEmoji, emoji: int) -> None:
        if name not in SelectEmoji.__args__:
            raise ValueError
        async with self.config.settings.select() as emojis:  # type: ignore
            emojis[name] = emoji
        if "select" not in self.emojis["settings"]:
            self.emojis["settings"] = {"select": {}}
        cast(Dict[str, int], self.emojis["settings"]["select"])[name] = emoji

    def get_member_device_status(self, member: discord.Member) -> Tuple[str, str, str]:
        mobile: str = {
            discord.Status.online: self.get_device_status_emoji("mobile_online"),
            discord.Status.idle: self.get_device_status_emoji("mobile_idle"),
            discord.Status.dnd: self.get_device_status_emoji("mobile_dnd"),
            discord.Status.offline: self.get_device_status_emoji("mobile_offline"),
        }[member.mobile_status]
        web: str = {
            discord.Status.online: self.get_device_status_emoji("web_online"),
            discord.Status.idle: self.get_device_status_emoji("web_idle"),
            discord.Status.dnd: self.get_device_status_emoji("web_dnd"),
            discord.Status.offline: self.get_device_status_emoji("web_offline"),
        }[member.web_status]
        desktop: str = {
            discord.Status.online: self.get_device_status_emoji("desktop_online"),
            discord.Status.idle: self.get_device_status_emoji("desktop_idle"),
            discord.Status.dnd: self.get_device_status_emoji("desktop_dnd"),
            discord.Status.offline: self.get_device_status_emoji("desktop_offline"),
        }[member.desktop_status]
        return mobile, web, desktop

    def get_special_badges(self, user: discord.Member) -> List[str]:
        special: List[str] = []
        for guild_id, roles in self.emojis["special"].items():
            if (guild := self.bot.get_guild(int(guild_id))) and (
                member := guild.get_member(user.id)
            ):
                for r in reversed(member.roles):
                    if str(r.id) in roles:  # type: ignore
                        special.append(
                            "{} {}".format(
                                self.bot.get_emoji(cast(Dict[str, int], roles)[str(r.id)]),
                                r.name.title(),
                            )
                        )
        return special

    async def set_special_badge(self, guild: int, role: int, emoji: int) -> None:
        async with self.config.special() as special:
            if str(guild) not in special:
                special[guild] = {}
            special[guild][role] = emoji
        if str(guild) not in self.emojis["special"]:
            self.emojis["special"] = {str(guild): {}}
        cast(Dict[str, int], self.emojis["special"][str(guild)])[str(role)] = emoji

    async def initialize(self) -> None:
        self.emojis["status"] = await self.config.status()
        self.emojis["badge"] = await self.config.badge()
        self.emojis["special"] = await self.config.special()
        self.emojis["settings"] = await self.config.settings()

    async def get_user_badges(self, user: discord.Member) -> Tuple[str, int]:
        flags: List[str] = [f.name for f in user.public_flags.all()]
        badges: str = ""
        count: int = 0
        if flags:
            for badge in sorted(flags):
                emoji: str = self.get_badge_emoji(cast(BadgeEmoji, badge))
                badges += "{} {}\n".format(emoji, badge.replace("_", " ").title())
            count += 1
        return badges, count