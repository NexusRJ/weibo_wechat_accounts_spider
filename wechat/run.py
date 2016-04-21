# coding: utf-8

from companies import WechatSpider
from sys import argv


def run(keyword):
    print("receiving keyword %s" % keyword)
    ws = WechatSpider(keyword)
    ws.multi_thread_run()
    return 1


if __name__ == '__main__':
    if len(argv) > 2:
        keyword = reduce(lambda x, y: x + ' ' + y, argv[1:])
    elif argv == 2:
        keyword = argv[1]
    else:
        raise ValueError("Wrong arguments.")
    run(keyword)
