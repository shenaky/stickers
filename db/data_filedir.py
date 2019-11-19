# -*- coding:utf-8 -*-
import json
import os
import re
path='../ChineseBQB'
list = []
for name in os.listdir(path):
    dict = {}
    pattern = re.compile('[\u4e00-\u9fa5]+')
    m = pattern.search(name)
    dict['folder'] = name
    dict['category'] = m.group(0)
    memelist = []
    for memeName in os.listdir(os.path.join(path, name)):
        memelist.append(memeName)
    dict['meme'] = memelist
    list.append(dict)
print(json.dumps(list,ensure_ascii=False,indent=4))

print(len(list))
# Writing JSON data
with open('data.json', 'w') as f:
    json.dump(list, f, ensure_ascii=False, indent=4)
# encode('utf-8')
# # Reading data back
# with open('data.json', 'r') as f:
#     data = json.load(f)

with open('data.json', 'r') as f:
    data = json.load(f)
print('btrshy')
print(list[34])


 
