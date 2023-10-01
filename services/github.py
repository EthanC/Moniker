from typing import Optional, Self

import httpx
from discord_webhook import DiscordEmbed
from httpx import Response
from loguru import logger


class GitHub:
    """
    Class to integrate with GitHub and build objects specific to the
    GitHub platform.
    """

    def IsUserAvailable(self: Self, username: str) -> bool:
        """Determine if a GitHub username is available."""

        status: Optional[int] = None

        try:
            res: Response = httpx.get(f"https://github.com/{username}")
            status = res.status_code

            logger.trace(f"HTTP {status} GET {res.url}: {res.text}")
        except Exception as e:
            logger.opt(exception=e).error(
                f"Failed to determine availability of GitHub username @{username}"
            )

        # GitHub returns HTTP 404 (Not Found) for non-existent accounts,
        # and HTTP 200 (Success) for existing accounts.
        if status:
            if status == 404:
                logger.success(f"GitHub username @{username} is available")

                return True
            elif status == 200:
                logger.info(f"Fetched GitHub user @{username}, username is unavailable")

        return False

    def BuildEmbed(self: Self, username: str) -> DiscordEmbed:
        """Build a Discord embed object for an available GitHub username."""

        embed: DiscordEmbed = DiscordEmbed()

        embed.set_description(
            f"GitHub username [@{username}](https://github.com/{username}) is currently available."
        )
        embed.set_color("171515")
        embed.set_footer(text="GitHub", icon_url="https://i.imgur.com/C3M0uwh.png")

        return embed
