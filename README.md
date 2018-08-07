# Bishop.

A telegram bot for ripping updates from MaplestoryM's facebook.

Because fuck proper rest API's and push notifications right, Nexon?

Written using Selenium to scrape the latest posts as I have no intention to seat through an app review process just to get updates from a game I enjoy playing.

You will need chromedriver, google-chrome-headless, mariaDB (or mySQL), python-telegram-bot, BeautifulSoup4, selenium and your own cfg.py.

This was written in 1 hour because I was asked to do it urgently. Forgive the shitty formatting.

```
BOT_TOKEN = "bot_token"
CHANNEL_ID = "channel_id"
SQL = {
    'host':'dbip',
    'user':'usr',
    'password':'pw',
    'db':'db_name',
    'charset':'utf8'
}
```