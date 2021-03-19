from DataFormatter import DataFormatter
from Crawler import Crawler
import geopandas as gpd
import logging
logging.basicConfig(level=logging.INFO)

c = Crawler('https://shenzhen.anjuke.com/sale/p{page}/?from=esf_list', city='深圳')
p = c.getPageRangeResult(1, 50)
formatter = DataFormatter(p)
gdf = formatter.getMeanPriceGeoDataFrame()
gdf.to_file('shenzhen_house.shp', encoding='utf-8')


