from typing import Self

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

        try:
            res: Response = httpx.get(f"https://github.com/{username}")
        except Exception as e:
            logger.error(
                f"Failed to determine availability of GitHub username @{username}, {e}"
            )

        # GitHub returns HTTP 404 (Not Found) for non-existent accounts,
        # while HTTP 200 (Success) is returned for existing accounts.
        if res.status_code == 404:
            return True

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
