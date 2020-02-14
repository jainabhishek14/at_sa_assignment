import scrapy, json, os, random, re
from slugify import slugify

from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

path = "articles"
user_agent_list = [
    #Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    #Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]
debug_mode = False
origin = 'https://seekingalpha.com'
maxCount = "1000"
headers = {
    'Content-Type': '*/*',
    'Origin': origin,
    'Referrer': origin
}

class SaSpider(scrapy.Spider):

    name = 'sa'
    allowed_domains = ['seekingalpha.com']
    custom_settings = {
            # 'LOG_LEVEL': 'CRITICAL', # 'DEBUG'
            # 'LOG_ENABLED': False,
            'DOWNLOAD_DELAY': 4 # 0.25 == 250 ms of delay, 1 == 1000ms of delay, etc.
    }

    def start_requests(self):
        urls = [ "https://r4rrlsfs4a.execute-api.us-west-2.amazonaws.com/production/search?q=(and+%27"+self.companyName+"%27+(and+content_type:%27transcripts%27)+(or+primary_symbols:%27%27))&q.parser=structured&sort=rank1+desc&size=10&q.options=%7B%22fields%22%3A%5B%22author%22%2C%22author_url%22%2C%22content%5E1%22%2C%22content_type%22%2C%22image_url%22%2C%22primary_symbols%22%2C%22secondary_symbols%22%2C%22summary%22%2C%22tags%22%2C%22title%5E3%22%2C%22uri%22%5D%7D&highlight.title=%7Bpre_tag%3A%27%3Cstrong%3E%27%2Cpost_tag%3A%27%3C%3C%3C%3Cstrong%3E%27%7D&highlight.summary=%7Bpre_tag%3A%27%3Cstrong%3E%27%2Cpost_tag%3A%27%3C%3C%3C%3Cstrong%3E%27%7D&highlight.content=%7Bpre_tag%3A%27%3Cstrong%3E%27%2Cpost_tag%3A%27%3C%3C%3C%3Cstrong%3E%27%7D&highlight.author=%7Bpre_tag%3A%27%3Cstrong%3E%27%2Cpost_tag%3A%27%3C%3C%3C%3Cstrong%3E%27%7D&highlight.primary_symbols=%7Bpre_tag%3A%27%3Cstrong%3E%27%2Cpost_tag%3A%27%3C%3C%3C%3Cstrong%3E%27%7D" ]
        user_agent = random.choice(user_agent_list)
        headers['User-Agent'] = user_agent
        for url in urls:
            yield scrapy.http.JsonRequest(url=url, callback=self.parse, errback=self.errback_httpbin, headers=headers)


    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 responses
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)

    def parse(self, data):
        self.logger.info("Parse Sessions")
        decodedResponse = json.loads(data.body_as_unicode())
        # Latest Article = first element in the response
        yield self.get_article(decodedResponse["hits"]["hit"][0])

    def get_article(self, data):
        self.logger.info("Fetching Article")
        url = data["fields"]["uri"]
        return scrapy.http.Request(url=origin + url, callback=self.save_contents, errback=self.errback_httpbin, headers=headers)

    # SAVE CONTENTS TO AN HTML FILE
    def save_contents(self, response):
        data = response.css("div#content-rail article #a-body")
        data = data.extract()
        if not os.path.exists(path):
            os.makedirs(path)

        filename = self.companyName + ".txt"
        with open(os.path.join(path,filename), 'w') as f:
            cleanText = self.cleanhtml(data[0])
            f.write(cleanText)
            f.close()

    def cleanhtml(self, raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext