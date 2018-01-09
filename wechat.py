from pywinauto.application import Application
import pywinauto
import time
import pandas as pd
import json

df      = pd.read_excel("C:\\Users\\g\\Desktop\\wechat_like\\excel.xlsx", sheetname=0)
df      = df.fillna('')
rows    = json.loads( df.to_json(orient='records') )

app = Application().Connect(title=u'\u5fae\u4fe1', class_name='WeChatMainWndForPC')
wechatmainwndforpc = app[u'\u5fae\u4fe1']

for row in rows:
    url  = row['url']
    # 下方发送
    pywinauto.mouse.click(button='left',coords=(532,540))
    #wechatmainwndforpc.SetFocus()
    wechatmainwndforpc.TypeKeys(url + "{ENTER}")
    # 上方点击
    time.sleep(1.5)
    pywinauto.mouse.click(button='left', coords=(645,435))
    


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
