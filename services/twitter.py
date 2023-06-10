from os import environ
from typing import Optional, Self

from discord_webhook import DiscordEmbed
from loguru import logger
from tweepy import API, OAuth1UserHandler
from tweepy.errors import Forbidden, NotFound
from tweepy.models import User


class Twitter:
    """
    Class to integrate with the Twitter API and build objects specific
    to the Twitter platform.
    """

    def Authenticate(self: Self) -> Optional[API]:
        """Authenticate with Twitter using the configured credentials."""

        try:
            client: API = API(
                OAuth1UserHandler(
                    environ.get("TWITTER_API_KEY"),
                    environ.get("TWITTER_API_KEY_SECRET"),
                    environ.get("TWITTER_ACCESS_TOKEN"),
                    environ.get("TWITTER_ACCESS_TOKEN_SECRET"),
                )
            )

            client.verify_credentials()
        except Exception as e:
            logger.error(f"Failed to authenticate with Twitter, {e}")

            return

        logger.success("Authenticated with Twitter")

        return client

    def IsUserAvailable(self: Self, client: API, username: str) -> bool:
        """Determine if a Twitter username is available."""

        try:
            user: User = client.get_user(screen_name=username)

            logger.info(
                f"Fetched Twitter user @{username} ({user.id}), username is unavailable"
            )
            logger.trace(user)
        except NotFound:
            logger.success(f"Twitter username @{username} is available")

            return True
        except Forbidden as e:
            # Forbidden exceptions are typically used for suspended
            # accounts, no need to log as an error.
            logger.info(f"Failed to fetch Twitter user @{username}, {e}")
        except Exception as e:
            logger.error(f"Failed to fetch Twitter user @{username}, {e}")

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
