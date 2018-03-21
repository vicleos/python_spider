# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import traceback


class LianjiaPipeline(object):
    def process_item(self, item, spider):
        db = pymysql.connect(host="192.168.1.15", user="root", password="123456", db="kg_house", port=3306, charset="utf8")
        # 使用cursor方法获取操作游标
        db_cur = db.cursor()

        # sql = "insert into spider_district(\
        # district_id, \
        # district_name, \
        # quanpin, \
        # lat, \
        # lng, \
        # position_border, \
        # count) \
        #  values(%s, %s, %s, %s, %s, %s, %s)"

        # values = (item['district_id'], item['district_name'].encode('utf8').decode('unicode_escape'),  item['quanpin'], item['lat'], item['lng'], item['position_border'].encode('utf8'), item['count'])

        sql = "insert into spider_biz_circle(\
        area_name, \
        area_id, \
        lat, \
        lng, \
        house_count, \
        position_border, \
        min_price_total, \
        avg_unit_price) \
         values(%s, %s, %s, %s, %s, %s, %s, %s)"

        values = (item['area_name'].encode('utf8').decode('unicode_escape'), item['area_id'],  item['lat'], item['lng'], item['house_count'], item['position_border'], item['min_price_total'], item['avg_unit_price'])

        try:
            print('item =======', item)
            db_cur.execute(sql, values)
            db.commit()
        except Exception as e:
            traceback.print_exc()
            db.rollback()
            print(e)
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
