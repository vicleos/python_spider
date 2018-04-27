# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import traceback
import time


class LianjiaPipeline(object):
    def batchInsertDistArea(self, item):
        if('area_list' in item and type(item['area_list']) is list):
            # 插入行政区数据
            self.insertSingle(item, 'area')
            for bizCircleRow in item['area_list']:
                print('bizCircleRow ==================')
                self.batchInsertDistArea(bizCircleRow)
        else:
            # 插入商圈数据
            print('not list to insert single item ~~~~~~~~~~~~~~~~')
            self.insertSingle(item, 'biz')

    def insertSingle(self, item, dataType):
        db = pymysql.connect(host="192.168.1.15", user="root", password="123456", db="kg_house", port=3306, charset="utf8")
        # 使用cursor方法获取操作游标
        db_cur = db.cursor()

        sql = "insert into dist_area(\
        city_id, \
        from_id, \
        area_type, \
        parent_id, \
        name, \
        lng, \
        lat, \
        quanpin, \
        position_border) \
         values(%s, %s, %s, %s, %s, %s, %s, %s, %s)"

        if dataType == 'area':
            city_id = 350200
            from_id = item['source_id']
            parent_id = 0
            name = item['name']
            lng = item['lng']
            lat = item['lat']
            areaType = 1
            quanpin = item['quanpin']
            positionBorder = item['position_border']
        elif dataType == 'biz':
            city_id = 350200
            from_id = item['id']
            parent_id = int(item['disId'])
            name = item['name']
            lng = item['x']
            lat = item['y']
            areaType = 2
            quanpin = ''
            positionBorder = item['baidu_coord']

        values = (city_id, from_id, areaType, parent_id, name, lng, lat, quanpin, positionBorder)

        try:
            db_cur.execute(sql, values)
            db.commit()
        except Exception as e:
            traceback.print_exc()
            db.rollback()
            print(e)
            raise
        finally:
            db.close()

    def insertSchool(self, item):
        db = pymysql.connect(host="192.168.1.15", user="root", password="123456", db="kg_house", port=3306, charset="utf8")
        # 使用cursor方法获取操作游标
        db_cur = db.cursor()

        sql = "insert into school(\
        name, \
        short_name, \
        city_id, \
        img_url, \
        type, \
        level, \
        address, \
        pinyin, \
        feature, guide, students_scope, intro, conditions, created_at, tel_number) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        name = item['name']
        short_name = item['short_name']
        city_id = 350100
        img_url = item['img_url']
        typeInt = 0
        level = 0
        # 学校等级,0=普通,1=区重点,2=市重点
        if (item['school_note_tag'] == '市重点'):
            level = 2
        elif (item['school_note_tag'] == '区重点'):
            level = 1
        address = item['address']
        pinyin = item['tags']
        created_at = int(time.time())
        tel_number = item['tel_number'] if len(item['tel_number']) > 0 else ''

        values = (name, short_name, city_id, img_url, typeInt, level, address, pinyin, item['feature'], item['guide'], item['students_scope'], item['intro'], item['conditions'], created_at, tel_number)

        try:
            # print('values============== ', values)
            db_cur.execute(sql, values)
            db.commit()
        except Exception as e:
            traceback.print_exc()
            db.rollback()
            print(e)
            raise
        finally:
            db.close()

    def process_item(self, item, spider):
        # 批量插入行政区及商圈相关数据
        # self.batchInsertDistArea(item)

        # 批量插入学校列表数据
        self.insertSchool(item)
        pass
