# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from baiduimage.settings import IMAGES_STORE
import os
import requests


class BaiduimagePipeline(object):
    def process_item(self, item, spider):
        header = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
            'Referer': item['image_referer']
        }
        if not os.path.exists(IMAGES_STORE) and len(item['image_url'].strip()) != 0:
            os.mkdir(IMAGES_STORE)

        os.chdir(IMAGES_STORE)

        req = requests.get(item['image_url'], headers=header)

        if req.status_code == requests.codes.ok:
            with open(str(item['image_num']) + 'jpg', 'wb') as f:
                f.write(req.content)

        return item
