# weibo_wechat_accounts_spider
two spiders to search wechat offical accounts and weibo users,with a controller excepted keywords
## **Start all spiders with keyword**

**modify the keyword in spider_controller.py and run it.**

you can input or use command arguments to start spider, easy to change.
all the data will store in the mongodb, the collection name generated according to the keywords you give.

## **Start weibo spider**
no money for using CAPTCHA api, so I turn to crawl the mobile web version of weibo, all you need is changing the cookie every two or three days, in my own experience, I don't update cookie for three days but still working well.
for now it will crawl weibo authenticated companies users,you can modify by changing the url in settings.py

**example: python mobile_weibo/run.py Elon Musk SPACE X**

the keyword will be 'Elon Musk SPACE X' to search

## **Start wechat spider**
the spider will grab data from sougou_wechat_search
http://weixin.sogou.com/ ,all info data will be store in the mongodb and the QR code stored as a bson object.

usage: same as the weibo spider

**example: python wechat/run.py Elon Musk SPACE X**

##**Requirements**
all the python lib you need to run the spider are requests,lxml,pymongo,and concurrent.futures(threadpool for weibo)

##**#TODO**
1. I used concurrent.futures in wechat spider,but threadpool in the weibo spider, should be replaced by concurrent.futures
2. wechat spider sometimes need to input CAPTCHA manually,web CAPTCHA api is a good choice when I got money.
3. the db module should be separated from the system when I got time.
4. weibo spider need refactor, I wrote that long time ago,now it looks shit.