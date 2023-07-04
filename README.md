# Moniker

![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/EthanC/Moniker/ci.yml?branch=main) ![Docker Pulls](https://img.shields.io/docker/pulls/ethanchrisp/moniker?label=Docker%20Pulls) ![Docker Image Size (tag)](https://img.shields.io/docker/image-size/ethanchrisp/moniker/latest?label=Docker%20Image%20Size)

Moniker monitors usernames across the following platforms and reports availability via Discord.

-   [Cash App](https://cash.app/)
-   [GitHub](https://github.com/)
-   [Mastodon](https://mastodon.social/)
-   [Snapchat](https://www.snapchat.com/)
-   [Twitter](https://twitter.com/)
-   [Venmo](https://venmo.com/)
-   [YouTube](https://youtube.com/)

<p align="center">
    <img src="https://i.imgur.com/OzxHboR.png" draggable="false">
</p>

## Setup

Although not required, a [Discord Webhook](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks) is recommended for notifications.

Regardless of your chosen setup method, Moniker is intended for use with a task scheduler, such as [cron](https://crontab.guru/).

**Environment Variables:**

-   `LOG_LEVEL`: [Loguru](https://loguru.readthedocs.io/en/stable/api/logger.html) severity level to write to the console.
-   `LOG_DISCORD_WEBHOOK_URL`: [Discord Webhook](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks) URL to receive log events.
-   `LOG_DISCORD_WEBHOOK_LEVEL`: Minimum [Loguru](https://loguru.readthedocs.io/en/stable/api/logger.html) severity level to forward to Discord.
-   `CASHAPP_USERNAMES`: Comma-separated list of [Cash App](https://cash.app/) $Cashtags to monitor.
-   `GITHUB_USERNAMES`: Comma-separated list of [GitHub](https://github.com/) usernames to monitor.
-   `MASTODON_USERNAMES`: Comma-separated list of [Mastodon](https://mastodon.social/) usernames to monitor.
-   `SNAPCHAT_USERNAMES`: Comma-separated list of [Snapchat](https://www.snapchat.com/) usernames to monitor.
-   `TWITTER_USERNAMES`: Comma-separated list of [Twitter](https://twitter.com/) usernames to monitor.
-   `GITHUB_USERNAMES`: Comma-separated list of [Venmo](https://venmo.com/) usernames to monitor.
-   `YOUTUBE_USERNAMES`: Comma-separated list of [YouTube](https://youtube.com/) usernames to monitor.
-   `DISCORD_WEBHOOK_URL`: [Discord Webhook](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks) URL to receive available username notifications.

### Docker (Recommended)

Modify the following `docker-compose.yml` example file, then run `docker compose up`.

```yml
version: "3"
services:
  moniker:
    container_name: moniker
    image: ethanchrisp/moniker:latest
    environment:
      LOG_LEVEL: INFO
      LOG_DISCORD_WEBHOOK_URL: https://discord.com/api/webhooks/YYYYYYYY/YYYYYYYY
      LOG_DISCORD_WEBHOOK_LEVEL: WARNING
      CASHAPP_USERNAMES: XXXXXXXX,YYYYYYYY,ZZZZZZZZ
      GITHUB_USERNAMES: XXXXXXXX,YYYYYYYY,ZZZZZZZZ
      MASTODON_USERNAMES: XXXXXXXX,YYYYYYYY,ZZZZZZZZ
      SNAPCHAT_USERNAMES: XXXXXXXX,YYYYYYYY,ZZZZZZZZ
      TWITTER_USERNAMES: XXXXXXXX,YYYYYYYY,ZZZZZZZZ
      VENMO_USERNAMES: XXXXXXXX,YYYYYYYY,ZZZZZZZZ
      YOUTUBE_USERNAMES: XXXXXXXX,YYYYYYYY,ZZZZZZZZ
      DISCORD_WEBHOOK_URL: https://discord.com/api/webhooks/XXXXXXXX/XXXXXXXX
```

### Standalone

Moniker is built for [Python 3.11](https://www.python.org/) or greater.

1. Install required dependencies using [Poetry](https://python-poetry.org/): `poetry install`
2. Rename `.env.example` to `.env`, then provide the environment variables.
3. Start Moniker: `python moniker.py`
