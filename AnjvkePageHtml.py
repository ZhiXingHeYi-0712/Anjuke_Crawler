from typing import List, Tuple

from lxml import etree
import logging

class AnjvkePageHtml():
    def __init__(self, html: bytes):
        '''
        :param html: response.content
        '''
        self._html = html.decode()
        self.tree = etree.HTML(self._html)

    def _findXpath(self, xpath: str) -> list:
        '''
        :param xpath: xpath string
        :return: element
        '''
        return self.tree.xpath(xpath)

    def _getXpathsList(self, number: int) -> Tuple[str, str, str]:
        a =     '/html/body/div/div/div/section/section[3]/section[1]/section[2]/div[1]/a/div[2]/div[1]/section/div[2]/p[1]/text()'
        base = f'/html/body/div/div/div/section/section[3]/section[1]/section[2]/div[{number + 1}]/'
        return (base + 'a/div[2]/div[1]/section/div[2]/p[1]/text()',
                base + 'a/div[2]/div[2]/p[1]/span[1]/text()',
                base + 'a/div[2]/div[2]/p[2]/text()')


    def _getResult(self, xpath_list: Tuple[str, str, str]) -> list:
        def findInfoXpath(xpath: str) -> str:
            result: list = self._findXpath(xpath)
            if len(result) > 1:
                raise Exception('Too many result!')
            if len(result) == 0:
                return findInfoXpath(f'{xpath[:-9]}2{xpath[-8:]}')
            return result[0]
        house = list(map(findInfoXpath, xpath_list))
        house[2] = house[2].replace('元/㎡', '')
        return house


    def _getPageLength(self) -> int:
        length = len(self._findXpath('/html/body/div/div/div/section/section[3]/section[1]/section[2]/div'))
        return length

    def getPageResult(self) -> List[List[str]]:
        '''
        :return: result. [[address, price, per_price], ...]
        '''
        result = []
        for i in range(self._getPageLength()):
            xpath_list = self._getXpathsList(i)
            result.append(self._getResult(xpath_list))
        logging.info(f'anjuke page result success')
        return result

