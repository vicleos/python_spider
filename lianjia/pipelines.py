# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import sys
import traceback


class LianjiaPipeline(object):
    def process_item(self, item, spider):
        db = pymysql.connect(host="192.168.1.15", user="root", password="123456", db="kg_house", port=3306, charset="utf8")
        # 使用cursor方法获取操作游标
        db_cur = db.cursor()
        sql = "insert into spider_house(\
        district_id, \
        lng, \
        lat, \
        name, \
        project_name, \
        min_frame_area, \
        max_frame_area, \
        price, \
        average_price, \
        image_url, \
        rooms, \
        frame_area, \
        house_type, \
        price_show_config, \
        show_price_unit, \
        show_price_desc) \
         values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        try:
            print('item =======', item)
            db_cur.execute(sql, (item['district_id'], item['lng'], item['lat'], item['name'], item['project_name'], item['min_frame_area'], item['max_frame_area'], item['price'], item['average_price'], item['image_url'], item['rooms'], item['frame_area'], item['house_type'], item['price_show_config'], item['show_price_unit'], item['show_price_desc'], ))
            db.commit()
        except:
            traceback.print_exc()
            db.rollback()
            raise
        finally:
            db.close()
        # with open("home_data.txt", 'ab') as fp:
        #     fp.write("===========================".encode("utf8")+b'\n')
        #     fp.write(item['name'].encode("utf8")+b'\n')
        #     fp.write(item['price'].encode("utf8")+b'\n')
        #     fp.write(str(item['second']).encode("utf8")+b'\n')
        #     fp.write(item['addr'].encode("utf8")+b'\n')
        #     fp.write(str(item['room']).encode("utf8")+b'\n')
        #     fp.write("===========================".encode("utf8")+b'\n')
