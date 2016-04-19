# coding: utf-8

import time
import random
import re
import logging
import traceback
from sys import argv

import requests
import pymongo
import bson
from lxml import etree
from concurrent.futures import ThreadPoolExecutor, as_completed

from settings import HEADERS, SEARCH_ACCOUNT_URL, SEARCH_ARTICLE_URL, MONGO_HOST, MONGO_PORT


class WechatSpider(object):

    def __init__(self, keyword):
        self.keyword = keyword
        db_name = keyword.replace(' ', '_').decode('utf-8')
        client = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
        self.collection = client['wechat_offical'][db_name]
        fl = logging.FileHandler('wechat_offical.log')
        sl = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s-%(levelname)s-%(message)s')
        fl.setFormatter(formatter)
        fl.setLevel(logging.ERROR)
        sl.setFormatter(formatter)
        sl.setLevel(logging.DEBUG)
        self.logger = logging.getLogger('wechat_offical')
        self.logger.addHandler(sl)
        self.logger.addHandler(fl)
        self.logger.setLevel(logging.DEBUG)

    def download(self, url, mode=0):
        '''
        mode=0 for download html
        mode=1 for download binary file
        '''
        try:
            if mode == 0:
                response = requests.get(url, headers=HEADERS)
            elif mode == 1:
                response = requests.get(url)
            else:
                response = None
        except Exception as e:
            self.error_handle(e, error_type='NetworkError', url=url)
        return response

    def download_image(self, url, file_type='.jpg'):
        time.sleep(random.random())
        response = self.download(url, 1)
        return response

    def get_page_count(self):
        self.logger.info("start getting pages count.")
        url = SEARCH_ACCOUNT_URL.format(self.keyword, 1)
        response = self.download(url)
        while self.if_Captcha(response):
            self.logger.warning('%s need captcha.' % url)
            raw_input()
            response = self.download(url)
        dom_tree = etree.HTML(response.content)
        count = int(dom_tree.xpath("//resnum[@id='scd_num']/text()")[0])
        self.page_count = count/10 + 1 if count % 10 else count/10
        self.logger.info("%s items %s pages got." % (count, self.page_count))

    def generate_page_url(self, mode=1):
        '''
        mode 1 for searching offical accounts,
        mode 2 for searching wechat articles.
        '''
        if mode == 1:
            index_url = SEARCH_ACCOUNT_URL
        elif mode == 2:
            index_url = SEARCH_ARTICLE_URL
        else:
            raise ValueError('Wrong argument when generate page url')
        for page in range(1, self.page_count+1):
            url = index_url.format(self.keyword, page)
            self.logger.info('yield page %s.' % page)
            yield url

    def if_Captcha(self, response):
        captcha_re = re.compile("id=\"seccodeImage\"")
        if re.search(captcha_re, response.text):
            return True
        else:
            return False

    def error_handle(self, exception, **kwargs):
        error_type = kwargs.get('error_type', '')
        wechat_id = kwargs.get('wechat_id', '')
        url = kwargs.get('url', '')
        trace = kwargs.get('trace', '')
        self.logger.error('<error_type:%s><url:%s><wechat_id:%s>,error_message:%s, traceback:%s \n' % (error_type, url, wechat_id, exception.message, trace))
        return

    def parse_page(self, url):
        t = random.random() * 4
        time.sleep(t)
        self.logger.info("wait for %s seconds, %s start." % (t, url))
        response = self.download(url, 0)
        while self.if_Captcha(response):
            self.logger.warning('%s need captcha.' % url)
            raw_input()
            response = self.download(url, 0)
        try:
            dom_tree = etree.HTML(response.content)
        except ValueError as e:
            self.error_handle(e, url=url, error_type='HtmlParseError', trace=traceback.format_exc())
        items = dom_tree.xpath("//div[contains(@id, 'sogou_vr_11002301_box_')]")
        get_string = lambda x: x.xpath("string(.)")
        for item in items:
            try:
                url = item.xpath("./@href")[0]
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
                # this part for getting the pos code image
                pos_code_url = item.xpath(".//div[@class='pos-box']/img/@src")[0]
            except IndexError as e:
                self.error_handle(e, url=url, error_type='XpathError', trace=traceback.format_exc())
            pos_code_image = self.download_image(pos_code_url, '.jpg')
            while self.if_Captcha(pos_code_image):
                self.logger.warning('%s need captcha.' % url)
                raw_input()
                pos_code_image = self.download_image(pos_code_url, '.jpg')
            # convert image to bson binary type for saving in mongo.
            pos_code_image = bson.Binary(pos_code_image.content)
            pos_code_image_name = "%s_%s.jpg" % (name, wechat_name)
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
            self.logger.info('%s done.' % (item['name']))
        except Exception as e:
            self.error_handle(e, url=item['url'], wechat_id=item['wechat_id'], error_type='MongoError', trace=traceback.format_exc())

    def single_thread_run(self):
        self.get_page_count()
        print(self.page_count)
        for page in range(1, self.page_count+1):
            url = SEARCH_ACCOUNT_URL.format(self.keyword, page)
            try:
                self.parse_page(url)
            except KeyboardInterrupt as e:
                self.error_handle(e)
            except Exception as e:
                self.error_handle(e, url=url, trace=traceback.format_exc())
                continue

    def multi_thread_run(self):
        self.get_page_count()
        with ThreadPoolExecutor(max_workers=5) as executor:
            queue = {executor.submit(self.parse_page, url) for url in self.generate_page_url()}


if __name__ == "__main__":
    keyword = argv[1]
    ws = WechatSpider(keyword)
    # for i in range(3, 8):
    #     ws.parse_page('http://weixin.sogou.com/weixin?type=1&query=%E6%B5%B7%E5%A4%96+%E7%BD%AE%E4%B8%9A&ie=utf8&_sug_=n&_sug_type_=&page={0}'.format(i))
    #     time.sleep(2)
    ws.multi_thread_run()
