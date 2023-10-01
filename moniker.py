import logging
from datetime import datetime, timezone
from os import environ
from sys import exit, stdout
from typing import List, Self

import dotenv
from discord_webhook import DiscordEmbed, DiscordWebhook
from httpx import TimeoutException
from loguru import logger
from loguru_discord import DiscordSink

from handlers import Intercept
from services import CashApp, GitHub, Mastodon, Snapchat, Twitter, Venmo, YouTube


class Moniker:
    """
    Monitor usernames across various services and report availability via Discord.

    https://github.com/EthanC/Moniker
    """

    def Start(self: Self) -> None:
        """Initialize Moniker and begin primary functionality."""

        logger.info("Moniker")
        logger.info("https://github.com/EthanC/Moniker")

        # Reroute standard logging to Loguru
        logging.basicConfig(handlers=[Intercept()], level=0, force=True)

        if dotenv.load_dotenv():
            logger.success("Loaded environment variables")
            logger.trace(environ)

        if level := environ.get("LOG_LEVEL"):
            logger.remove()
            logger.add(stdout, level=level)

            logger.success(f"Set console logging level to {level}")

        if url := environ.get("LOG_DISCORD_WEBHOOK_URL"):
            logger.add(
                DiscordSink(url, suppress=[TimeoutException]),
                level=environ.get("LOG_DISCORD_WEBHOOK_LEVEL"),
                backtrace=False,
            )

            logger.success(f"Enabled logging to Discord webhook")
            logger.trace(url)

        Moniker.CheckCashApp(self)
        Moniker.CheckGitHub(self)
        Moniker.CheckMastodon(self)
        Moniker.CheckSnapchat(self)
        Moniker.CheckTwitter(self)
        Moniker.CheckVenmo(self)
        Moniker.CheckYouTube(self)

        logger.success("Completed username availability checks for all services")

    def CheckCashApp(self: Self) -> None:
        """Check availability of the configured Cash App $Cashtags."""

        if not (var := environ.get("CASHAPP_USERNAMES")):
            logger.info("Skipping Cash App, no $Cashtags configured")

            return

        cashtags: List[str] = var.split(",")

        logger.trace(cashtags)

        for cashtag in cashtags:
            if not CashApp.IsUserAvailable(self, cashtag):
                continue

            if url := environ.get("DISCORD_WEBHOOK_URL"):
                embed: DiscordEmbed = CashApp.BuildEmbed(self, cashtag)

                Moniker.Notify(self, url, embed)

        logger.info("Completed $Cashtag availability checks for Cash App")

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

            if url := environ.get("DISCORD_WEBHOOK_URL"):
                embed: DiscordEmbed = GitHub.BuildEmbed(self, username)

                Moniker.Notify(self, url, embed)

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

            if url := environ.get("DISCORD_WEBHOOK_URL"):
                embed: DiscordEmbed = Mastodon.BuildEmbed(self, username)

                Moniker.Notify(self, url, embed)

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

            if url := environ.get("DISCORD_WEBHOOK_URL"):
                embed: DiscordEmbed = Snapchat.BuildEmbed(self, username)

                Moniker.Notify(self, url, embed)

        logger.info("Completed username availability checks for Snapchat")

    def CheckTwitter(self: Self) -> None:
        """Check availability of the configured Twitter usernames."""

        if not (var := environ.get("TWITTER_USERNAMES")):
            logger.info("Skipping Twitter, no usernames configured")

            return

        usernames: List[str] = var.split(",")

        logger.trace(usernames)

        for username in usernames:
            if not Twitter.IsUserAvailable(self, username):
                continue

            if url := environ.get("DISCORD_WEBHOOK_URL"):
                embed: DiscordEmbed = Twitter.BuildEmbed(self, username)

                Moniker.Notify(self, url, embed)

        logger.info("Completed username availability checks for Twitter")

    def CheckVenmo(self: Self) -> None:
        """Check availability of the configured Venmo usernames."""

        if not (var := environ.get("VENMO_USERNAMES")):
            logger.info("Skipping Venmo, no usernames configured")

            return

        usernames: List[str] = var.split(",")

        logger.trace(usernames)

        for username in usernames:
            if not Venmo.IsUserAvailable(self, username):
                continue

            if url := environ.get("DISCORD_WEBHOOK_URL"):
                embed: DiscordEmbed = Venmo.BuildEmbed(self, username)

                Moniker.Notify(self, url, embed)

        logger.info("Completed username availability checks for Venmo")

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

            if url := environ.get("DISCORD_WEBHOOK_URL"):
                embed: DiscordEmbed = YouTube.BuildEmbed(self, username)

                Moniker.Notify(self, url, embed)

        logger.info("Completed username availability checks for YouTube")

    def Notify(self: Self, url: str, embed: DiscordEmbed) -> None:
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
