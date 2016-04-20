# coding: utf-8

from sys import argv

from get_uids import Weibo_uids
from companies import multi_run


def run_uids(keyword):
    weibo_uid = Weibo_uids(keyword)
    weibo_uid.run()


def run_info(keyword):
    with open('uids/%s_uids.txt' % (keyword), 'rb') as f:
        uids = f.readlines()
    uids = [uid.strip() for uid in uids]
    multi_run(uids)


if __name__ == '__main__':
    # if option == 0:
    #     run_uids(SCOPE, KEYWORD)
    # elif option == 1:
    #     run_info(SCOPE, KEYWORD)
    # elif option == 2:
    #     run_uids(SCOPE, KEYWORD)
    #     run_info(SCOPE, KEYWORD)
    # else:
    #     print('wrong argv.')
    if len(argv) == 2:
        keyword = argv[1]
    else:
        keyword = reduce(lambda x, y: x+'+'+y, argv[1:])
    run_uids(keyword)
    run_info(keyword)
