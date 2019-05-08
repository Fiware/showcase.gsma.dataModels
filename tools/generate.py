#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
    This program parses xml provided by http://www.ine.es/en/welcome.shtml
    and prepares the initial data for weather harvesters.

    It collects:
      - weather stations (weather observed id for municipality)
      - municipalities (weather forecast id for municipality)
      - provinces (for future purposes)
      - communities (for future purposes)
"""

import sys
import json
from aiohttp import ClientSession, client_exceptions
from bs4 import BeautifulSoup
from asyncio import Semaphore, ensure_future, gather, run
import xlrd

file_config = 'stations.json'
file_init = 'info.xlsx'
limit = 4
result = dict()
result['communities'] = dict()
result['municipalities'] = dict()
result['provinces'] = dict()
result['stations'] = dict()
url_municipalities_template = 'http://www.aemet.es/es/eltiempo/prediccion/municipios?p={}&w=t'
url_stations_template = ("http://www.aemet.es/es/eltiempo/observacion/ultimosdatos?k={}"
                         "&l={}&w=0&datos=det&x=h24&f=temperatura")
url_stations_list_template = 'http://www.aemet.es/es/eltiempo/observacion/ultimosdatos?k={}&w=0'


async def stations_list():
    sem = Semaphore(limit)
    tasks = list()

    async with ClientSession() as session:
        for c in result['communities']:
            task = ensure_future(stations_list_bounded(sem, c, session))
            tasks.append(task)

        response = await gather(*tasks)

    return [j for i in response for j in i]


async def stations_list_bounded(sem, community, session):
    async with sem:
        return await stations_list_one(community, session)


async def stations_list_one(community, session):
    # get init list of stations by communities

    res = list()
    content = None
    url = url_stations_list_template.format(result['communities'][community]['tag'])
    try:
        async with session.get(url) as response:
            content = await response.read()
    except client_exceptions.ClientOSError:
        print(url)

    soup = BeautifulSoup(content, features="lxml")
    source = soup.findAll('div', attrs={'class':'contenedor_popup width250px'})
    for c in source:
        res.append({'station': c.attrs['id'].split('_')[1], 'community': str(community)})

    return res


async def stations(list_stations):
    sem = Semaphore(limit)
    tasks = list()

    async with ClientSession() as session:
        for s in list_stations:
            task = ensure_future(stations_bounded(sem, session, s['station'], s['community']))
            tasks.append(task)

        response = await gather(*tasks)

    return response


async def stations_bounded(sem, session, station, community):
    async with sem:
        return await stations_one(session, station, community)


async def stations_one(session, station, community):
    # get init list of stations

    res = dict()
    content = None
    res['id'] = station

    url = url_stations_template.format(result['communities'][community]['tag'], station)

    try:
        async with session.get(url) as response:
            content = await response.read()
    except client_exceptions.ClientOSError:
        print(url)

    soup = BeautifulSoup(content, features="lxml")

    res['name'] = soup.find('h2', attrs={'class': 'titulo'}).text.split('.')[1].lstrip()

    source = soup.find('span', attrs={'class': 'geo'})
    res['latitude'] = source.find('abbr', attrs={'class': 'latitude'}).attrs['title']
    res['longitude'] = source.find('abbr', attrs={'class': 'longitude'}).attrs['title']

    st = True

    try:
        source = soup.findAll('a', attrs={'class': 'enlace_web'})[1].attrs['href']
    except IndexError:
        st = False

    if st:
        res['municipality'] = source.rsplit('id', 1)[1]
    else:
        res['community'] = str(community)

    return res


async def municipalities():
    sem = Semaphore(limit)
    tasks = list()

    async with ClientSession() as session:
        for p in result['provinces']:
            task = ensure_future(municipalities_bounded(sem, p, session))
            tasks.append(task)

        response = await gather(*tasks)

    return [j for i in response for j in i]


async def municipalities_bounded(sem, province, session):
    async with sem:
        return await municipalities_one(province, session)


async def municipalities_one(province, session):
    # get init list of municipalities and forecast links

    res = list()
    url = url_municipalities_template.format(result['provinces'][province]['tag'])
    async with session.get(url) as response:
        content = await response.read()

    soup = BeautifulSoup(content, features="lxml")
    source = soup.findAll('div', attrs={'class': 'contenedor_central'})
    source = source[1].find_all('option')
    for option in source:
        link = option['value']
        if link:
            unit = dict()
            unit['name'] = option.text
            unit['province'] = province
            fid = link.rsplit('id', 1)[1]
            unit['id'] = fid
            res.append(unit)
    return res


if __name__ == '__main__':

    result['community_type'] = dict()
    result['community_type']['1'] = dict()
    result['community_type']['1']['name'] = 'community'
    result['community_type']['2'] = dict()
    result['community_type']['2']['name'] = 'city'

    result['province_type'] = dict()
    result['province_type']['1'] = dict()
    result['province_type']['1']['name'] = 'municipality'
    result['province_type']['2'] = dict()
    result['province_type']['2']['name'] = 'council'
    result['province_type']['3'] = dict()
    result['province_type']['3']['name'] = 'city'

    book = xlrd.open_workbook(file_init)

    # get init data about communities
    sheet = book.sheet_by_index(1)
    for row in range(1, sheet.nrows):
        result['communities'][str(row)] = dict()
        result['communities'][str(row)]['name'] = sheet.cell_value(row, 0)
        result['communities'][str(row)]['type'] = sheet.cell_value(row, 1)
        result['communities'][str(row)]['timezone'] = sheet.cell_value(row, 2)
        result['communities'][str(row)]['tag'] = sheet.cell_value(row, 3)
        check = False

        for el in result['community_type']:
            if result['community_type'][el]['name'] == result['communities'][str(row)]['type']:
                result['communities'][str(row)]['type'] = el
                check = True
        if not check:
            print('Error during parsing communities:', row)
            sys.exit(1)

    # get init data about provinces
    sheet = book.sheet_by_index(0)
    for row in range(1, sheet.nrows):
        result['provinces'][str(row)] = dict()
        result['provinces'][str(row)]['name'] = sheet.cell_value(row, 0)
        result['provinces'][str(row)]['type'] = sheet.cell_value(row, 1)
        result['provinces'][str(row)]['community'] = sheet.cell_value(row, 2)
        result['provinces'][str(row)]['tag'] = str(sheet.cell_value(row, 3)).split('.')[0]

        check = False
        for el in result['province_type']:
            if result['province_type'][el]['name'] == result['provinces'][str(row)]['type']:
                result['provinces'][str(row)]['type'] = el
                check = True
        if not check:
            print('Error during parsing provinces:', str(row))
            sys.exit(1)

        check = False
        for el in result['communities']:
            if result['communities'][el]['name'] == result['provinces'][str(row)]['community']:
                result['provinces'][str(row)]['community'] = el
                check = True
        if not check:
            print('Error during parsing communities:', str(row))
            sys.exit(1)

    reply = run(municipalities())
    for i in reply:
        f = str(i['id'])
        result['municipalities'][f] = dict()
        result['municipalities'][f]['province'] = i['province']
        result['municipalities'][f]['name'] = i['name']

    reply = run(stations_list())

    reply = run(stations(reply))
    for i in reply:
        o = str(i['id'])
        result['stations'][o] = dict()
        result['stations'][o]['latitude'] = i['latitude']
        result['stations'][o]['longitude'] = i['longitude']
        if 'municipality' in i:
            result['stations'][o]['municipality'] = i['municipality']
        if 'community' in i:
            result['stations'][o]['community'] = i['community']

    # dump result to file
    with open(file_config, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent = 2)
    f.close()

    # print statistic
    print('total communities: ', len(result['communities']))
    print('total provinces: ', len(result['provinces']))
    print('total municipalities: ', len(result['municipalities']))
    print('total stations: ', len(result['stations']))
