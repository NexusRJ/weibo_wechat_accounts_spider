# coding: utf-8

import re

import requests
import json

from settings import AJAX_HEADERS, FIRST_PAGE_URL, AJAX_URL


class Weibo_uids(object):

    def __init__(self, scope, keyword):
        self.scope = scope
        self.keyword = keyword

    def handle_first_page(self, scope, keyword):
        f = open('uids/%s_%s_uids.txt' % (scope, keyword), 'ab')
        url = FIRST_PAGE_URL.format(scope, keyword)
        response = requests.get(url, headers=AJAX_HEADERS)
        uid_re = re.compile('&uid=([0-9]*)')
        uids = re.findall(uid_re, response.content)
        print('start 1')
        for uid in uids:
            print(str(uid)),
            f.write(str(uid))
            f.write('\n')
        print('\n------------------')
        f.close()


    def download_and_parse(self, url):
        response = requests.get(url)
        print(response.status_code)
        weibo_json = json.loads(response.text)
        return response, weibo_json


    def parse_json(self, weibo_json):
        user_list = weibo_json['cards'][0]['card_group']
        max_page = int(weibo_json['maxPage'])
        return (user_list, max_page)

    def error_handle(self, e, code=1, url=''):
        if code == 0:
            message = '%s download failed.' % url
            print(message)
            with open('failed_info/failed_page_list.txt', 'ab') as f:
                f.write(message)
                f.write('\n')
        if code == 1:
            message = '%s parse failed.' % url
            print(message)
            with open('failed_info/failed_page_list.txt', 'ab') as f:
                f.write(message)
                f.write('\n')

    def get_jsons(self, scope, keyword):
        with open("uids/%s_%s_uids.txt" % (scope, keyword), 'ab') as f:
            page_url = AJAX_URL.format(scope, keyword)
            i = 2
            max_page = 3
            while(i <= max_page):
                url = page_url + str(i)
                try:
                    response, weibo_json = self.download_and_parse(url)
                except Exception as e:
                    self.error_handle(e, url=response.url, code=0)
                    continue
                try:
                    user_list, max_page = self.parse_json(weibo_json)
                except TypeError as e:
                    self.error_handle(e, url=response.url, code=1)
                    continue
                print("%s/%s" % (i, max_page))
                for user in user_list:
                    uid = user['user']['id']
                    print(uid),
                    f.write(str(uid))
                    f.write('\n')
                print('\n------------------')
                i += 1

    def run(self):
        self.handle_first_page(self, self.scope, self.keyword)
        self.get_jsons(self, self.scope, self.keyword)
