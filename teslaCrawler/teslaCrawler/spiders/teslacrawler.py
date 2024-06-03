import scrapy
from scrapy_splash import SplashRequest
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
from urllib.parse import urlencode, parse_qs
from scrapy.http import HtmlResponse  # Import HtmlResponse



lang_country_url_pattern = r'https://www\.tesla\.com/[a-z]{2}_[a-z]{2}.*'

# to pause and resume crawls -> run `scrapy crawl somespider -s JOBDIR=crawls/somespider-1``
class TeslaSpider(CrawlSpider):
    name = "tesla"
    visited_urls = set()
    allowed_domains = ["tesla.com", "shop.tesla.com", 'localhost']
    start_urls = [
        'https://www.tesla.com/'
    ]

    # deny any urls that is www.tesla.com/<language>_<country> to prevent duplicate
    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        print(f"{response.url} processing")

         # Check if the URL matches the pattern
        if self.regionalURLRegexCheck(response.url):
            print(f"{response.url} skipped due to regional URL pattern match!")
            return

        self.visited_urls.add(response.url)
        print(self.visited_urls)
        page = response.url.split("/")[-2]
        title = self.getTitle(response);
        keywords = self.getKeywords(response)
        url = response.url
        desc = self.getDesc(response)
        main_content = self.getContentsByMainTag(response)
    
        # filename = '/Users/lionelchew/Desktop/python-web-crawler/teslaCrawler/teslaCrawler/data/%s.html' % page
        # with open(filename, 'wb') as f:
        #     # f.write(response.body)
        #     f.write(keywords)
        #     f.write(title)
        # self.log('Saved file %s' % filename)
    
    def regionalURLRegexCheck(self, url):
        return re.match(lang_country_url_pattern, url)

    def getTitle(self, response):
        og_title = response.xpath('//meta[@property="og:title"]/@content').get()
        print(og_title)
        return og_title
    
    def getKeywords(self, response):
        keywords = response.xpath('//meta[@name="keywords"]/@content').get()
        print(keywords)
        return keywords
    
    def getDesc(self, response):
        desc= response.xpath('//meta[@name="description"]/@content').get()
        return desc
    
    def getContentsByMainTag(self, response):
        main_content = response.xpath('//main[@id="main-content"]').get()
        if main_content:
            print(main_content)
        else:
            print("main_content, NONO")
        return main_content


    
