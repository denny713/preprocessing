from flask import Flask, render_template, request, url_for, flash, redirect
from mp_db import dstokopedia, dsbukalapak, dsshopee
from mp_scrapper import tokopedia, bukalapak, shopee

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# tokopedia
@app.route('/tokopedia_scrapper')
def tokopedia_scrapper():
    return render_template('tokopedia_scrapper.html')

@app.route('/dataset_tokopedia')
def dataset_tokopedia():
    tokopedia_koleksi = dstokopedia()
    dataset = tokopedia_koleksi.get_all()
    print(dataset)
    return render_template('tokopedia_dataset.html', dataset = dataset)

@app.route('/tp_total_halaman', methods=['POST'])
def tp_total_halaman():
    if request.method == 'POST':
        cari_apa = request.form['cari']
        if not cari_apa:
            hasil = {'hasil':false, 'pesan':'Jelaskan kamu cari apa bro...'}
        else:
            scrapper = tokopedia()
            # hapus hasil pencarian sebelumnya yang disimpan di tabel agar tidak ada data ganda
            scrapper.delete_pencarian(cari_apa)
            total_halaman = scrapper.total_halaman_pencarian(cari_apa)
            hasil = {'hasil':False, 'pesan':total_halaman}
        # print(hasil)
        return hasil
    
@app.route('/tp_scrap', methods=['POST'])
def tp_scrap():
    if request.method == 'POST':
        kategori = request.form['kategori']
        cari_apa = request.form['cari']
        if not cari_apa:
            hasil = {'hasil':false, 'pesan':'Jelaskan kamu cari apa bro...'}
        else:
            # if int(hal) < 2:
            scrapper = tokopedia()
            # print(cari_apa)
            if (kategori=='toko'):
                # scrapper.cari_toko(cari_apa)
                hasil = scrapper.scrap_toko(cari_apa)
            else:
                hal = request.form['hal']
                # hasil = scrapper.scrap_produk(cari_apa)
                hasil_element_scrap, tp_total_halaman = scrapper.cari_produk(cari_apa, hal)
                hasil = scrapper.scraping(hasil_element_scrap, cari_apa)
            komentar = scrapper.scrap_komentar_hasil_pencarian(hasil)
            print(komentar)
            # scrapper.simpan_ke_tabel(hasil)
            scrapper.simpan_ke_tabel(komentar)
            # else:
                # hasil = 'Salah'
        # print(hasil)
        return komentar

# bukalapak    
@app.route('/bukalapak_scrapper')
def bukalapak_scrapper():
    return render_template('bukalapak_scrapper.html')

@app.route('/dataset_bukalapak')
def dataset_bukalapak():
    bukalapak_koleksi = dsbukalapak()
    dataset = bukalapak_koleksi.get_all()
    print(dataset)
    return render_template('bukalapak_dataset.html', dataset = dataset)

@app.route('/bl_total_halaman', methods=['POST'])
def bl_total_halaman():
    if request.method == 'POST':
        cari_apa = request.form['cari']
        if not cari_apa:
            hasil = {'hasil':false, 'pesan':'Jelaskan kamu cari apa bro...'}
        else:
            scrapper = bukalapak()
            # hapus hasil pencarian sebelumnya yang disimpan di tabel agar tidak ada data ganda
            scrapper.delete_pencarian(cari_apa)
            total_halaman = scrapper.total_halaman_pencarian(cari_apa)
            hasil = {'hasil':False, 'pesan':total_halaman}
        # print(hasil)
        return hasil
    
@app.route('/bl_scrap', methods=['POST'])
def bl_scrap():
    if request.method == 'POST':
        kategori = request.form['kategori']
        cari_apa = request.form['cari']
        if not cari_apa:
            hasil = {'hasil':false, 'pesan':'Jelaskan kamu cari apa bro...'}
        else:
            # if int(hal) < 2:
            scrapper = bukalapak()
            # print(cari_apa)
            if (kategori=='toko'):
                # scrapper.cari_toko(cari_apa)
                hasil = scrapper.scrap_toko(cari_apa)
            else:
                hal = request.form['hal']
                # hasil = scrapper.cari_produk(cari_apa)
                hasil_element_scrap, tp_total_halaman = scrapper.cari_produk(cari_apa, hal)
                hasil = scrapper.scraping(hasil_element_scrap, cari_apa)
            print(hasil)
            komentar = scrapper.scrap_komentar_hasil_pencarian(hasil)
            print(komentar)
            # scrapper.simpan_ke_tabel(hasil)
            scrapper.simpan_ke_tabel(komentar)
            # else:
                # hasil = 'Salah'
        # print(hasil)
        return komentar

# shopee    
@app.route('/shopee_scrapper')
def shopee_scrapper():
    return render_template('shopee_scrapper.html')

@app.route('/dataset_shopee')
def dataset_shopee():
    shopee_koleksi = dsshopee()
    dataset = shopee_koleksi.get_all()
    print(dataset)
    return render_template('shopee_dataset.html', dataset = dataset)

@app.route('/sp_total_halaman', methods=['POST'])
def sp_total_halaman():
    if request.method == 'POST':
        cari_apa = request.form['cari']
        if not cari_apa:
            hasil = {'hasil':false, 'pesan':'Jelaskan kamu cari apa bro...'}
        else:
            scrapper = shopee()
            # hapus hasil pencarian sebelumnya yang disimpan di tabel agar tidak ada data ganda
            scrapper.delete_pencarian(cari_apa)
            total_halaman = scrapper.total_halaman_pencarian(cari_apa)
            hasil = {'hasil':False, 'pesan':total_halaman}
        # print(hasil)
        return hasil
    
@app.route('/sp_scrap', methods=['POST'])
def sp_scrap():
    if request.method == 'POST':
        kategori = request.form['kategori']
        cari_apa = request.form['cari']
        if not cari_apa:
            hasil = {'hasil':false, 'pesan':'Jelaskan kamu cari apa bro...'}
        else:
            # if int(hal) < 2:
            scrapper = shopee()
            # print(cari_apa)
            if (kategori=='toko'):
                # scrapper.cari_toko(cari_apa)
                hasil = scrapper.scrap_toko(cari_apa)
            else:
                hal = request.form['hal']
                # hasil = scrapper.cari_produk(cari_apa)
                hasil_element_scrap, tp_total_halaman = scrapper.cari_produk(cari_apa, hal)
                hasil = scrapper.scraping(hasil_element_scrap, cari_apa)
            print(hasil)
            komentar = scrapper.scrap_komentar_hasil_pencarian(hasil)
            print(komentar)
            # scrapper.simpan_ke_tabel(hasil)
            scrapper.simpan_ke_tabel(komentar)
            # else:
                # hasil = 'Salah'
        # print(hasil)
        return komentar
