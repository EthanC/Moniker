from typing import Self

import httpx
from discord_webhook import DiscordEmbed
from httpx import Response
from loguru import logger


class YouTube:
    """
    Class to integrate with YouTube and build objects specific to the
    YouTube platform.
    """

    def IsUserAvailable(self: Self, username: str) -> bool:
        """Determine if a YouTube username is available."""

        status: int | None = None

        try:
            res: Response = httpx.get(
                f"https://youtube.com/@{username}", follow_redirects=True
            )
            status = res.status_code

            logger.trace(f"HTTP {status} GET {res.url}: {res.text}")
        except Exception as e:
            logger.opt(exception=e).error(
                f"Failed to determine availability of YouTube username @{username}"
            )

        # YouTube returns HTTP 404 (Not Found) for non-existent accounts,
        # and HTTP 200 (Success) for existing accounts.
        if status:
            if status == 404:
                logger.success(f"YouTube username @{username} is available")

                return True
            elif status == 200:
                logger.info(
                    f"Fetched YouTube user @{username}, username is unavailable"
                )

        return False

    def BuildEmbed(self: Self, username: str) -> DiscordEmbed:
        """Build a Discord embed object for an available YouTube username."""

        embed: DiscordEmbed = DiscordEmbed()

        embed.set_description(
            f"YouTube username [@{username}](https://youtube.com/@{username}) is currently available."
        )
        embed.set_color("FF0000")
        embed.set_footer(text="YouTube", icon_url="https://i.imgur.com/sBcs6ct.png")

        return embed
