#!/usr/bin/env python
# coding: utf-8

# In[4]:


!pip install pymongo dnspython

# In[5]:


!pip install Json2Excel

# In[6]:


!pip install xlsxwriter

# In[7]:


import pymongo
from pymongo import MongoClient
from pymongo.server_api import ServerApi

from json2excel import Json2Excel
import pandas as pd
import json
from bson.objectid import ObjectId
from bson import json_util

client = pymongo.MongoClient("mongodb+srv://SERVER/?retryWrites=true&w=majority", server_api=ServerApi('1'))
# Database Name
db = client["salimWiki"]
# Collection Name
col = db["wiki_laman_judul"]
#  Find All: It works like Select * query  of SQL.
x = col.find()
list_01 = []
for data in x:
    list_01.append(data)
#    print(data)


print("= = = = = ")
df = pd.DataFrame(data,index=[0])

# select two columns
for y in df:
    print(y)

print("= = = = = ")
print(type(list_01))


print(list_01)
df = pd.DataFrame(list_01)
writer = pd.ExcelWriter('test10.24.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='welcome', index=False)
writer.save()

# In[ ]:


# Collection Name
col = db["wiki_laman_deskripsi"]
#  Find All: It works like Select * query  of SQL.
x = col.find()
list_01 = []
for data in x:
    list_01.append(data)
#    print(data)


print("= = = = = ")
df = pd.DataFrame(data,index=[0])

# select two columns
for y in df:
    print(y)

print("= = = = = ")
print(type(list_01))


print(list_01)
df = pd.DataFrame(list_01)
writer = pd.ExcelWriter('wiki_laman_deskripsi.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='welcome', index=False)
writer.save()
