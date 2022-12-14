import os
from datetime import datetime
from sys import exit
from typing import List, Optional, Self

import dotenv
from discord_webhook import DiscordEmbed, DiscordWebhook
from loguru import logger
from notifiers.logging import NotificationHandler
from tweepy import Client

from services import Twitter


class Moniker:
    """
    Twitter username watcher that reports availability via Discord.

    https://github.com/EthanC/Moniker
    """

    def Start(self: Self) -> None:
        """Initialize Moniker and begin primary functionality."""

        logger.info("Moniker")
        logger.info("https://github.com/EthanC/Moniker")

        if dotenv.load_dotenv():
            logger.success("Loaded environment variables")
            logger.trace(os.environ)

        if logUrl := os.environ.get("DISCORD_LOG_WEBHOOK"):
            if not (logLevel := os.environ.get("DISCORD_LOG_LEVEL")):
                logger.critical("Level for Discord webhook logging is not set")

                return

            logger.add(
                NotificationHandler(
                    "slack", defaults={"webhook_url": f"{logUrl}/slack"}
                ),
                level=logLevel,
                format="```\n{time:YYYY-MM-DD HH:mm:ss.SSS} | {level:<8} | {name}:{function}:{line} - {message}\n```",
            )

            logger.success(f"Enabled logging to Discord webhook")
            logger.trace(logUrl)

        Moniker.CheckTwitter(self)

    def CheckTwitter(self: Self) -> None:
        """Check availability of the configured Twitter usernames."""

        client: Optional[Client] = Twitter.Authenticate(self)

        if not client:
            return

        usernames: List[str] = []

        if var := os.environ.get("TWITTER_USERNAMES"):
            usernames = var.split(",")

        logger.trace(usernames)

        for username in usernames:
            if not Twitter.IsUserAvailable(self, client, username):
                continue

            if os.environ.get("DISCORD_NOTIFY_WEBHOOK"):
                embed: DiscordEmbed = Twitter.BuildEmbed(self, username)

                Moniker.Notify(self, embed)

        logger.info("Completed availability check for all configured Twitter usernames")

    def Notify(self: Self, embed: DiscordEmbed) -> None:
        """Report username availability to the configured Discord webhook."""

        if not (url := os.environ.get("DISCORD_NOTIFY_WEBHOOK")):
            logger.info("Discord webhook for notifications is not set")

            return

        embed.set_author(
            "Moniker",
            url="https://github.com/EthanC/Moniker",
            icon_url="https://i.imgur.com/lhTfe8m.png",
        )
        embed.set_timestamp(datetime.now().timestamp())

        DiscordWebhook(url=url, embeds=[embed], rate_limit_retry=True).execute()


if __name__ == "__main__":
    try:
        Moniker.Start(Moniker)
    except KeyboardInterrupt:
        exit()
