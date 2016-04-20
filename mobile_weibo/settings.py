# coding: utf-8

AJAX_HEADERS = {
    "Host": "m.weibo.cn",
    "Connection": "keep-alive",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36",
    "Accept-Encoding": "gzip, deflate, sdch",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Cookie": "_T_WM=d2e6e757d050207f4be576710e8097db; SUB=_2A2578Jn_DeTxGeNG41YT8y7KyDSIHXVZGie3rDV6PUJbrdBeLXGgkW1LHeuR_BlqAt8aDXsTs4l1O6lwmruERQ..; SUHB=08JrDE7ns_fdGH; SSOLoginState=1458891183; H5_INDEX=0_all; H5_INDEX_TITLE=Laura%E9%80%97%E9%80%97%E6%9E%97%E7%BF%A6%E5%8D%93%E7%84%B6; gsid_CTandWM=4ujUCpOz5NgPuiDYKxVa7oGKWai; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D100103type%253D39%2526q%253D%25E8%258B%258F%25E5%25B7%259E%2B%25E7%25A7%25BB%25E6%25B0%2591%2526t%253D%26fid%3D100103type%253D3%2526q%253D%25E8%258B%258F%25E5%25B7%259E%2B%25E7%25A7%25BB%25E6%25B0%2591%2526isv%253D3%2526specfilter%253D1%2526log_type%253D6%26uicode%3D10000011"
}
# DATA = {
#     "containerid": "",
#     "containerid": "100103type=3&q=上海 移民&isv=3&specfilter=1&log_type=6",
#     "title": "机构认证-上海 移民",
#     "uid": "5884230638",
#     "v_p": "11",
#     "ext": "",
#     "fid": "100103type=3&q=上海 移民&isv=3&specfilter=1&log_type=6",
#     "uicode": "10000011",
#     "next_cursor": "",
#     "page": "2",
# }

FIRST_PAGE_URL = 'http://m.weibo.cn/p/index?containerid=100103type%3D3%26q%3D{0}%26isv%3D3%26specfilter%3D1%26log_type%3D6&title=%E6%9C%BA%E6%9E%84%E8%AE%A4%E8%AF%81-{0}&uid=5884230638'
AJAX_URL = 'http://m.weibo.cn/page/pageJson?containerid=&containerid=100103type%3D3%26q%3D{0}%26isv%3D3%26specfilter%3D1%26log_type%3D6&title=%E6%9C%BA%E6%9E%84%E8%AE%A4%E8%AF%81-{0}&uid=5884230638&luicode=10000011&lfid=100103type%3D3&v_p=11&ext=&fid=100103type%3D3%26q%3D{0}%26isv%3D3%26specfilter%3D1%26log_type%3D6&uicode=10000011&next_cursor=&page='

WEIBO_URL = 'http://weibo.com/%s/about'
HEADERS = {
    "Host": "weibo.com",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36",
    "Accept-Encoding": "gzip, deflate, sdch",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Cookie": "SINAGLOBAL=6577276759780.943.1453779320693; _s_tentry=www.reader8.cn; YF-Ugrow-G0=57484c7c1ded49566c905773d5d00f82; YF-V5-G0=bc033c7c7d5164aa92fea9d75cc6f127; YF-Page-G0=0dccd34751f5184c59dfe559c12ac40a; Apache=6170847057364.881.1456886840378; ULV=1456886840517:4:1:2:6170847057364.881.1456886840378:1456307239926; wb_feed_unfolded_2264633500=1; wb_feed_unfolded_5296319687=1; login_sid_t=8525d4511d6d138a717e945f20e832bb; wb_publish_vip_2264633500=1; WBtopGlobal_register_version=8a840560e41b693d; un=florent@zunest.com; UOR=www.wooyun.org,widget.weibo.com,www.baidu.com; SUHB=0U1ZtXBIQPyWSa; myuid=5884230638; SUB=_2AkMhrzo1dcNhrAZZkPwXz2vkb4VTgFCt8I-vZxaBEiMLXChJ3xAEx0lqtBN-Xtyh2Ra52xgFC0x8bcKZ4CKXAsxf20h3_GtqdUG8dPkf; SUBP=0033WrSXqPxfM72wWs9jqgMF55529P9D9Wh10cp2_7jHJZ1Ar4Jq1Bgh5JpV8GDQIPLDdJUQdK-7125pSoeVqcv_",
}

SCOPE = '上海'
KEYWORD = '保险'
# change the name to hanyupinyin 汉语拼音 to be the db name
scope = 'shanghai'
keyword = 'insurance'

DB_NAME = 'Companies'
COLLECTION_NAME = '%s_%s' % (scope, keyword)
# COLLECTION_NAME = '%s_%s' % (SCOPE, KEYWORD)
