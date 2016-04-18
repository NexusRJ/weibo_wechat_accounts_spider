# coding: utf-8

from sys import argv

from get_uids import Weibo_uids
from companies import multi_run
from settings import SCOPE, KEYWORD


def run_uids(scope, keyword):
    weibo_uid = Weibo_uids(scope, keyword)
    weibo_uid.run()


def run_info(scope, keyword):
    with open('uids/%s_%s_uids.txt' % (scope, keyword), 'rb') as f:
        uids = f.readlines()
    uids = [uid.strip() for uid in uids]
    multi_run(uids)


if __name__ == '__main__':
    option = argv[1]
    if option == 0:
        run_uids(SCOPE, KEYWORD)
    elif option == 1:
        run_info(SCOPE, KEYWORD)
    elif option == 2:
        run_uids(SCOPE, KEYWORD)
        run_info(SCOPE, KEYWORD)
    else:
        print('wrong argv.')
