from typing import Optional, Self

import httpx
from discord_webhook import DiscordEmbed
from httpx import Response
from loguru import logger


class Snapchat:
    """
    Class to integrate with Snapchat and build objects specific to the
    Snapchat platform.
    """

    def IsUserAvailable(self: Self, username: str) -> bool:
        """Determine if a Snapchat username is available."""

        status: Optional[int] = None

        try:
            res: Response = httpx.get(
                f"https://www.snapchat.com/add/{username}", follow_redirects=True
            )
            status = res.status_code

            logger.trace(f"HTTP {status} GET {res.url}: {res.text}")
        except Exception as e:
            logger.opt(exception=e).error(
                f"Failed to determine availability of Snapchat username @{username}"
            )

        # Snapchat returns HTTP 404 (Not Found) for non-existent accounts,
        # and HTTP 200 (Success) for existing accounts.
        if status:
            if status == 404:
                logger.success(f"Snapchat username @{username} is available")

                return True
            elif status == 200:
                logger.info(
                    f"Fetched Snapchat user @{username}, username is unavailable"
                )

        return False

    def BuildEmbed(self: Self, username: str) -> DiscordEmbed:
        """Build a Discord embed object for an available Snapchat username."""

        embed: DiscordEmbed = DiscordEmbed()

        embed.set_description(
            f"Snapchat username [@{username}](https://snapchat.com/add/{username}) is currently available."
        )
        embed.set_color("FFFC00")
        embed.set_footer(text="Snapchat", icon_url="https://i.imgur.com/NARmOty.png")

        return embed
