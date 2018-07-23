# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import json
from baiduimage.items import BaiduimageItem
from baiduimage.settings import IMAGES_KEYWORD, IMAGES_NUM


class BaiduSpider(scrapy.Spider):
    name = 'baidu'
    allowed_domains = ['image.baidu.com']
    # start_urls = ['http://image.baidu.com/']

    current_page_number = 30
    image_num = 0
    baidu_pic_url = 'http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord={search_word}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=&z=9&ic=&word={search_word}&s=&se=&tab=&width=0&height=0&face=&istype=&qc=&nc=&fr=&pn={page_number}&rn=30&gsm=1e&1532263828693='

    def start_requests(self):
        yield Request(self.baidu_pic_url.format(search_word=IMAGES_KEYWORD, page_number=self.current_page_number),
                      callback=self.parse_image)

    def parse_image(self, response):
        imgs = json.loads(response.text)['data']
        for img in imgs:
            item = BaiduimageItem()
            try:
                item['image_url'] = img['middleURL']
                item['image_referer'] = response.url
                item['image_num'] = self.image_num
                yield item
            except Exception as e:
                print(e)
            self.image_num += 1
        self.current_page_number += 30
        if self.current_page_number <= IMAGES_NUM:
            yield Request(self.baidu_pic_url.format(search_word=IMAGES_KEYWORD, page_number=self.current_page_number),
                          callback=self.parse_image)
