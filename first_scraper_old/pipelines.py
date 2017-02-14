import sqlite3
import json
import csv
import smtplib
from email.mime.text import MIMEText


class DatabasePipeline(object):

    def open_spider(self, spider):
        self.conn = sqlite3.connect('data.db')
        self.c = self.conn.cursor()
        self.c.execute('CREATE TABLE IF NOT EXISTS data(area TEXT, color TEXT, description TEXT, doors TEXT, \
        extra_equipment TEXT, fuel TEXT, horse_power TEXT, image_urls TEXT, insurance TEXT, km TEXT, price TEXT, \
        seats TEXT, title TEXT, transmission TEXT, year TEXT)')

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):

        data = dict(item)

        for key in data.keys():
            data[key] = ''.join([i if ord(i) < 128 and i != '"' else '' for i in data[key][0]])

        sorted_keys = sorted(list(data.keys()))
        values = []
        for key in sorted_keys:
            values.append(data[key])

        raw_data = '", "'.join(values)
        query = 'INSERT INTO data VALUES ("' + raw_data + '")'

        self.c.execute(query)
        self.conn.commit()

        return item


class JSONPipeline(object):

    def open_spider(self, spider):
        self.file = open('data.json', 'wb')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):

        data = dict(item)

        line = json.dumps(data) + "\n"
        self.file.write(line)

        return item


class CSVPipeline(object):

    def open_spider(self, spider):
        self.file = open('data.csv', 'wb')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        data = dict(item)

        writer = csv.writer(self.file)
        writer.writerow(list(data.values()))

        return item


class MailPipeline(object):

    def close_spider(self, spider):

        with open('logfile.txt', 'r') as log:
            report = MIMEText(log.read())

        report['Subject'] = "cars spider report"
        report['From'] = 'scrapytestmail@gmail.com'
        report['To'] = 'chira.mircea.mc@gmail.com'

        mail = smtplib.SMTP('smtp.gmail.com', 587)
        mail.ehlo()
        mail.starttls()

        mail.login('scrapytestmail@gmail.com', 'scrapytestmail123')
        mail.sendmail('scrapytestmail@gmail.com', 'chira.mircea.mc@gmail.com', report.as_string())

        mail.close()

    def process_item(self, item, spider):

        return item
