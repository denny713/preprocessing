#!/usr/bin/env python
# coding: utf-8

# In[1]:


!pip install wikipedia

# In[2]:


import wikipedia

# In[3]:


def wiki_cari(kata):
  return wikipedia.summary(kata, auto_suggest = False)

# In[4]:


def wiki_search(kata, rs=20):
  return wikipedia.search(kata, results=rs)

# In[5]:


def wiki_url(kata):
  return wikipedia.WikipediaPage(kata).url

# In[6]:


import json
def wiki_json(data):
  return json.dumps(data)

# In[7]:


!pip install openpyxl

# In[8]:


import pandas as pd
import openpyxl

def wiki_excel(data):
  df=pd.DataFrame(data)
  return df.to_excel("data-wiki.xlsx")

# In[9]:


!pip install pymongo dnspython

# In[10]:


from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://SERVER/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Menghubungi database, berhasil terkoneksi ke MongoDB!")
except Exception as e:
    print(e)

# In[ ]:


dbs = client.list_database_names()
print(dbs)

# In[ ]:


import pymongo
import sys

db = client.salimWiki
my_collection = db["wiki_laman_deskripsi"]


# In[ ]:


#skip

datam = []
carim=wiki_search(cari)
for mn in range(len(carim)):
  itemm = {"ids": carim[mn], "ringkasan": wiki_cari(carim[mn])}
  datam.append(itemm)
print(datam)
#wiki_mongo(datam)

# In[ ]:


#skip

#df=pd.DataFrame(datam)
try:
  result = my_collection.insert_many(datam)

# return a friendly error if the operation fails
except pymongo.errors.OperationFailure:
  print("An authentication error was received. Are you sure your database user is authorized to perform write operations?")
  sys.exit(1)
else:
  inserted_count = len(result.inserted_ids)
  print("I inserted %x documents." %(inserted_count))

  print("\n")

# In[ ]:


dbs = client.list_database_names()
print(dbs)

# In[ ]:


myDB = client["salimWiki"]
print(myDB.list_collection_names())

# In[ ]:


collectionDB = myDB["wiki_laman_deskripsi"]

result = collectionDB.find()

if result:
  for doc in result:
    id = doc['ids']
    name = doc['ringkasan']
    print("%s - : %s." %(id,name))

else:
  print("Dokumen tidak ditemukan.")

print("\n")


# In[ ]:


def main():
    global cari
    # print your menu here
    selection = input('\nPilihan Anda : ')
    try:
       selection = int(selection)
    except ValueError:
       print('Maaf, "',format(selection),'" tidak ada pada daftar pilihan yang disediakan.')
       main()
    if selection == 1:
      cari = input('Cari : ')

    if selection == 2:
      print ("Cari di Wikipedia: "+cari)
      print ("URL: "+wiki_url(cari))
      print ("Ringkasan: "+wiki_cari(cari))
      print ("\nBahasan yang mirip: ")
      carimi=wiki_search(cari)
      print (carimi)
      for cm in range(len(carimi)):
        print(str(cm)+" "+carimi[cm])

    if selection == 3:
      data = []
      carijs=wiki_search(cari)
      for cj in range(len(carijs)):
        item = {"ids": carijs[cj], "ringkasan": wiki_cari(carijs[cj])}
        data.append(item)
      print(wiki_json(data))

    if selection == 4:
      datax = []
      carixl=wiki_search(cari)
      for xl in range(len(carixl)):
        itemx = {"ids": carixl[xl], "ringkasan": wiki_cari(carixl[xl])}
        datax.append(itemx)
      wiki_excel(datax)

    if selection == 9:
       exit_check = input('Ketik "ya" untuk keluar : ')
       return exit_check.lower()
    return selection

# In[ ]:


print ("Menu: \n 1. Masukkan kata yang dicari\n 2. Cari di Wikipedia\n 3. Konversi ke JSON\n 4. Konversi ke Excel\n 9. Keluar")
selesai = main()
while selesai != 'ya':
  pil = (1,2,3,4)
  if selesai in pil:
    selesai = main()
print('Terimakasih..')

# In[ ]:



