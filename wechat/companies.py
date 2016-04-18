# coding: utf-8

import time
import random

import requests
import pymongo
import bson
from lxml import etree
import concurrent

from settings import HEADERS, SEARCH_ACCOUNT_URL, SEARCH_ARTICLE_URL, HOST_URL, MONGO_HOST, MONGO_PORT


class WechatSpider(object):

    def __init__(self, keyword):
        self.keyword = keyword
        db_name = keyword.replace(' ', '_').decode('utf-8')
        client = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
        self.collection = client['wechat_offical'][db_name]

    def download(self, url, mode=0):
        '''
        mode=0 for download html
        mode=1 for download binary file
        '''
        if mode == 0:
            response = requests.get(url, headers=HEADERS)
        elif mode == 1:
            response = requests.get(url)
        else:
            response = None
        return response

    def download_image(self, url, file_type='.jpg'):
        print(url)
        response = self.download(url, 1)
        file_name = url + file_type
        return (file_name, response.content)

    def get_page_count(self):
        url = SEARCH_ACCOUNT_URL.format(self.keyword, 1)
        response = requests.get(url, headers=HEADERS)
        dom_tree = etree.HTML(response.content)
        count = dom_tree.xpath("//resnum[@id='scd_num']/text()")
        self.page_count = count/10 + 1 if count % 10 else count/10

    def parse_page(self, url):
        response = self.download(url, 0)
        dom_tree = etree.HTML(response.content)
        items = dom_tree.xpath("//div[contains(@id, 'sogou_vr_11002301_box_')]")
        get_string = lambda x: x.xpath("string(.)")
        for item in items:
            url = HOST_URL + item.xpath("./@href")[0]
            name = item.xpath(".//h3")[0]
            name = get_string(name)
            wechat_name = item.xpath(".//h4/span/label/text()")[0]
            p_tags = item.xpath(".//p[@class='s-p3']")
            introduction = p_tags[0].xpath("./span[@class='sp-txt']")[0]
            if len(p_tags) == 3:
                authentication = p_tags[1].xpath("./span[@class='sp-txt']")[0]
                authentication = get_string(authentication)
            else:
                authentication = ''
            introduction = get_string(introduction)
            pos_code_url = item.xpath(".//div[@class='pos-box']/img/@src")[0]
            pos_code_image_name, pos_code_image = self.download_image(pos_code_url, '.jpg')
            pos_code_image = bson.Binary(pos_code_image)
            pos_code_image_name = pos_code_image_name.split('/')[-1]
            item_result = dict()
            item_result['name'] = name
            item_result['wechat_id'] = wechat_name
            item_result['introduction'] = introduction
            item_result['url'] = url
            item_result['authentication'] = authentication
            item_result['pos_code_image'] = [pos_code_image_name, pos_code_image]
            self.save_to_mongo(item_result)

    def save_to_mongo(self, item):
        try:
            self.collection.insert_one(item)
            print('%s done.' % (item['name']))
        except:
            print('%s:%s failed save.' % (item['name'], item['url']))

    def run(self):
        self.get_page_count()
        for page in self.page_count:
            url = SEARCH_ACCOUNT_URL.format(self.keyword, page)
            try:
                self.parse_page(url)
            except:
                print('%s was wrong' % url)
                continue


if __name__ == "__main__":
    ws = WechatSpider('海外置业')
    import time
    for i in range(3, 8):
        ws.parse_page('http://weixin.sogou.com/weixin?type=1&query=%E6%B5%B7%E5%A4%96+%E7%BD%AE%E4%B8%9A&ie=utf8&_sug_=n&_sug_type_=&page={0}'.format(i))
        time.sleep(2)
