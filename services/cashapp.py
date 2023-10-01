from typing import Optional, Self

import httpx
from discord_webhook import DiscordEmbed
from httpx import Response
from loguru import logger


class CashApp:
    """
    Class to integrate with Cash App and build objects specific to the
    Cash App platform.
    """

    def IsUserAvailable(self: Self, cashtag: str) -> bool:
        """Determine if a Cash App $Cashtag is available."""

        status: Optional[int] = None

        try:
            res: Response = httpx.get(
                f"https://cash.app/${cashtag}", follow_redirects=True
            )
            status = res.status_code

            logger.trace(f"HTTP {status} GET {res.url}: {res.text}")
        except Exception as e:
            logger.opt(exception=e).error(
                f"Failed to determine availability of Cash App $Cashtag ${cashtag}"
            )

        # Cash App returns HTTP 404 (Not Found) for non-existent accounts,
        # and HTTP 200 (Success) for existing accounts.
        if status:
            if status == 404:
                logger.success(f"Cash App $Cashtag ${cashtag} is available")

                return True
            elif status == 200:
                logger.info(
                    f"Fetched Cash App user ${cashtag}, $Cashtag is unavailable"
                )

        return False

    def BuildEmbed(self: Self, cashtag: str) -> DiscordEmbed:
        """Build a Discord embed object for an available Cash App $Cashtag."""

        embed: DiscordEmbed = DiscordEmbed()

        embed.set_description(
            f"Cash App $Cashtag [${cashtag}](https://cash.app/${cashtag}) is currently available."
        )
        embed.set_color("00C244")
        embed.set_footer(text="Cash App", icon_url="https://i.imgur.com/Mbr5HTD.png")

        return embed
