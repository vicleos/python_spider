# -*- coding: utf-8 -*-
import scrapy
# import re
# from lianjia.items import LianjiaItem
# from lianjia.items import LJDistrictItem
# from lianjia.items import LJBizCircleItem
# from lianjia.items import FangDistAreaItem
from lianjia.items import FangSchoolListItem
# import json
# import re
from scrapy import log


class ZzljSpider(scrapy.Spider):
    name = 'zzlj'
    # allowed_domains = ['zz.fang.lianjia.com']
    allowed_domains = ['esf.fz.fang.com']
    # start_urls = ['http://esf.fz.fang.com/map/?a=getDistArea&city=xm', 'http://zz.fang.lianjia.com/loupan/', 'https://zz.fang.lianjia.com/xinfang/mapsearchloupan', 'https://zz.fang.lianjia.com/xinfang/mapsearchdistrict?&&position_border=1&callback=jQuery11110023956285515926545_1521108328084&_=1521108328085', 'https://ajax.lianjia.com/ajax/mapsearch/area/bizcircle?&&city_id=410100&callback=jQuery111107924035109078831_1521623214218&_=1521623214224']
    start_urls = ['http://esf.fz.fang.com/school/']
    pageNum = 1
    listItem = {}

    def parseDetail(self, response):
        fromId = ''.join(response.request.flags)
        listItem = self.listItem[fromId]
        shortName = response.css('.schoolname span.info::text').extract_first().replace(']', '')
        listItem['short_name'] = shortName.split('：')[1] if len(shortName.split('：')) > 1 else ''
        listItem['tel_number'] = response.css('.SchoolInfo .floatr ul li:nth-child(6)::text').extract_first()
        listItem['tel_number'] = listItem['tel_number'] if listItem['tel_number'] is not None else ''
        log.msg("listItem['tel_number'] -> ")
        log.msg(listItem['tel_number'])
        listItem['guide'] = ''
        listItem['students_scope'] = ''
        listItem['conditions'] = ''
        listItem['intro'] = ''
        listItem['feature'] = ''
        yield scrapy.Request('http://esf.fz.fang.com/school/' + fromId + '/profile/#profile', callback=self.parseProfile, flags=fromId)

    def parseProfile(self, response):
        fromId = ''.join(response.request.flags)
        try:
            listItem = self.listItem[fromId]
        except AttributeError as e:
            log.msg('not has fromId =============> ')
            log.msg(fromId)

        listItem['guide'] = response.css('.profile dl:nth-child(1) dd p:nth-child(1)').extract_first()
        listItem['intro'] = response.css('.profile dl:nth-child(2) dd p:nth-child(1)').extract_first()
        listItem['students_scope'] = response.css('.profile dl:nth-child(3) dd p:nth-child(1)').extract_first()
        listItem['conditions'] = response.css('.profile dl:nth-child(4) dd p:nth-child(1)').extract_first()
        listItem['feature'] = response.css('.profile dl:nth-child(5) dd p:nth-child(1)').extract_first()
        yield listItem

    def parse(self, response):
        if (response.url.count('school') > 0 and self.pageNum <= 6):
            print('school start ==================')
            # print('response==========', response.css('div.schoollist dl'))
            # 网页列表解析
            listData = response.css('div.schoollist dl')
            self.pageNum += 1
            nextPageUrl = self.start_urls[0] + "i3" + str(self.pageNum)
            print('nextPageUrl========', nextPageUrl)

            # 先将源ID存放在short_name中,采集完列表后，根据short_name继续采集详情内容，再次保存更新
            # 先将 tags 放入 pinyin 中，后续由 laravel seeder 来处理
            # 学校所在小区根据地址或名称反查得到行政区
            for lineRow in listData:
                item = FangSchoolListItem()
                fromId = str(lineRow.css('.title a::attr(href)').extract_first()).replace('/school/', '').replace('.htm', '')
                detailLink = lineRow.css('.title a::attr(href)').extract_first()
                item['short_name'] = detailLink
                item['name'] = lineRow.css('.title a::text').extract_first()
                item['img_url'] = lineRow.css('a img::attr(src)').extract_first()
                item['address'] = lineRow.css('span.iconAdress::text').extract_first()
                item['school_note_tag'] = lineRow.css('span.sch-noteTag::text').extract_first()
                item['tags'] = ','.join(lineRow.css('span[class*="color"]::text').extract())
                # print('list item', item)
                self.listItem[fromId] = item
                yield scrapy.Request('http://esf.fz.fang.com' + detailLink, callback=self.parseDetail, flags=fromId)
                # yield item

            if self.pageNum <= 6:
                yield scrapy.Request(nextPageUrl, callback=self.parse)
            pass
        elif (response.url.count('getDistArea') > 0):
            # distListJson = json.loads(response.body)
            # for lineRow in distListJson:
            #     item = FangDistAreaItem()
            #     item['source_id'] = lineRow['id']
            #     item['name'] = lineRow['name']
            #     item['lng'] = lineRow['x']
            #     item['lat'] = lineRow['y']
            #     item['quanpin'] = lineRow['quanpin']
            #     item['position_border'] = lineRow['baidu_coord']
            #     item['area_list'] = lineRow['area']
            #     yield item
            pass

        elif(response.url.count('mapsearchloupan') > 0):
            # print('================ json parse start ===============')
            # mapListJson = json.loads(response.body)
            # for lineRow in mapListJson['data']:
            #     for rowItem in mapListJson['data'][lineRow]:
            #         item = LianjiaItem()
            #         item['district_id'] = rowItem['district_id']
            #         item['lng'] = rowItem['longitude']
            #         item['lat'] = rowItem['latitude']
            #         item['name'] = rowItem['resblock_name']
            #         item['project_name'] = rowItem['project_name']
            #         item['min_frame_area'] = rowItem['min_frame_area']
            #         item['max_frame_area'] = rowItem['max_frame_area']
            #         item['price'] = rowItem['show_price']
            #         item['average_price'] = rowItem['average_price']
            #         item['image_url'] = rowItem['cover_pic']
            #         item['rooms'] = rowItem['rooms']
            #         item['frame_area'] = rowItem['resblock_frame_area']
            #         item['house_type'] = rowItem['house_type']
            #         item['price_show_config'] = rowItem['price_show_config']
            #         item['show_price_unit'] = rowItem['show_price_unit']
            #         item['show_price_desc'] = rowItem['show_price_desc']
            #         yield item
            pass
        elif(response.url.count('mapsearchdistrict') > 0):
            # print('================ mapsearchdistrict json parse start ===============')
            # bodyStr = str(response.body)
            # bodyStr = bodyStr.replace('/**/jQuery11110023956285515926545_1521108328084(', '')[2:-2]
            # mapListJson = json.loads(bodyStr, encoding='utf-8')
            # # print(mapListJson)
            # for lineRow in mapListJson['data']:
            #     print('======================', lineRow['latitude'])
            #     item = LJDistrictItem()
            #     item['district_id'] = lineRow['district_id']
            #     item['lng'] = lineRow['longitude']
            #     item['lat'] = lineRow['latitude']
            #     item['district_name'] = lineRow['district_name']
            #     item['quanpin'] = lineRow['quanpin']
            #     item['position_border'] = lineRow['positionBorder']
            #     item['count'] = lineRow['count']
            #     yield item
            pass
        elif(response.url.count('bizcircle') > 0):
            # print('================ bizcircle json parse start ===============')
            # bodyStr = str(response.body)
            # bodyStr = bodyStr.replace('jQuery111107924035109078831_1521623214218(', '')[2:-2]
            # mapListJson = json.loads(bodyStr, encoding='utf-8')
            # # print(mapListJson)
            # for lineRow in mapListJson['data']:
            #     print('======================', lineRow['latitude'])
            #     item = LJBizCircleItem()
            #     item['area_name'] = lineRow['name']
            #     item['area_id'] = lineRow['id']
            #     item['lat'] = lineRow['latitude']
            #     item['lng'] = lineRow['longitude']
            #     item['house_count'] = lineRow['house_count']
            #     item['position_border'] = lineRow['position_border']
            #     item['min_price_total'] = lineRow['min_price_total']
            #     item['avg_unit_price'] = round(lineRow['bs_avg_unit_price'], 2) * 100
            #     yield item
            pass
        else:
            # print('xxxxxxxxxxxxxx ==========', response.url)
            # 网页列表解析
            # lianjias = response.css('ul.resblock-list-wrapper li')
            # self.pageNum += 1
            # nextPageUrl = 'http://zz.fang.lianjia.com/loupan/' + "pg" + str(self.pageNum)

            # for eachLi in lianjias:
            #     item = LianjiaItem()
            #     item['name'] = eachLi.css('a::attr(title)').extract_first()
            #     item['price'] = eachLi.css('span.number::text').extract_first()
            #     item['second'] = re.sub("\D", "", str(eachLi.css('div.second::text').extract_first()))
            #     item['addr'] = eachLi.css('div.resblock-location a::text').extract_first()
            #     item['room'] = eachLi.css('a.resblock-room > span::text').extract_first()
            #     # print("=========", item['name'])
            #     # print("=========", item['price'])
            #     # print("=========", item['second'])
            #     # print("=========", item['addr'])
            #     # print("=========", item['room'])
            #     yield item
            # if self.pageNum < 25:
            #     yield scrapy.Request(nextPageUrl, callback=self.parse)
            pass
