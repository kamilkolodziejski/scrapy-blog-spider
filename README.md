# *BlogSpider* - example scrapy spider
### Spider for scraping blog https://blog.prokulski.science/

Spider scrapes informations about posts on blog:
* Post title
* Post date
* List of tags
* Number of tables
* Number of code lines

---
## Features
1. Rotates `User-Agent` header values
2. Auto-adjust or constant delay between HTTP requests
3. Disable all cookies in sent requests
4. Command-line argument for number of pages to download
5. Terminate automatically when response body is empty
6. Provides JSON-RPC API with actual state running spiders

---

## Installation

#### 1. Install scrapy
   
    conda install -c conda-forge scrapy
or

    pip install Scrapy

#### 2. Install extensions (optional)
user-agents

    pip install scrapy-useragents
json-rpc

    pip install scrapy-jsonrpc-api -i https://pypi.python.org/simple/

---
## Configuration

Configure settings in `settings.py`

> You can overwrite settings value directly in your Spider class assigning dict with settings to `self.custom_settings` property

### Disable cookies in requests

    COOKIES_ENABLED = False

### Set concurrent requests number

    CONCURRENT_REQUESTS = 5

### Rotate `User-Agent` header values

> `scrapy-useragents` extension may causes unwanted results  
> if `COOKIES_ENABLED` on `True`
> For more info check extension repository: https://github.com/scrapedia/scrapy-useragents

For enable `User-Agent` rotation set Downloader Middleware:
    
    DOWNLOADER_MIDDLEWARES = {
        'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
        'scrapy_useragents.downloadermiddlewares.useragents.UserAgentsMiddleware': 500,
    }

Define list of `User-Agent` values (use well-known values for best results):


    USER_AGENTS = [
        ('Mozilla/5.0 (X11; Linux x86_64) '
         'AppleWebKit/537.36 (KHTML, like Gecko) '
         'Chrome/57.0.2987.110 '
         'Safari/537.36'),  # chrome
        ('Mozilla/5.0 (X11; Linux x86_64) '
         'AppleWebKit/537.36 (KHTML, like Gecko) '
         'Chrome/61.0.3163.79 '
         'Safari/537.36'),  # chrome
        ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) '
         'Gecko/20100101 '
         'Firefox/55.0')  # firefox
    ]


### Constant delay between reqeusts

    DOWNLOAD_DELAY = 5

### Auto-adjustable delay (Auththrottle)

    UTOTHROTTLE_ENABLED = True


### JSON-RPC API for getting spiders state

    EXTENSIONS = {
        'scrapy_jsonrpc.webservice.WebService': 500,
    }
    
    JSONRPC_ENABLED = True
    JSONRPC_PORT = [6080]

Endpoint for access information about running spiders:

    http://localhost:6080/crawler

## Running spider

For start spider:

    scrapy crawl blog-spider

To run spider with number of pages to process:

    scrapy crawl blog-spider -a pages_number={x}