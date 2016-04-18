# coding: utf-8

import os
import re
import time
import random

import requests
import threadpool
import pymongo

from settings import WEIBO_URL, HEADERS, DB_NAME, COLLECTION_NAME


class WeiboDownload(object):

    def __init__(self, uid):
        self.url = WEIBO_URL % str(uid)
        self.uid = uid.strip()

    def download(self):
        response = requests.get(self.url, headers=HEADERS)
        return response

    def get_details(self, response):
        # intro_re = re.compile('<p class=\\\"p_txt\\\">(.*)<')
        print('{0} download {1}'.format(self.uid, response.status_code))
        if response.status_code != 200:
            self.error_handle(response.status_code)
            return None
        text = response.content
        text = text.replace('\\', '')
        name_re = re.compile("<title>(.*)</title>")
        intro_re = re.compile('<p class="p_txt">(.*)</p>')
        contact_re = re.compile('<span class="pt_detail">(.*)</span>')
        tel_re = re.compile('([0-9-]{7,14})')
        link_re = re.compile('<a href=(.*?) title=(.*?) alt')
        email_re = re.compile('(\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*)')
        name = try_re(name_re, text).replace('的微博_微博', '')
        contact = try_re(contact_re, text)
        tel = try_re(tel_re, contact)
        intro = try_re(intro_re, text)
        email = try_re(email_re, contact)
        links = re.findall(link_re, contact)
        # print(contact)
        d = dict()
        d['name'] = name
        d['intro'] = intro
        d['tel'] = tel
        d['links'] = links
        d['email'] = email
        d['url'] = self.url
        return d

    def save_to_mongo(self, dict_d):
        client = pymongo.MongoClient('localhost', 27017)
        collection = client[DB_NAME][COLLECTION_NAME]
        url = dict_d['url']
        try:
            self.is_existed(url, collection)
        except:
            try:
                time.sleep(2)
                self.is_existed(url, collection)
            except Exception as e:
                self.error_handle(e)
        try:
            collection.insert_one(dict(dict_d))
            print('%s done.' % dict_d['name'])
            return 1
        except Exception as e:
            return self.error_handle(e)

    def error_handle(self, e):
        if isinstance(e, Exception):
            with open('failed_info/failed_company.txt', 'ab') as f:
                f.write('{0}\n'.format(self.uid))
            print('%s failed.' % self.uid),
            print e.message
            return None
        else:
            with open('failed_company.txt', 'ab') as f:
                f.write('{0}\n'.format(self.uid))
            print ('%s failed.'.format(self.uid)),
            print(e)
            return None

    def run(self):
        print('%s start.' % self.uid)
        res = self.download()
        d = self.get_details(res)
        status = self.save_to_mongo(d)
        time.sleep(random.random()*5)
        if status == 1:
            return 1
        else:
            return None

    def is_existed(self, url, collection):
        record = collection.find_one({'url': url})
        if record:
            print(record['name'] + 'existed.')
            collection.delete_many({'url': url})

    def try_one_more_time(self, func, *kwargs):
        time.sleep(1)
        try:
            func(kwargs)
        except Exception as e:
            self.error_handle(e)
            raise e


def try_re(re_content, text_content):
    try:
        res = re.search(re_content, text_content).groups()[0]
        return res
    except AttributeError:
        return ''


def run(uid):
    wd = WeiboDownload(uid)
    wd.run()


def multi_run(uids):
    pool = threadpool.ThreadPool(10)
    reqs = threadpool.makeRequests(run, uids)
    [pool.putRequest(req) for req in reqs]
    pool.wait()

if __name__ == '__main__':
    f = open('weibo_uids.txt', 'rb')
    uids = f.readlines()
    f.close()
    uids = [uid.strip() for uid in uids]
    multi_run(uids)
    # wd = WeiboDownload('3289319380')
    # wd.run()
    # d = wd.get_details(wd.download())
    # for i in d:
    #     print d[i]
