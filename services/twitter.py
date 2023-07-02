import json
from typing import Any, Dict, Optional, Self

import httpx
from bs4 import BeautifulSoup
from discord_webhook import DiscordEmbed
from httpx import Response
from loguru import logger


class Twitter:
    """
    Class to integrate with Twitter and build objects specific to the
    Twitter platform.
    """

    def IsUserAvailable(self: Self, username: str) -> bool:
        """Determine if a Twitter username is available."""

        data: Dict[str, Any] = {}

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
            logger.error(
                f"Failed to determine availability of Twitter username @{username}, {e}"
            )

        # TODO: Due to limitations of this unsupported API, usernames
        # held by suspended accounts will report as available.
        #
        # As of 7/2/2023, "temporary" measures are in-place to prevent
        # acess to page content without authorization. If this blocker
        # is to be lifted, we can avoid the API entirely and instead
        # scrape the empty_state_header_text from profile pages.
        # https://twitter.com/elonmusk/status/1674865731136020505
        results: Optional[bool] = data.get("hasResults")

        if results is not None:
            if not results:
                logger.success(f"Twitter username @{username} is available")

                return True

        logger.info(f"Fetched Twitter user @{username}, username is unavailable")

        return False

    def BuildEmbed(self: Self, username: str) -> DiscordEmbed:
        """Build a Discord embed object for an available Twitter username."""

        embed: DiscordEmbed = DiscordEmbed()

        embed.set_description(
            f"Twitter username [@{username}](https://twitter.com/{username}) is currently available."
        )
        embed.set_color("1D9BF0")
        embed.set_footer(text="Twitter", icon_url="https://i.imgur.com/6BAmj0I.png")

        return embed
