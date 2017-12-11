# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class Dribbble1Pipeline(object):
#     def process_item(self, item, spider):
#         return item

import pymysql

from scrapy.conf import settings
from qiniu import Auth
from qiniu import BucketManager
import random
import time
import hashlib
import re
import uuid

# 下面是将爬取到的信息插入到MySQL数据库中
class HouzzPipeline(object):
    def process_item(self, item, spider):
        access_key = 'WqGpPbXHzArQoc9mkSra0ripmMwWLjyOscGfGAyf'
        secret_key = 'SYNGnkvaIISGywUZfJhFO2qugPeONgNwyR3g2hoi'
        bucket_name = 'lingan-img'
        q = Auth(access_key, secret_key)
        bucket = BucketManager(q)
        # if len(item["img_bigUrl"]) > 0:
        url = item["img_bigUrl"]
        # url = 'https://pre00.deviantart.net/b900/th/pre/f/2012/177/4/5/traditional_house_by_asiansxrulexall-d54w4ke.jpg'
        m = str(random.randint(1, 10)) + str(int(time.time()))
        m = hashlib.md5(m.encode("utf8")).hexdigest()[0:10]
        m = re.sub(r"(?<=\w)(?=(?:\w\w)+$)", "/", m)
        uid = str(uuid.uuid3(uuid.NAMESPACE_DNS, 'url'))
        lastStr = url.rsplit('.', 1)[1]
        key = m + '/' + uid + '.' + lastStr
        print(key)
        ret, info = bucket.fetch(url, bucket_name, key)
        print(info)
        assert ret['key'] == key
        host = settings['MYSQL_HOST']
        user = settings['MYSQL_USER']
        psd = settings['MYSQL_PASSWD']
        db = settings['MYSQL_DBNAME']
        c = settings['CHARSET']
        port = settings['MYSQL_PORT']
        # 数据库连接
        con = pymysql.connect(host=host, user=user, passwd=psd, db=db, charset=c, port=port)
        # 数据库游标
        cue = con.cursor()
        print("mysql connect succes")  # 测试语句，这在程序执行时非常有效的理解程序是否执行到这一步
        # sql="insert into 表名 (字段) values(%s,%s,%s,%s,%s)" % (item['']...)

        # 创三个表，一个图片集表（图片集的名字和链接），一个图片链接表，一个设计师表，图片链接表和图片集表还要建一个对应关系（这个图片属于哪个图片集）

        # sql1 = "insert into behance_imgLink(img_url) values(%s)"
        # params1 = (item["Li_img_list"])
        #
        # sql2 = "insert into behance_picSet(design_name,set_name) values(%s,%s)"
        # params2 = (item["Li_designer"],item["Li_name"])
        # print(parten)
        # print(res)
        # print(new_img_urls)
        try:
            print("insert into houzz_project (project_info,project_name,project_url) values({},{},{})".format(item['project_info'], item['project_name'], item['project_url']))
            cue.execute(
                "insert into houzz_project (project_info,project_name,project_url) values(%s,%s,%s)", (item['project_info'], item['project_name'], item['project_url']))
            # pid = int(con.insert_id())
            # pid = int(cue.lastrowid)
            # print(pid)

            # print("insert into houzz_img (designer_name,collection,relevant_theme,Keywords,img_name,Category,img_bigUrl,img_link,project_url) values({},{},{},{},{},{},{},{},{})".format(item['designer_name'], item['img_collection'], item['relevant_theme'], item['img_Keywords'], item['img_name'], item['img_Category'], item['img_bigUrl'], item['img_link'], item['project_url']))
            # cue.execute("insert into houzz_img (designer_name,collection,relevant_theme,Keywords,img_name,Category,img_bigUrl,img_link,project_url) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            #             (item['designer_name'], item['img_collection'], item['relevant_theme'], item['img_Keywords'], item['img_name'], item['img_Category'], item['img_bigUrl'], item['img_link'], item['project_url']))
            # mid = int(con.insert_id())
            # mid = int(cue.lastrowid)
            # print(mid)
            # cue.execute("insert into houzz_relation (pid,mid) values(%s,%s)", (pid, mid))
            # select img_id, project_id from houzz_img, houzz_project where houzz_img.project_url = houzz_project.project_url;

            # 测试语句
            print("insert success")
        except Exception as e:
            print('Insert error:', e)
            con.rollback()  # 回滚
        else:
            con.commit()  # 提交
        # con.close()  # 关闭

        try:
            # print("insert into houzz_project (project_info,project_name,project_url) values({},{},{})".format(item['project_info'], item['project_name'], item['project_url']))
            # cue.execute(
            #     "insert into houzz_project (project_info,project_name,project_url) values(%s,%s,%s)", (item['project_info'], item['project_name'], item['project_url']))
            # pid = int(con.insert_id())
            # pid = int(cue.lastrowid)
            # print(pid)

            print("insert into houzz_img (designer_name,collection,relevant_theme,Keywords,img_name,Category,img_bigUrl,img_link,project_url,img_key) values({},{},{},{},{},{},{},{},{},{})".format(item['designer_name'], item['img_collection'], item['relevant_theme'], item['img_Keywords'], item['img_name'], item['img_Category'], item['img_bigUrl'], item['img_link'], item['project_url'], key))
            cue.execute("insert into houzz_img (designer_name,collection,relevant_theme,Keywords,img_name,Category,img_bigUrl,img_link,project_url,img_key) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        (item['designer_name'], item['img_collection'], item['relevant_theme'], item['img_Keywords'], item['img_name'], item['img_Category'], item['img_bigUrl'], item['img_link'], item['project_url'], key))
            # mid = int(con.insert_id())
            # mid = int(cue.lastrowid)
            # print(mid)
            # cue.execute("insert into houzz_relation (pid,mid) values(%s,%s)", (pid, mid))
            # sql = 'select img_id, project_id from houzz_img, houzz_project where houzz_img.project_url = houzz_project.project_url'
            # cue.execute(sql)

            # 测试语句
            print("insert success")
        except Exception as e:
            print('Insert error:', e)
            con.rollback()  # 回滚
        else:
            con.commit()  # 提交

        # sql = 'select img_id, project_id from houzz_img, houzz_project where houzz_img.project_url = houzz_project.project_url'
        # cue.execute(sql)
        # # print("insert into houzz_project (project_info,project_name,project_url) values({},{},{})".format(
        # #     item['project_info'], item['project_name'], item['project_url']))
        # cue.execute(
        #     "insert into houzz_relation (img_id,project_id) values(%s,%s)",
        #     (img_id, project_id))

        con.close()  # 关闭
        return item
