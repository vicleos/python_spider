# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaItem(scrapy.Item):
    # define the fields for your item here like:
    district_id = scrapy.Field()
    lng = scrapy.Field()
    lat = scrapy.Field()
    name = scrapy.Field()
    project_name = scrapy.Field()
    min_frame_area = scrapy.Field()
    max_frame_area = scrapy.Field()
    price = scrapy.Field()
    average_price = scrapy.Field()
    image_url = scrapy.Field()
    rooms = scrapy.Field()
    frame_area = scrapy.Field()
    house_type = scrapy.Field()
    price_show_config = scrapy.Field()
    show_price_unit = scrapy.Field()
    show_price_desc = scrapy.Field()
