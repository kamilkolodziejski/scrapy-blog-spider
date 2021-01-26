# -*- coding: utf-8 -*-

import logging
from scrapy import Spider, Request
from scrapy.exceptions import CloseSpider


class BlogSpider(Spider):
    name = 'blog-spider'

    custom_settings = {
        'USER_AGENTS': [(
            # Samsung Galaxy S9
            'Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/62.0.3202.84 Mobile Safari/537.36'),
            # Samsung Galaxy S7
            ('Mozilla/5.0 (Linux; Android 7.0; SM-G930VC Build/NRD90M; wv) '
             'AppleWebKit/537.36 (KHTML, like Gecko) '
             'Version/4.0 Chrome/58.0.3029.83 Mobile Safari/537.36'),
            # Apple IPhone XR (Safari)
            ('Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) '
             'AppleWebKit/605.1.15 (KHTML, like Gecko) '
             'Version/12.0 Mobile/15E148 Safari/604.1')]
    }

    def __init__(self, *args, pages_number=None, **kwargs):
        Spider.__init__(self, *args, **kwargs)
        self.page_number_to_crawl = pages_number

    def start_requests(self):
        base_url = 'https://blog.prokulski.science/index.php/wp-json/nv/v1/posts/page/'
        if self.page_number_to_crawl is None:
            self.page_number_to_crawl = 9999
        for i in range(int(self.page_number_to_crawl)):
            url = f'{base_url}{i}'
            self.log(f'Create POST Request with url: {url}')
            yield Request(url=url, callback=self.parse, method='POST')

    def parse(self, response, **kwargs):
        self.log(f'Parse response with method parse() from url:{response.url}')
        self.log(f'User-Agent: {response.request.headers["User-Agent"]}')
        if response.body == b'\"\"':
            self.log(f'Stop BlogSpider beacause url "{response.request.url}" response is empty.',
                     level=logging.ERROR)
            raise CloseSpider('Empty response')
        for href in response.css('h2 > a::attr(href)').getall():
            url = href.replace('\\\"', '').replace('\\', '')
            self.log(f'Create GET Request with url: "{url}"')
            yield Request(url=url, callback=self.parse_post_page)

    def parse_post_page(self, response):
        self.log(f'Parse response with method parse_post() from url:{response.url}')
        post_name = response.url.replace(response.request.url, "").replace("/", "_")[:-1]
        self.log('Extract fields [post_title, post_date, post_tags, ' +
                 f'"post_tables_num, post_code_lines_num] from Post {post_name}')

        post_date = post_name[:10].replace("_", "-")
        post_title = post_name[11:]
        post_tags = response.css('.nv-tags-list > a::text').getall()
        post_tables_num = len(response.css('table'
                                           '.table.table-striped.table-hover'
                                           '.table-condensed.table-responsive'
                                           ).getall())
        post_code_lines_num = len(response.css('.crayon-code > .crayon-pre > .crayon-line'
                                               ).getall())

        self.log(f'Return data for post "{post_name}"')
        yield {
            'post_title': post_title,
            'post_date': post_date,
            'post_tags': post_tags,
            'post_tables_num': post_tables_num,
            'post_code_lines_num': post_code_lines_num
        }
