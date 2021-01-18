from scrapy import Spider, Request
from scrapy.exceptions import CloseSpider
import logging
import time
import os
import signal


class BlogSpider(Spider):
    name = 'blog-spider'

    def start_requests(self):
        base_url = 'https://blog.prokulski.science/index.php/wp-json/nv/v1/posts/page/'
        for i in range(5):
            url = f'{base_url}{i}'
            self.log(f'Create POST Request with url: {url}')
            time.sleep(5)
            yield Request(url=url, callback=self.parse, method='POST')

    def parse(self, response):
        self.log(f'Parse response with method parse() from url:{response.url}')
        if response.body == '\"\"':
            self.log(f'Stop ApiSpider beacause url "{response.request.url}" response is empty!!',
                     level=logging.ERROR)
            self.log(f'{response.body}', level=logging.ERROR)
            os.kill(os.getpid(), signal.SIGINT)
            raise CloseSpider('Empty response')

        for href in response.css('h2 > a::attr(href)').getall():
            url = href.replace('\\\"', '').replace('\\', '')
            self.log(f'Create GET Request with url: "{url}"')
            yield Request(url=url, callback=self.parse_post)

    def parse_post(self, response):
        self.log(f'Parse response with method parse_post() from url:{response.url}')
        post_name = response.url.replace("https://blog.prokulski.science/index.php/", "").replace("/", "_")[:-1]
        self.log(f"Extract fields [post_title, post_date, post_tags, " +
                 "post_tables_num, post_code_lines_num] from Post {post_name}")
        post_date = post_name[:10].replace("_", "-")
        post_title = post_name[11:]
        post_tags = response.css('.nv-tags-list > a::text').getall()
        post_tables_num = len(response.css('table.table.table-striped.table-hover.table-condensed.table-responsive')
                              .getall())
        post_code_lines_num = len(response.css('.crayon-code > .crayon-pre > .crayon-line').getall())
        self.log(f'Return data for post "{post_name}"')
        yield {
            'post_title': post_title,
            'post_date': post_date,
            'post_tags': post_tags,
            'post_tables_num': post_tables_num,
            'post_code_lines_num': post_code_lines_num
        }
