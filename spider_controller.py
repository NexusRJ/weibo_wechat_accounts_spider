# coding: utf-8

import logging

from wechat.run import run as run_wechat
from mobile_weibo.run import run as run_weibo


class SpiderController(object):

    def __init__(self, keywords, spider='wechat'):
        self.keywords = keywords
        self.spider = spider
        fl = logging.FileHandler('spider_controller.log')
        formatter = logging.Formatter("%(asctime)s-%(levelname)s-%(message)s")
        fl.setFormatter(formatter)
        fl.setLevel(logging.INFO)
        self.logger = logging.getLogger('spider_controller')
        self.logger.addHandler(fl)
        self.logger.setLevel(logging.INFO)

    def invoke_spider(self, keyword, spider_name):
        if spider_name == 'wechat':
            spider = run_wechat
        elif spider_name == 'weibo':
            spider = run_weibo
        else:
            self.logger.error("Wrong spider name.\n")
            return
        result = spider(keyword)
        if result:
            self.logger.info("task %s done.\n" % keyword)
        else:
            self.logger.info("task %s failed.\n" % keyword)
        return

    def start(self):
        for keyword in self.keywords:
            if keyword == '' or keyword is None:
                self.logger.warning("invalid keyword %s.\n" % keyword)
                continue
            try:
                self.invoke_spider(keyword, self.spider)
            except Exception as e:
                self.logger.exception(e)
                continue


if __name__ == "__main__":
    # print("input keywords list, split with ';' please.")
    # task_str = raw_input()
    # tasks = task_str.split(";")
    tasks = ['律师行', '留学']
    controller = SpiderController(tasks)
    controller.start()
