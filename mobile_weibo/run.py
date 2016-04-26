# coding: utf-8

from sys import argv

from get_uids import Weibo_uids
from companies import multi_run
from settings import SEARCH_TYPE


def run_uids(keyword):
    weibo_uid = Weibo_uids(keyword)
    weibo_uid.run()


def run_info(keyword):
    if SEARCH_TYPE == 1:
        uid_file_name = "uids/%s_uids_verified_companies.txt" % keyword
    elif SEARCH_TYPE == 2:
        uid_file_name = "uids/%s_uids_all_users.txt" % keyword
    else:
        raise ValueError("wrong search type.")
    with open(uid_file_name, 'rb') as f:
        uids = f.readlines()
    uids = [uid.strip() for uid in uids]
    multi_run(uids, keyword)


def run(keyword):
    run_uids(keyword)
    run_info(keyword)
    return 1


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
    print('reciving keyword %s' % keyword)
    keyword = keyword.decode('utf-8')
    run_uids(keyword)
    run_info(keyword)
    run(keyword)
