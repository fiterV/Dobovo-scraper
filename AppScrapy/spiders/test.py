import scrapy
from scrapy import signals
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.xlib.pydispatch import dispatcher

import urllib.parse
from AppScrapy.items import AppscrapyItem
from termcolor import colored
from selenium import webdriver
from .utils import changeDateFormat
from time import sleep


DEBUG = True

def Debug():
    for i in range(10):
        print(colored(
            '-----------------------------------------------------------------------------------------------> Look over here, boy',
            color='red'))


class MySpider(BaseSpider):
    name='betty'
    allowed_domains = ['dobovo.com']
    start_urls = ['http://www.dobovo.com/ua/%D0%BA%D0%B8%D1%97%D0%B2-%D0%BA%D0%B2%D0%B0%D1%80%D1%82%D0%B8%D1%80%D0%B8-%D0%BF%D0%BE%D0%B4%D0%BE%D0%B1%D0%BE%D0%B2%D0%BE.html?page=1']

    def __init__(self):
        self.driver = webdriver.PhantomJS()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        self.driver.quit()

    def parseAppartment(self, response):
        #Debug()
        resp = self.driver.get(response.url)
        sel = Selector(text=self.driver.page_source)
        app = AppscrapyItem()
        app['url']=response.url
        app['name'] = sel.xpath("//h1[@id='dbv_js_title']/text()").extract()[0]
        app['address'] = sel.xpath("//div[@class='address']/text()").extract()[0].lstrip().rstrip()
        livingInfo = sel.xpath("//ul[@class='require']/li/span/text()").extract()
        app['housingArea'] = livingInfo[0]
        app['minAmountOfNights'] = livingInfo[1]
        app['floor'] = livingInfo[2]
        app['berthCount'] = livingInfo[3]
        app['bathroomCount'] = livingInfo[4]
        app['owner'] = sel.xpath("//div[@class='owner__title']/span[1]/text()").extract()[0]
        try:
            app['personalSpeaks'] = sel.xpath("//div[@class='owner__title']/div/text()").extract()[1]
        except:
            app['personalSpeaks'] = ''

        addAdvantages = sel.xpath("//span[@class='attr__item']/text()").extract()
        app['additionalAdvantages'] = ', '.join(addAdvantages)

        app['minSum'] = sel.xpath("//span[@class='dbv_price price-detail__val dbv_apt_price_current dbv_coloured']//span[@class='dbv_val']/text()").extract()[0]
        app['freeDates']=[]
        freeDates = sel.xpath("//div[starts-with(@class,'cell clickable')]/@date").extract()

        for date in freeDates:
            block = sel.xpath("//div[starts-with(@class, 'cell clickable') and @date='{}']".format(date)).extract()
            currency = sel.xpath(
                "//div[starts-with(@class, 'cell clickable') and @date='{}']//span[@class='dbv_cur']/text()".format(
                    date)).extract()[0]
            price = sel.xpath(
                "//div[starts-with(@class, 'cell clickable') and @date='{}']//span[@class='dbv_val']/text()".format(
                    date)).extract()[0]
            text = block[0]
            # print('Date = {} price = {}{}'.format(changeDateFormat(date), price, currency))
            app['freeDates'].append({
                'date': changeDateFormat(date),
                'price': price + currency,
            })

        #get overall mark for the appartment
        try:
            app['mark']=sel.xpath("//a[@class='flat-mark js-to-comments']/strong/text()").extract()[0]
        except:
            app['mark']=''


        if DEBUG:
            Debug()
            # Suspicious code goes here
            Debug()

        #normalize all the results,remove all these spaces and \n's
        for key in app:
            if (type(app[key]) is str):
                app[key]= app[key].lstrip().rstrip()

        return app



    def parse(self, response):
        sel = Selector(response)
        appartments = sel.xpath("//div[@class='item__main']/a/@href").extract()
        if DEBUG:
            print(appartments)
        for link in appartments:
            print('Were going to scrapy this: {}'.format(link))
            yield scrapy.Request(link, callback=self.parseAppartment)

        nextPage = sel.xpath("//div[@class='pages']/a[last()]/@href").extract()[0]
        nextPage = urllib.parse.urljoin(response.url, nextPage)
        if (nextPage!=response.url):
            nextPage=response.url[response.url.find('page')+5:]
            before = response.url[:response.url.find('page')+5]
            nextPage=int(nextPage)+1
            nextPage = before+str(nextPage)
            yield scrapy.Request(nextPage)