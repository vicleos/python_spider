# -*- coding: utf-8 -*-
import scrapy
import re
from lianjia.items import LianjiaItem
import json


class ZzljSpider(scrapy.Spider):
    name = 'zzlj'
    allowed_domains = ['zz.fang.lianjia.com']
    start_urls = ['http://zz.fang.lianjia.com/loupan/', 'https://zz.fang.lianjia.com/xinfang/mapsearchloupan']
    pageNum = 1

    def parse(self, response):
        # json 解析, 取出坐标
        if response.url.count('mapsearchloupan') > 0:
            print('================ json parse start ===============')
            mapListJson = json.loads(response.body)
            for lineRow in mapListJson['data']:
                for rowItem in mapListJson['data'][lineRow]:
                    item = LianjiaItem()
                    item['district_id'] = rowItem['district_id']
                    item['lng'] = rowItem['longitude']
                    item['lat'] = rowItem['latitude']
                    item['name'] = rowItem['resblock_name']
                    item['project_name'] = rowItem['project_name']
                    item['min_frame_area'] = rowItem['min_frame_area']
                    item['max_frame_area'] = rowItem['max_frame_area']
                    item['price'] = rowItem['show_price']
                    item['average_price'] = rowItem['average_price']
                    item['image_url'] = rowItem['cover_pic']
                    item['rooms'] = rowItem['rooms']
                    item['frame_area'] = rowItem['resblock_frame_area']
                    item['house_type'] = rowItem['house_type']
                    item['price_show_config'] = rowItem['price_show_config']
                    item['show_price_unit'] = rowItem['show_price_unit']
                    item['show_price_desc'] = rowItem['show_price_desc']
                    yield item
        else:
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
