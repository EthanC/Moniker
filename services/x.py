import json
from typing import Any, Self

import httpx
from bs4 import BeautifulSoup
from discord_webhook import DiscordEmbed
from httpx import Response
from loguru import logger


class X:
    """
    Class to integrate with X and build objects specific to the
    X platform.
    """

    def IsUserAvailable(self: Self, username: str) -> bool:
        """Determine if a X username is available."""

        data: dict[str, Any] = {}

        try:
            res: Response = httpx.get(
                f"https://syndication.twitter.com/srv/timeline-profile/screen-name/{username}"
            )

            res.raise_for_status()

            logger.trace(res.text)

            if not res.text:
                raise ValueError("response body is null")

            parser: BeautifulSoup = BeautifulSoup(res.text, "html.parser")
            script: str = parser.find("script", attrs={"id": "__NEXT_DATA__"}).string

            logger.trace(script)

            data = json.loads(script)
            data = data["props"]["pageProps"]["contextProvider"]
        except Exception as e:
            logger.opt(exception=e).error(
                f"Failed to determine availability of X username @{username}"
            )

            return False

        # TODO: Due to limitations of this unsupported API, usernames
        # held by suspended accounts will report as available.
        #
        # As of 7/2/2023, "temporary" measures are in-place to prevent
        # acess to page content without authorization. If this blocker
        # is to be lifted, we can avoid the API entirely and instead
        # scrape the empty_state_header_text from profile pages.
        # https://x.com/elonmusk/status/1674865731136020505
        results: bool | None = data.get("hasResults")

        if not results:
            logger.success(f"X username @{username} is available")

            return True

        logger.info(f"Fetched X user @{username}, username is unavailable")

        return False

    def BuildEmbed(self: Self, username: str) -> DiscordEmbed:
        """Build a Discord embed object for an available X username."""

        embed: DiscordEmbed = DiscordEmbed()

        embed.set_description(
            f"X username [@{username}](https://x.com/{username}) is currently available."
        )
        embed.set_color("1D9BF0")
        embed.set_footer(text="X", icon_url="https://i.imgur.com/hZbC8my.png")

        return embed
