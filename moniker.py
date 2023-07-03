from datetime import datetime, timezone
from os import environ
from sys import exit, stdout
from typing import List, Self

import dotenv
from discord_webhook import DiscordEmbed, DiscordWebhook
from loguru import logger
from loguru_discord import DiscordSink

from services import GitHub, Mastodon, Snapchat, Twitter, YouTube


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

        if level := environ.get("LOG_LEVEL"):
            logger.remove()
            logger.add(stdout, level=level)

            logger.success(f"Set logging level to {level}")

        if url := environ.get("LOG_DISCORD_WEBHOOK_URL"):
            logger.add(
                DiscordSink(url),
                level=environ.get("LOG_DISCORD_WEBHOOK_LEVEL"),
                backtrace=False,
            )

            logger.success(f"Enabled logging to Discord webhook")
            logger.trace(url)

        Moniker.CheckGitHub(self)
        Moniker.CheckMastodon(self)
        Moniker.CheckSnapchat(self)
        Moniker.CheckTwitter(self)
        Moniker.CheckYouTube(self)

        logger.success("Completed username availability checks for all services")

    def CheckGitHub(self: Self) -> None:
        """Check availability of the configured GitHub usernames."""

        if not (var := environ.get("GITHUB_USERNAMES")):
            logger.info("Skipping GitHub, no usernames configured")

            return

        usernames: List[str] = var.split(",")

        logger.trace(usernames)

        for username in usernames:
            if not GitHub.IsUserAvailable(self, username):
                continue

            if environ.get("DISCORD_WEBHOOK_URL"):
                embed: DiscordEmbed = GitHub.BuildEmbed(self, username)

                Moniker.Notify(self, embed)

        logger.info("Completed username availability checks for GitHub")

    def CheckMastodon(self: Self) -> None:
        """Check availability of the configured Mastodon usernames."""

        if not (var := environ.get("MASTODON_USERNAMES")):
            logger.info("Skipping Mastodon, no usernames configured")

            return

        usernames: List[str] = var.split(",")

        logger.trace(usernames)

        for username in usernames:
            if not Mastodon.IsUserAvailable(self, username):
                continue

            if environ.get("DISCORD_WEBHOOK_URL"):
                embed: DiscordEmbed = Mastodon.BuildEmbed(self, username)

                Moniker.Notify(self, embed)

        logger.info("Completed username availability checks for Mastodon")

    def CheckSnapchat(self: Self) -> None:
        """Check availability of the configured Snapchat usernames."""

        if not (var := environ.get("SNAPCHAT_USERNAMES")):
            logger.info("Skipping Snapchat, no usernames configured")

            return

        usernames: List[str] = var.split(",")

        logger.trace(usernames)

        for username in usernames:
            if not Snapchat.IsUserAvailable(self, username):
                continue

            if environ.get("DISCORD_WEBHOOK_URL"):
                embed: DiscordEmbed = Snapchat.BuildEmbed(self, username)

                Moniker.Notify(self, embed)

        logger.info("Completed username availability checks for Snapchat")

    def CheckTwitter(self: Self) -> None:
        """Check availability of the configured Twitter usernames."""

        if not (var := environ.get("TWITTER_USERNAMES")):
            logger.info("Skipping Twitter, no usernames configured")

            return

        usernames: List[str] = var.split(",")

        logger.trace(usernames)

        for username in usernames:
            # TODO: Testing
            Twitter.IsUserAvailable(self, username)
            break

            if not Twitter.IsUserAvailable(self, username):
                continue

            if environ.get("DISCORD_WEBHOOK_URL"):
                embed: DiscordEmbed = Twitter.BuildEmbed(self, username)

                Moniker.Notify(self, embed)

        logger.info("Completed username availability checks for Twitter")

    def CheckYouTube(self: Self) -> None:
        """Check availability of the configured YouTube usernames."""

        if not (var := environ.get("YOUTUBE_USERNAMES")):
            logger.info("Skipping YouTube, no usernames configured")

            return

        usernames: List[str] = var.split(",")

        logger.trace(usernames)

        for username in usernames:
            if not YouTube.IsUserAvailable(self, username):
                continue

            if environ.get("DISCORD_WEBHOOK_URL"):
                embed: DiscordEmbed = YouTube.BuildEmbed(self, username)

                Moniker.Notify(self, embed)

        logger.info("Completed username availability checks for YouTube")

    def Notify(self: Self, embed: DiscordEmbed) -> None:
        """Report username availability to the configured Discord webhook."""

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
