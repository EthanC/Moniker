from typing import Optional, Self

import httpx
from discord_webhook import DiscordEmbed
from httpx import Response, TimeoutException
from loguru import logger


class Venmo:
    """
    Class to integrate with Venmo and build objects specific to the
    Venmo platform.
    """

    def IsUserAvailable(self: Self, username: str) -> bool:
        """Determine if a Venmo username is available."""

        status: Optional[int] = None

        try:
            res: Response = httpx.get(
                f"https://venmo.com/u/{username}", follow_redirects=True
            )
            status = res.status_code

            logger.trace(f"HTTP {status} GET {res.url}: {res.text}")
        except TimeoutException as e:
            logger.opt(exception=e).debug(
                f"Ignoring Venmo timeout for username @{username}"
            )
        except Exception as e:
            logger.opt(exception=e).error(
                f"Failed to determine availability of Venmo username @{username}"
            )

        # Venmo returns HTTP 404 (Not Found) for non-existent accounts,
        # and HTTP 200 (Success) for existing accounts.
        if status:
            if status == 404:
                logger.success(f"Venmo username @{username} is available")

                return True
            elif status == 200:
                logger.info(f"Fetched Venmo user @{username}, username is unavailable")

        return False

    def BuildEmbed(self: Self, username: str) -> DiscordEmbed:
        """Build a Discord embed object for an available Venmo username."""

        embed: DiscordEmbed = DiscordEmbed()

        embed.set_description(
            f"Venmo username [@{username}](https://venmo.com/u/{username}) is currently available."
        )
        embed.set_color("008CFF")
        embed.set_footer(text="Venmo", icon_url="https://i.imgur.com/F2Vsv73.png")

        return embed
