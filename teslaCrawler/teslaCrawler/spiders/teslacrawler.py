import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrapy.http import HtmlResponse
from scrapy_selenium import SeleniumRequest
from urllib.parse import urlparse
import json
from teslaCrawler.items import TeslacrawlerItem
from .MongoDB import MongoDB as db

lang_country_url_pattern = r'https://www\.tesla\.com/[a-z]{2}_[A-Z]{2}/'
CONNECTION_STRING = "mongodb+srv://irproject991:12312331231233@cluster0.x0jpsot.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DATABASE_NAME = "IR-2024"
COLLECTION_NAME = "crawler-data"

class TeslaSpider(scrapy.Spider):
    name = "tesla"
    visited_url = set()
    allowed_domains = ["tesla.com", "shop.tesla.com"]
    mongodb = db(CONNECTION_STRING, DATABASE_NAME, COLLECTION_NAME)

    def start_requests(self):
        urls = [
            # 'https://www.tesla.com/',
            'https://www.tesla.com/fr_CA/model3/design#overview'
        ]
        for url in urls:
            yield SeleniumRequest(url=url,wait_time=10 ,callback=self.parse)

    def parse(self, response):
        print("Inside Parse")
        # Skip any URL that is tesla.com/<lang>_<country>
        if (self.regionalURLRegexCheck(response.url)):
            return
        # Skip if is not allowed domains
        if (self.isAllowedURLcheck(response) is False):
            return
        # Skip if is a visited URL
        if (response.url in self.visited_url):
            return
        
        self.visited_url.add(response.url)

        rendered_html = response.text
        item = TeslacrawlerItem()
        item['full_html'] = rendered_html
        item['main_content'] = self.getMainContent(response)
        item['title'] = self.getTitleByOgTitle(response)
        item['description'] = self.getDescByOgDesc(response)
        item['keywords'] = self.getKeywordsByKeywords(response)
        item['url'] = response.url
        item_dict = dict(item)

        print(item)
        # Uncomment this if you want to insert into MongoDB
        # self.mongodb.save_json(item_dict)

        linksFound = LinkExtractor().extract_links(response)

        for link in linksFound:
            self.logger.info(f"Found link: {link.url}")
            yield SeleniumRequest(url=link.url, wait_time=10, callback=self.parse)


    def regionalURLRegexCheck(self, url):
        pattern = re.compile(lang_country_url_pattern)
        match = pattern.search(url)
        if match:
            print(f"{url} is not allowed, is a lang Url")
            return True
        else:
            return False
    
    def isAllowedURLcheck(self, response):
        parsed_url = urlparse(response.url)
        domain = parsed_url.netloc

        for allowed_domain in self.allowed_domains:
            if domain.endswith(allowed_domain):
                print(f"{response.url} is allowed")
                return True
        
        self.logger.info(f"{response.url} is not an allowed Url")
        return False

    
    def getMainContent(self, response):
        try:
            body_content = response.xpath('//body//*[not(self::script or self::style)]/text()').getall()
            body_text = '. '.join(text.strip() for text in body_content if text.strip()).strip().lower()
            return body_text
        except:
            return None

    def getTitleByOgTitle(self, response):
        og_title = response.xpath('//meta[@property="og:title"]/@content').get()
        return og_title
    
    def getDescByOgDesc(self, response):
        desc = response.xpath('//meta[@property="og:description"]/@content').get()
        return desc
    
    def getKeywordsByKeywords(self, response):
        keywords = response.xpath('//meta[@name="keywords"]/@content').get()
        return keywords
    def isTextContent(self, response):
        meta_tag = response.xpath('//meta[@http-equiv="Content-Type"]/@content').get()
        if meta_tag and 'text/html' in meta_tag:
            return True
        print(f"{response.url} is not html/text.")
        return False