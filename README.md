# Moniker

Moniker is a Twitter username watcher that reports availability via Discord.

# Setup

[Twitter API](https://developer.twitter.com/en/docs/twitter-api) credentials are required for functionality, and a [Discord Webhook](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks) is recommended for notifications. Regardless of your chosen setup method, Moniker is intended for use with a task scheduler, such as [cron](https://crontab.guru/).

**Environment Variables:**

-   `TWITTER_ACCESS_TOKEN` (Required): [Twitter API](https://developer.twitter.com/en/docs/twitter-api) Access Token.
-   `TWITTER_ACCESS_TOKEN_SECRET` (Required): [Twitter API](https://developer.twitter.com/en/docs/twitter-api) Access Token Secret.
-   `TWITTER_API_KEY` (Required): [Twitter API](https://developer.twitter.com/en/docs/twitter-api) Key.
-   `TWITTER_API_KEY_SECRET` (Required): [Twitter API](https://developer.twitter.com/en/docs/twitter-api) Key Secret.
-   `TWITTER_USERNAMES` (Required): Comma-separated list of Twitter usernames to watch.
-   `DISCORD_NOTIFY_WEBHOOK`: [Discord Webhook](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks) URL to receive available username notifications.
-   `DISCORD_LOG_WEBHOOK`: [Discord Webhook](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks) URL to receive log events.
-   `DISCORD_LOG_LEVEL`: Minimum [Loguru](https://loguru.readthedocs.io/en/stable/api/logger.html) severity level to forward to Discord.

## Docker (Recommended)

Clone the Moniker GitHub repository, then run `docker compose up`. Alternatively, create a [Stack](https://docs.portainer.io/user/docker/stacks/add) in Portainer using the provided `docker-compose.yml` example file.

https://github.com/EthanC/Moniker/blob/main/docker-compose.yml

## Standalone

Moniker is built for [Python 3.11](https://www.python.org/) or greater.

1. Install required dependencies using [Poetry](https://python-poetry.org/): `poetry install`
2. Rename `.env_example` to `.env`, then provide the environment variables.
3. Start Moniker: `python moniker.py`
