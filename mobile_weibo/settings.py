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
# These two url are for verified companies.
FIRST_PAGE_URL = u'http://m.weibo.cn/p/index?containerid=100103type%3D3%26q%3D{0}%26isv%3D3%26specfilter%3D1%26log_type%3D6&title=%E6%9C%BA%E6%9E%84%E8%AE%A4%E8%AF%81-{0}&uid=5884230638'
AJAX_URL = u'http://m.weibo.cn/page/pageJson?containerid=&containerid=100103type%3D3%26q%3D{0}%26isv%3D3%26specfilter%3D1%26log_type%3D6&title=%E6%9C%BA%E6%9E%84%E8%AE%A4%E8%AF%81-{0}&uid=5884230638&luicode=10000011&lfid=100103type%3D39%26q%3D{0}%26t%3D&v_p=11&ext=&fid=100103type%3D3%26q%3D{0}%26isv%3D3%26specfilter%3D1%26log_type%3D6&uicode=10000011&next_cursor=&page='

# These for all users of weibo no matter verified or not.
FIRST_PAGE_URL_ALL_USER = u'http://m.weibo.cn/main/pages/index?containerid=100103type%3D3%26q%3D{0}&type=user&queryVal={0}&luicode=10000011&lfid=100103type%3D3%26q%3D{0}&title={0}'
AJAX_URL_ALL_USER = u'http://m.weibo.cn/page/pageJson?containerid=&containerid=100103type%3D3%26q%3D{0}&type=user&queryVal={0}&luicode=10000011&lfid=100103type%3D3%26q%3D{0}&title={0}&v_p=11&ext=&fid=100103type%3D3%26q%3D{0}&uicode=10000011&next_cursor=&page='

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
    "Cookie": "SINAGLOBAL=1213665334507.823.1458891315810; YF-Page-G0=23b9d9eac864b0d725a27007679967df; _s_tentry=-; Apache=196413819212.4665.1460440366645; ULV=1460440366722:2:1:1:196413819212.4665.1460440366645:1458891315854; YF-V5-G0=572595c78566a84019ac3c65c1e95574; SUB=_2A256E1A5DeTxGeNG41YT8y7KyDSIHXVZacbxrDV8PUJbstBeLWXFkW9LHeuaj4uwneZcpk6zvceMs-b0PG4CsQ..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh10cp2_7jHJZ1Ar4Jq1Bgh5JpX5o2p; SUHB=0xnSua6Qdn0kHM; SSOLoginState=1461133417"
}

SCOPE = '上海'
KEYWORD = '保险'
# change the name to hanyupinyin 汉语拼音 to be the db name
scope = 'shanghai'
keyword = 'insurance'

DB_NAME = 'Companies'
COLLECTION_NAME = '%s_%s' % (scope, keyword)
# COLLECTION_NAME = '%s_%s' % (SCOPE, KEYWORD)
# 1 for verified companies, 2 for all weibo accounts no matter verified or not
SEARCH_TYPE = 2
