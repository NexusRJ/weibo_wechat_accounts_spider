# coding: utf-8

from migrate_info import WeiboDownload

f = open('failed_company.txt', 'rb')
l = f.readlines()
for uid in l:
    wd = WeiboDownload(uid.strip())
    status = wd.run()
    if status == 1:
        l.remove(uid)
    else:
        continue
