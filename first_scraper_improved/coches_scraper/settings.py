BOT_NAME = 'coches_scraper'

SPIDER_MODULES = ['coches_scraper.spiders']

NEWSPIDER_MODULE = 'coches_scraper.spiders'

DOWNLOAD_HANDLERS = {
    's3': None
}
DOWNLOAD_DELAY = 0
DOWNLOAD_MAXSIZE = 0

LOG_ENABLED = True
#LOG_FILE = 'logfile.txt'
LOG_LEVEL = 'ERROR'

FEED_URI = '%(name)s@%(time)s'
FEED_FORMAT = 'csv'
FEED_EXPORT_FIELDS = ["title", "price", "year"]

ROBOTSTXT_OBEY = True
USER_AGENT = "Firefox"
