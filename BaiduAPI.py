import requests
from GCJ_Formatter import gcj02towgs84
import logging

class BaiduAPIs():
    def __init__(self, ak):
        self.ak = ak

    def BaiduQuery(self, address: str, city_code: str = '全国') -> tuple:
        """
        address convert lat and lng
        :param address: address
        :param city_code: 城市代码
        :return: a tuple, the first is the longitude, the second is the latitude.
        if query failed, return (-9999, -9999)
        """
        url = 'http://api.map.baidu.com/geocoding/v3/?'
        params = {
            "address": address,
            "city": city_code,
            "output": 'json',
            "ak": self.ak,
            "ret_coordtype": "gcj02ll"
        }
        response = requests.get(url, params=params)
        answer = response.json()
        if answer['status'] == 0:
            tmpList = answer['result']
            coordString = tmpList['location']
            coordList = [coordString['lng'], coordString['lat']]
            logging.info(f'baidu query {address} success.')
            return gcj02towgs84(float(coordList[0]), float(coordList[1]))
        else:
            logging.error(f'baidu query {address} failed')
            return (-9999, -9999)


    def reverse_geocoding(self, lng: float, lat: float) -> str:
        """
        lat and lng convert address
        :param lng: longitude
        :param lat: latitude
        :return: address
        :raise: Baidu Query Failed if the response return code is not 0.
        """
        url = 'http://api.map.baidu.com/reverse_geocoding/v3/?'
        params = {
            "location": str(lat) + ',' + str(lng),
            "output": 'json',
            "ak": self.ak,
            "coordtype": "wgs84ll",
        }
        response = requests.get(url, params=params)
        answer = response.json()
        if answer['status'] == 0:
            tmpList = answer['result']
            address = tmpList['formatted_address']
            return address
            # places_ll.append([address, lng, lat])
        else:
            raise Exception('Baidu Geo decode fail!')