import asyncio
import json

import aiohttp
import nest_asyncio

nest_asyncio.apply()


def map_search_url(address1):
    """
    With the block number and street name, get the full address of the hdb flat,
    including the postal code, geographical coordinates (lat/long)
    """
    # Do not need to change the URL
    return "https://developers.onemap.sg/commonapi/search?returnGeom=Y&getAddrDetails=Y&pageNum=1&searchVal=" + address1


async def async_get(url, session, response_formatter):
    try:
        async with session.get(url=url) as response:
            resp = await response.read()
            return {'url': url, 'body': response_formatter(resp), 'response_obj': response}
    except Exception as e:
        print("Unable to get url {} due to {}.".format(url, e.__class__))
        return None


async def async_gather(urls, response_formatter):
    async with aiohttp.ClientSession() as session:
        ret = await asyncio.gather(*[async_get(url, session, response_formatter) for url in urls])
        return ret


def map_data_formatter(response):
    # {'SEARCHVAL': 'ESSO ANG MO KIO AVENUE 8',
    #  'BLK_NO': '2225',
    #  'ROAD_NAME': 'ANG MO KIO AVENUE 8',
    #  'BUILDING': 'ESSO ANG MO KIO AVENUE 8',
    #  'ADDRESS': '2225 ANG MO KIO AVENUE 8 ESSO ANG MO KIO AVENUE 8 SINGAPORE 569810',
    #  'POSTAL': '569810',
    #  'X': '30139.113448292',
    #  'Y': '38291.9079437293',
    #  'LATITUDE': '1.36257285737839',
    #  'LONGITUDE': '103.852539960282',
    #  'LONGTITUDE': '103.852539960282'}
    try:
        data = json.loads(response)
    except ValueError:
        print('JSONDecodeError')
        return []
    res = data['results'][0]
    return [res['LONGITUDE'], res['LATITUDE']]


def parallelize_http(urls=[], data_formatter=json.loads):
    return asyncio.run(async_gather(urls, data_formatter))


# websites = """https://developers.onemap.sg/commonapi/search?returnGeom=Y&getAddrDetails=Y&pageNum=1&searchVal=ANG%20MO%20KIO%20AVE%208
# https://developers.onemap.sg/commonapi/search?returnGeom=Y&getAddrDetails=Y&pageNum=1&searchVal=ANG%20MO%20KIO%20AVE%208
# https://developers.onemap.sg/commonapi/search?returnGeom=Y&getAddrDetails=Y&pageNum=1&searchVal=ANG%20MO%20KIO%20AVE%208"""
#
# urls = websites.split('\n')
# url_dict = {}
# for url in urls:
#     url_dict['ANG MO KIO AVE 8'] = url
# results = parallelize_http(urls)
# for res in results:
#     search_val = res['response_obj'].url_obj.query['searchVal']
#     res['searchVal'] = search_val
# results
