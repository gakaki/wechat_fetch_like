from pywinauto.application import Application
import pywinauto
import time
import pandas as pd
import json
from pymongo import MongoClient

client          = MongoClient('mongodb://127.0.0.1:27017/')
db              = client['wechat_tmp']
coll_tmp        = db.tmp
coll_wechat     = db['wechat_tuang_tanxianzhe']
coll_error      = db.err
df      = pd.read_excel("C:\\Users\\g\\Desktop\\wechat_like\\途昂 探险者 两辆车微信.xlsx", sheetname=0)
df      = df.fillna('')
rows    = json.loads( df.to_json(orient='records') )

app = Application().Connect(title=u'\u5fae\u4fe1', class_name='WeChatMainWndForPC')
wechatmainwndforpc = app[u'\u5fae\u4fe1']

# todo 位置如果能移动过去 并且要欸次保存下来就好
# 然后复制哪里做成从剪贴板复制黏贴会更好

for row in rows:
    url  = row['url']
    if len(url) <= 0:
        continue
    # 下方发送
    pywinauto.mouse.click(button='left',coords=(574,537))
    #wechatmainwndforpc.SetFocus()
    wechatmainwndforpc.TypeKeys(url)
    time.sleep(0.5)
    wechatmainwndforpc.TypeKeys("{ENTER}")
    time.sleep(0.5)
    pywinauto.mouse.click(button='left', coords=(626,427))

    time.sleep(1) #给fiddler到数据库一些时间
    rows_tmp = list(coll_tmp.find())
    try:
        for row_tmp in rows_tmp:
            if row_tmp['type'] == "like":
                row["read_num"] = -1
                row["like_num"] = -1
                try:
                    o = json.loads(row_tmp['resp'])
                    o = o["appmsgstat"]
                    row["like_num"] = o['like_num']
                    row["read_num"] = o['read_num']
                except:
                    pass

        row['rows'] = rows_tmp
        coll_wechat.insert(row)
        coll_tmp.remove()
        time.sleep(0.5)
    except:
        coll_error.insert(row)
# url_list = [
#     "https://mp.weixin.qq.com/s?__biz=MzI4MjE3MTcwNA==&mid=2664336916&idx=1&sn=af469b7dd8bd3eab7fae0d54ca7319bd&chksm=f0a42e43c7d3a7553b6fd844baf3d08ef901cd5ddbb32661686ec00bed5bc384bcf3dbbba669&scene=0#rd",
#     "https://mp.weixin.qq.com/s?__biz=MzU0NzA4NTM5MQ==&mid=2247484669&idx=1&sn=97a92cd955df21c82ca9a335c9af849a&chksm=fb5289ddcc2500cb8e2bbb15dea1eedacbbd243d0c20ba3f35727205ca161d6554c426877db5&scene=0#rd",
#     "https://mp.weixin.qq.com/s?__biz=MjM5NzA1MTcyMA==&mid=2651165850&idx=1&sn=d6991a284794295f75af570154a3b404&chksm=bd2ed8bd8a5951abbec60ccd6b64f095d0d499e1f839c14188c22fbd1b3a099da85c413f5e6b&scene=0#rd",
#     "https://mp.weixin.qq.com/s?__biz=MzI3MDE0MzAzMw==&mid=2652202241&idx=1&sn=1d458ed521856b131f2c4fa65b2365d3&chksm=f1345e57c643d74165cf8bae5c33e459f6d0e89374e15d1a0215b1760d3218ce8247b0f43117&scene=0#rd"
# ]

# for url in url_list:
#     pywinauto.mouse.click(button='left',coords=(545,528))
#     wechatmainwndforpc.SetFocus()
#     wechatmainwndforpc.TypeKeys(url + "{ENTER}")
#     pywinauto.mouse.click(button='left', coords=(545,437))
#     time.sleep(1.5)
