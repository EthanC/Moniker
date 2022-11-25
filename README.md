# Moniker

Moniker is a Twitter username watcher that reports availability via Discord.

# Setup

[Twitter API](https://developer.twitter.com/en/docs/twitter-api) credentials are required for functionality, and a [Discord Webhook](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks) is recommended for notifications.

Regardless of your chosen setup method, Moniker is intended for use with a task scheduler, such as [cron](https://crontab.guru/).

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

Modify the following `docker-compose.yml` example file, then run `docker compose up`.

```yml
version: "3"
services:
  moniker:
    container_name: moniker
    image: ethanchrisp/moniker:latest
    environment:
      TWITTER_ACCESS_TOKEN: XXXXXXXX
      TWITTER_ACCESS_TOKEN_SECRET: XXXXXXXX
      TWITTER_API_KEY: XXXXXXXX
      TWITTER_API_KEY_SECRET: XXXXXXXX
      TWITTER_USERNAMES: username123,user_name,jack
      DISCORD_NOTIFY_WEBHOOK: https://discord.com/api/webhooks/XXXXXXXX/XXXXXXXX
      DISCORD_LOG_WEBHOOK: https://discord.com/api/webhooks/XXXXXXXX/XXXXXXXX
      DISCORD_LOG_LEVEL: WARNING
```

## Standalone

Moniker is built for [Python 3.11](https://www.python.org/) or greater.

1. Install required dependencies using [Poetry](https://python-poetry.org/): `poetry install`
2. Rename `.env_example` to `.env`, then provide the environment variables.
3. Start Moniker: `python moniker.py`