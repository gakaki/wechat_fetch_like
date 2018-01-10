
import time
import pandas as pd
import json
from pymongo import MongoClient

# df      = pd.read_excel("C:\\Users\\g\\Desktop\\wechat_like\\大切诺基 探险者 两辆车微信.xlsx", sheetname=0)
# df      = df.fillna('')
# rows    = json.loads( df.to_json(orient='records') )

client          = MongoClient('mongodb://127.0.0.1:27017/')
db              = client['wechat_tmp']
coll            = db.wechat_tuang_tanxianzhe

cursors        = coll.find()
rows_final     = []
for row in cursors:
    try:
        row['Views'] = row['read_num']
        row['Likes'] = row['like_num']

        del row['read_num']
        del row['like_num']
        del row['rows']
        del row['_id']
        rows_final.append(row)
    except KeyError:
        pass

df     = pd.DataFrame.from_dict( rows_final  )
writer = pd.ExcelWriter('new_small_s_wechat_tuang_tanxianzhe.xlsx')
df.to_excel(writer,'sheet0')
writer.save()

# res_brands      = res_brands + res_brands
# res_brands      = list(set(res_brands))
# df              = pd.DataFrame( res_brands  )

# df.columns   = ["brands"]
# df["brands"].unique()
# writer = pd.ExcelWriter('brands_and_oems.xlsx')
# df.to_excel(writer,'Brands')
# writer.save()


# 福特 探险者 撼路者       wechat_fordtanxianzhehanluzhe 
# 途昂 探险者 两辆车微信   wechat_tuang_tanxianzhe
# 大切诺基 探险者 两辆车微信  wechat_daqietanxianzhe
# 普拉多 探险者 两辆车微信 wechat_pladuotanxian
# 探险者微信 wechat_tanxianzhe
# 途昂单辆车微信文章 wechat_tuang
# prado清理文章的 wechat
