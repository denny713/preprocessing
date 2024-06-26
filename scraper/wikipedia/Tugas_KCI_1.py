#!/usr/bin/env python
# coding: utf-8

# #Tugas Matakuliah Komputer Cerdas Interaktif
# 
# Salim Athari

# ##Memanggil Paket dan penggunaannya
# - Memanggil paket library yang akan digunakan, dalam hal ini paket **json** dan **urllib.request**
# - Menggunakan paket untuk mengambil konten dari alamat API Bahasa pada wikipedia yang tersedia
# - Mengubah format data menjadi json menggunakan paket yang sebelumnya sudah dipanggil

# In[25]:


import json,urllib.request

url = "https://commons.wikimedia.org/w/api.php?action=sitematrix&smtype=language&format=json"
data = urllib.request.urlopen(url).read()
output = json.loads(data)

# ##Proses pencarian semua Bahasa yang tersedia di Wikipedia
# - Melakukan pencarian nama Bahasa tertentu dari hasil API Bahasa pada wikipedia
# - Menampilkan data sesuai pilihan, semua untuk menampilkan semua data atau sesuai kata yang dimasukkan
# - Melakukan pencarian halaman dari wikipedia sesuai kode yang dimasukkan
# - Menampilkan hasil pencarian secara raw maupun beutify

# In[34]:


cari = input('Cari Bahasa (Masukkan kata / ketik "semua" untuk menampilkan semua): ')

jdt = 0
print('\n')
print('\033[1m','Kode\t: Nama Bahasa\t: Nama Latin','\033[0m')
print('------------------------------------')
for element in output['sitematrix']:
  lang = output['sitematrix'][element]
  if element!='count':
    if cari.lower() == 'semua':
      print(lang['code'],'\t: ',lang['name'],'\t: ',lang['localname'])
    elif cari.lower() in lang['name'].lower():
      print(lang['code'],'\t: ',lang['name'],'\t: ',lang['localname'])
      jdt += 1

#print(jdt)
if jdt>0:
  idlang = input('\nMasukkan kode: ')
  urlp = "https://"+idlang+".wikipedia.org/w/api.php?action=query&format=json&list=allpages&aplimit=500"
  #print(urlp)

  datap = urllib.request.urlopen(urlp).read()
  outputp = json.loads(datap)
  fortam = input('\nFormat (raw/json)?: ')
  if fortam=='raw':
    print (outputp)
  elif fortam=='json':
    print (json.dumps(outputp, indent=4))


# ##Pengambilan judul laman wikipedia
# - Menggunakan tautan sebelumnya dan menambahkan parameter **continue** untuk mendapatkan laman berikutnya

# In[35]:


urld = urlp

neks = True
i = 1
while neks:
  print(i)
  i += 1
  if i>100:
    neks = False

  datap = urllib.request.urlopen(urlp).read()
  outputp = json.loads(datap)

  if 'continue' in outputp:
    urlt = "&apfrom="+urllib.parse.quote(outputp['continue']['apcontinue'])
    urlp = urld+urlt
    print ('url: ',urlp)
    print ('continue: ',outputp['continue']['apcontinue'])

  if 'continue' not in outputp:
    print ('stop: ',outputp)
    neks = False


# - Simpan hasil dari pencarian berdasar kata tertentu
# - Pilih bahasa sebelum melakukan pencarian
