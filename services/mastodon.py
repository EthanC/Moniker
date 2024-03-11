from typing import Self

import httpx
from discord_webhook import DiscordEmbed
from httpx import Response
from loguru import logger


class Mastodon:
    """
    Class to integrate with Mastodon and build objects specific to the
    Mastodon platform.
    """

    def IsUserAvailable(self: Self, username: str) -> bool:
        """Determine if a Mastodon username is available."""

        status: int | None = None

        try:
            res: Response = httpx.get(
                f"https://mastodon.social/api/v1/accounts/lookup?acct={username}"
            )
            status = res.status_code

            logger.trace(f"HTTP {status} GET {res.url}: {res.text}")
        except Exception as e:
            logger.opt(exception=e).error(
                f"Failed to determine availability of Mastodon username @{username}"
            )

        # Mastodon returns HTTP 404 (Not Found) for non-existent accounts,
        # and HTTP 200 (Success) for existing accounts.
        if status:
            if status == 404:
                logger.success(f"Mastodon username @{username} is available")

                return True
            elif status == 200:
                logger.info(
                    f"Fetched Mastodon user @{username}, username is unavailable"
                )

        return False

    def BuildEmbed(self: Self, username: str) -> DiscordEmbed:
        """Build a Discord embed object for an available Mastodon username."""

        embed: DiscordEmbed = DiscordEmbed()

        embed.set_description(
            f"Mastodon username [@{username}](https://mastodon.social/@{username}) is currently available."
        )
        embed.set_color("6364FF")
        embed.set_footer(text="Mastodon", icon_url="https://i.imgur.com/Xh51yxT.png")

        return embed
