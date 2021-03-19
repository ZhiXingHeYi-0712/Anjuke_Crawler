import logging
from typing import List

import requests
from AnjvkePageHtml import AnjvkePageHtml

class Crawler():
    """
    This class used to crawl data from anjuke.com
    """
    def __init__(self, base_url: str = 'https://zh.anjuke.com/sale/p{page}/?from=navigation',
                 city: str = '全国'):
        '''
        :param base_url: the base url must contains a {page}.
        default value is 'https://zh.anjuke.com/sale/p{page}/?from=navigation'.
        the {page} will be replaces by str.format(page=)
        :param city: city name.
        '''
        self._base_url = base_url
        self._city = city

    def _getPageUrl(self, page: int) -> str:
        '''
        get page url. based on self._base_url
        :param page: page number.
        :return: page url
        '''
        return self._base_url.format(page = page)

    def _getPageHtml(self, page_url: str) -> AnjvkePageHtml:
        '''

        :param page_url: page url. from self._getPageUrl()
        :return: AnjvkePageHtml Object
        '''
        headers = {  # 由于安居客网站的反爬虫，这里必须要设置header
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Referer': 'https: // wuhan.anjuke.com / sale /?from=navigation',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
        }
        content = requests.get(page_url, headers = headers, timeout = 60).content
        return AnjvkePageHtml(content)

    def _getPageRangeHtmls(self, start_page: int, end_page: int):
        for i in range(start_page, end_page):
            page_url = self._getPageUrl(i)
            html = self._getPageHtml(page_url)
            logging.info(f'get page {i} html success')
            yield html

    def getPageRangeResult(self, start_page: int, end_page: int) -> List[List[str]]:
        '''
        获取结果列表
        :param start_page: 开始页码
        :param end_page: 结束页码，不包含该页
        :return: 含有子列表的列表。每个子列表长度为3，[小区名, 总价, 单价]
        '''
        htmls = list(self._getPageRangeHtmls(start_page, end_page))

        result = []
        for html in htmls:
            result.extend(html.getPageResult())

        logging.info('get page ranges success')
        return result

