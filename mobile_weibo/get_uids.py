# coding: utf-8

import re
import time
import random

import requests
import json

from settings import AJAX_HEADERS, FIRST_PAGE_URL, AJAX_URL, FIRST_PAGE_URL_ALL_USER, AJAX_URL_ALL_USER, SEARCH_TYPE


class Weibo_uids(object):

    def __init__(self, keyword):
        self.keyword = keyword
        if SEARCH_TYPE == 1:
            self.ajax_url = AJAX_URL
            self.first_page_url = FIRST_PAGE_URL
            self.uid_file_name = "uids/%s_uids_verified_companies.txt" % keyword
        elif SEARCH_TYPE == 2:
            self.ajax_url = AJAX_URL_ALL_USER
            self.first_page_url = FIRST_PAGE_URL_ALL_USER
            self.uid_file_name = "uids/%s_uids_all_users.txt" % keyword
        else:
            raise ValueError('wrong search_type settings.')

    def handle_first_page(self, keyword):
        f = open(self.uid_file_name, 'ab')
        url = self.first_page_url.format(keyword)
        response = self.download(url)
        uid_re = re.compile('&uid=([0-9]*)')
        uids = re.findall(uid_re, response.content)
        print('start')
        for uid in uids:
            print(str(uid)),
            f.write(str(uid))
            f.write('\n')
        print('\n------------------')
        f.close()

    def download(self, url):
        try:
            response = requests.get(url, headers=AJAX_HEADERS)
        except Exception as e:
            self.error_handle(e, code=0, url=url)
        return response

    def download_and_parse(self, url):
        try:
            response = requests.get(url, headers=AJAX_HEADERS)
            print(response.status_code)
        except Exception as e:
            self.error_handle(e, code=0, url=url)
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

    def get_jsons(self, keyword):
        with open(self.uid_file_name, 'wb') as f:
            page_url = self.ajax_url.format(keyword)
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
                except IndexError as e:
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
                self.wait()

    def wait(self, factor=1):
        t = random.random()
        print("wait for %s seconds" % t)
        time.sleep(t)

    def run(self):
        self.handle_first_page(self.keyword)
        self.get_jsons(self.keyword)
