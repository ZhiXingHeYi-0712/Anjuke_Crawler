from typing import List

import pandas as pd
import geopandas as gpd
from BaiduAPI import BaiduAPIs

import shapely.geometry as geo

class DataFormatter():
    def __init__(self, data: List[List[str]]):
        '''
        Init this class to format the data.
        The data can be generated from Crawler.getPageRangeResult
        :param data: data
        '''
        self._data = data
        self._df = pd.DataFrame(self._data)
        self._df.rename(columns={0: '小区', 1: '总价', 2: '单价'}, inplace=True)

        # convert type to calculate mean data.
        self._df = self._df.astype({
            '总价': 'float64',
            '单价': 'int64'
        })

        self.baidu_apis = BaiduAPIs('WDMj5RHjZU41U9GhlbgaRziVrGKkCf7T')


    def _generateGeoDataFrame(self, df: pd.DataFrame, address_index: int = 0):
        '''
        generate pandas.DataFrame to geopandas.GeoDataFrame
        this method will use baidu api to geocoding the address to (longitude, latitude) (wgs84)
        :param df: dataframe
        :param address_index: the address column index. default value is 0
        :return: geopandas.GeoDataFrame
        '''
        geometry = []
        for location in df.iloc[:, address_index]:
            lnglat = self.baidu_apis.BaiduQuery(location)

            # if baidu query failed:
            if lnglat[0] == -9999:
                point = None
            else:
                point = geo.Point(self.baidu_apis.BaiduQuery(location))
            geometry.append(point)

        # the GeoSeries contains geometries. if the location query failed, it is replaced by None
        gs = gpd.GeoSeries(geometry)
        gdf = gpd.GeoDataFrame(data=df, geometry=gs)

        # convert to epsg:4326
        gdf.set_crs(epsg=4326, inplace=True)
        return gdf


    def _getMeanPriceDataframe(self) -> pd.DataFrame:
        '''
        get the mean price of each estate
        :return: mean price of each estate
        '''
        df_mean: pd.DataFrame = self._df.groupby(by='小区').mean()
        df_mean = df_mean.reset_index()
        return df_mean


    def getMeanPriceGeoDataFrame(self) -> gpd.GeoDataFrame:
        '''
        get the mean price of each estate with geometry
        :return: mean price of each estate with geometry
        '''
        df_mean = self._getMeanPriceDataframe()
        return self._generateGeoDataFrame(df_mean, 0)

