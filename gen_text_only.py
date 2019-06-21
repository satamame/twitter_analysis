#%%
"""
gen_text_only.py
サンプルツイートを元に、id と full_text だけの Collection を作る。
full_text が重複しないように作る。
"""

#%%

from pymongo import MongoClient

# データベースの準備
client = MongoClient()
col_twsamples = client.tw_ana.tw_samples
col_text = client.tw_ana.tw_text

cnt = 0
add = 0
for t in col_twsamples.find({}, {'id': 1, 'full_text': 1}, no_cursor_timeout=True):
    id = t['id']
    text = t['full_text']
    if col_text.count_documents({'full_text': text}) < 1:
        col_text.insert_one({'id': id, 'full_text': text})
        add += 1
    
    cnt += 1
    if cnt % 1000 == 0:
        print('{} processed, {} added.'.format(cnt, add))

#%%

print('Done.')
cnt_txt = col_text.count_documents({})
print('Totally {} tweets are in text-only Collection.'.format(cnt_txt))


#%%
