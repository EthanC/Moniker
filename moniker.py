from datetime import datetime, timezone
from os import environ
from sys import exit
from typing import List, Optional, Self

import dotenv
from discord_webhook import DiscordEmbed, DiscordWebhook
from loguru import logger
from notifiers.logging import NotificationHandler
from tweepy import Client

from services import GitHub, Mastodon, Snapchat, Twitter


class Moniker:
    """
    Monitor usernames across various services and report availability via Discord.

    https://github.com/EthanC/Moniker
    """

    def Start(self: Self) -> None:
        """Initialize Moniker and begin primary functionality."""

        logger.info("Moniker")
        logger.info("https://github.com/EthanC/Moniker")

        if dotenv.load_dotenv():
            logger.success("Loaded environment variables")
            logger.trace(environ)

        if logUrl := environ.get("DISCORD_LOG_WEBHOOK"):
            if not (logLevel := environ.get("DISCORD_LOG_LEVEL")):
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

        Moniker.CheckGitHub(self)
        Moniker.CheckMastodon(self)
        Moniker.CheckSnapchat(self)
        Moniker.CheckTwitter(self)

    def CheckGitHub(self: Self) -> None:
        """Check availability of the configured GitHub usernames."""

        if not (var := environ.get("GITHUB_USERNAMES")):
            logger.info(
                "Skipping availability check for GitHub, no usernames configured"
            )

            return

        usernames: List[str] = var.split(",")

        logger.trace(usernames)

        for username in usernames:
            if not GitHub.IsUserAvailable(self, username):
                continue

            if environ.get("DISCORD_NOTIFY_WEBHOOK"):
                embed: DiscordEmbed = GitHub.BuildEmbed(self, username)

                Moniker.Notify(self, embed)

        logger.info("Completed availability check for all configured GitHub usernames")

    def CheckMastodon(self: Self) -> None:
        """Check availability of the configured Mastodon usernames."""

        if not (var := environ.get("MASTODON_USERNAMES")):
            logger.info(
                "Skipping availability check for Mastodon, no usernames configured"
            )

            return

        usernames: List[str] = var.split(",")

        logger.trace(usernames)

        for username in usernames:
            if not Mastodon.IsUserAvailable(self, username):
                continue

            if environ.get("DISCORD_NOTIFY_WEBHOOK"):
                embed: DiscordEmbed = Mastodon.BuildEmbed(self, username)

                Moniker.Notify(self, embed)

        logger.info(
            "Completed availability check for all configured Mastodon usernames"
        )

    def CheckSnapchat(self: Self) -> None:
        """Check availability of the configured Snapchat usernames."""

        if not (var := environ.get("SNAPCHAT_USERNAMES")):
            logger.info(
                "Skipping availability check for Snapchat, no usernames configured"
            )

            return

        usernames: List[str] = var.split(",")

        logger.trace(usernames)

        for username in usernames:
            if not Snapchat.IsUserAvailable(self, username):
                continue

            if environ.get("DISCORD_NOTIFY_WEBHOOK"):
                embed: DiscordEmbed = Snapchat.BuildEmbed(self, username)

                Moniker.Notify(self, embed)

        logger.info(
            "Completed availability check for all configured Snapchat usernames"
        )

    def CheckTwitter(self: Self) -> None:
        """Check availability of the configured Twitter usernames."""

        if not (var := environ.get("TWITTER_USERNAMES")):
            logger.info(
                "Skipping availability check for Twitter, no usernames configured"
            )

            return

        usernames: List[str] = var.split(",")

        logger.trace(usernames)

        client: Optional[Client] = Twitter.Authenticate(self)

        if not client:
            return

        for username in usernames:
            if not Twitter.IsUserAvailable(self, client, username):
                continue

            if environ.get("DISCORD_NOTIFY_WEBHOOK"):
                embed: DiscordEmbed = Twitter.BuildEmbed(self, username)

                Moniker.Notify(self, embed)

        logger.info("Completed availability check for all configured Twitter usernames")

    def Notify(self: Self, embed: DiscordEmbed) -> None:
        """Report username availability to the configured Discord webhook."""

        if not (url := environ.get("DISCORD_NOTIFY_WEBHOOK")):
            logger.info("Discord webhook for notifications is not set")

            return

        embed.set_author(
            "Moniker",
            url="https://github.com/EthanC/Moniker",
            icon_url="https://i.imgur.com/gImd2zu.png",
        )
        embed.set_timestamp(datetime.now(timezone.utc).timestamp())

        DiscordWebhook(url=url, embeds=[embed], rate_limit_retry=True).execute()


if __name__ == "__main__":
    try:
        Moniker.Start(Moniker)
    except KeyboardInterrupt:
        exit()
