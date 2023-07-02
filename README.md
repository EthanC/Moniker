# Moniker

![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/EthanC/Moniker/ci.yml?branch=main) ![Docker Pulls](https://img.shields.io/docker/pulls/ethanchrisp/moniker?label=Docker%20Pulls) ![Docker Image Size (tag)](https://img.shields.io/docker/image-size/ethanchrisp/moniker/latest?label=Docker%20Image%20Size)

Moniker monitors usernames across the following platforms and reports availability via Discord.

-   [GitHub](https://github.com/)
-   [Mastodon](https://mastodon.social/)
-   [Snapchat](https://www.snapchat.com/)
-   [Twitter](https://twitter.com/)

<p align="center">
    <img src="https://i.imgur.com/OzxHboR.png" draggable="false">
</p>

## Setup

Although not required, a [Discord Webhook](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks) is recommended for notifications.

Regardless of your chosen setup method, Moniker is intended for use with a task scheduler, such as [cron](https://crontab.guru/).

**Environment Variables:**

-   `GITHUB_USERNAMES`: Comma-separated list of GitHub usernames to monitor.
-   `MASTODON_USERNAMES`: Comma-separated list of Mastodon usernames to monitor.
-   `SNAPCHAT_USERNAMES`: Comma-separated list of Snapchat usernames to monitor.
-   `TWITTER_ACCESS_TOKEN` (Required for Twitter): [Twitter API](https://developer.twitter.com/en/docs/twitter-api) Access Token.
-   `TWITTER_ACCESS_TOKEN_SECRET` (Required for Twitter): [Twitter API](https://developer.twitter.com/en/docs/twitter-api) Access Token Secret.
-   `TWITTER_API_KEY` (Required for Twitter): [Twitter API](https://developer.twitter.com/en/docs/twitter-api) Key.
-   `TWITTER_API_KEY_SECRET` (Required for Twitter): [Twitter API](https://developer.twitter.com/en/docs/twitter-api) Key Secret.
-   `TWITTER_USERNAMES`: Comma-separated list of Twitter usernames to monitor.
-   `DISCORD_NOTIFY_WEBHOOK`: [Discord Webhook](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks) URL to receive available username notifications.
-   `DISCORD_LOG_WEBHOOK`: [Discord Webhook](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks) URL to receive log events.
-   `DISCORD_LOG_LEVEL`: Minimum [Loguru](https://loguru.readthedocs.io/en/stable/api/logger.html) severity level to forward to Discord.

### Docker (Recommended)

Modify the following `docker-compose.yml` example file, then run `docker compose up`.

```yml
version: "3"
services:
  moniker:
    container_name: moniker
    image: ethanchrisp/moniker:latest
    environment:
      GITHUB_USERNAMES: XXXXXXXX,YYYYYYYY,ZZZZZZZZ
      MASTODON_USERNAMES: XXXXXXXX,YYYYYYYY,ZZZZZZZZ
      SNAPCHAT_USERNAMES: XXXXXXXX,YYYYYYYY,ZZZZZZZZ
      TWITTER_ACCESS_TOKEN: XXXXXXXX
      TWITTER_ACCESS_TOKEN_SECRET: XXXXXXXX
      TWITTER_API_KEY: XXXXXXXX
      TWITTER_API_KEY_SECRET: XXXXXXXX
      TWITTER_USERNAMES: XXXXXXXX,YYYYYYYY,ZZZZZZZZ
      DISCORD_NOTIFY_WEBHOOK: https://discord.com/api/webhooks/XXXXXXXX/XXXXXXXX
      DISCORD_LOG_WEBHOOK: https://discord.com/api/webhooks/XXXXXXXX/XXXXXXXX
      DISCORD_LOG_LEVEL: WARNING
```

### Standalone

Moniker is built for [Python 3.11](https://www.python.org/) or greater.

1. Install required dependencies using [Poetry](https://python-poetry.org/): `poetry install`
2. Rename `.env.example` to `.env`, then provide the environment variables.
3. Start Moniker: `python moniker.py`
