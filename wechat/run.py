# coding: utf-8

from companies import WechatSpider

if __name__ == '__main__':
    keyword = argv[1]
    ws = WechatSpider(keyword)
    ws.multi_thread_run()
