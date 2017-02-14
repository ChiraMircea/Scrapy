BOT_NAME = 'coches_scraper'

SPIDER_MODULES = ['coches_scraper.spiders']

NEWSPIDER_MODULE = 'coches_scraper.spiders'

ITEM_PIPELINES = {
    'coches_scraper.pipelines.DatabasePipeline': 100,
    'coches_scraper.pipelines.JSONPipeline': 200,
    'coches_scraper.pipelines.CSVPipeline': 300,
    'coches_scraper.pipelines.MailPipeline': 400

}

DOWNLOAD_HANDLERS = {
    's3': None
}
DOWNLOAD_DELAY = 1
DOWNLOAD_MAXSIZE = 0

LOG_ENABLED = True
LOG_FILE = 'logfile.txt'
LOG_LEVEL = 'CRITICAL'


ROBOTSTXT_OBEY = True
USER_AGENT = "Firefox"
