import os
import re

import neattext.functions as nfx
import pandas as pd
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from flask import Flask, render_template, request, redirect, Response, flash
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='assets', template_folder='templates')
app.debug = True
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
stemmer = StemmerFactory().create_stemmer()

# Lokasi upload folder
ALLOWED_EXTENSION = set(['csv'])
app.config['UPLOAD_FOLDER'] = 'uploads'


# Allowed filename
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION


filename = str
nm_kol = str
home = bool
index_kol = int
raw_text = pd.Series()
processed_text = pd.Series()
options = pd.Series()
preprocess_options = []
folderpath = app.root_path + "/uploads/"
previewindex = 20


# Route ke halaman preprocessing
@app.route('/')
def index():
    global folderpath
    global home

    home = True

    if os.path.exists(folderpath):
        files = os.listdir(folderpath)
        for file in files:
            filepath = os.path.join(folderpath, file)
            if os.path.isfile(filepath):
                try:
                    os.remove(filepath)
                except OSError as e:
                    flash('Data kosong', 'warning')

    return render_template('home.html')


# Route fungsi upload
@app.route('/uploader', methods=['GET', 'POST'])
def upload():
    global home
    global filename
    global options
    global folderpath

    if os.path.exists(folderpath):
        files = os.listdir(folderpath)
        for file in files:
            filepath = os.path.join(folderpath, file)
            if os.path.isfile(filepath):
                try:
                    os.remove(filepath)
                except OSError as e:
                    flash('Data kosong', 'warning')

    # Jika ada aksi POST
    if 'file_csv' in request.files:
        file = request.files['file_csv']

        # Cek apakah file sudah terupload
        if 'file_csv' not in request.files:
            flash('Tidak ada file yang diupload', 'warning')
            return redirect(request.url)

        # Cek apakah nama file tidak kosong
        if file.filename == '':
            flash('Tidak ada file yang diupload', 'warning')
            return redirect(request.url)

        # Cek apakah ekstensi sudah benar
        if not allowed_file(file.filename):
            flash('File harus berformat CSV', 'warning')
            return redirect(request.url)

        # Jika ekstensi file sudah benar
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.root_path + "/uploads/", filename))
            df = pd.read_csv(app.root_path + "/uploads/" + filename, encoding='latin1', on_bad_lines='skip')

            options = pd.Series(df.columns)
            options = [x for x in options.str.split(';')[0]]

            if home == True:
                return render_template(
                    "home.html",
                    options=options,
                    show_kolom=True)
            else:
                return render_template(
                    "prepro.html",
                    options=options,
                    show_kolom=True)
    if home == True:
        return render_template('home.html')
    else:
        return render_template('prepro.html')


@app.route("/selector", methods=['GET', 'POST'])
def select():
    global home
    global filename
    global options
    global index_kol
    global nm_kol
    global raw_text
    global raw_text_preview
    global processed_text

    home = False

    index_kol = int(request.form['column_name'])
    df = pd.read_csv(app.root_path + "/uploads/" + filename, encoding='latin1', sep=';')

    # try:
    #     df = pd.read_csv("uploads/" + filename, encoding='utf-8', sep=';', on_bad_lines='skip', header=None)
    # except pd.errors.ParserError:
    #     df = pd.read_csv("uploads/" + filename, encoding='utf-8', sep=',', on_bad_lines='skip', header=None)

    raw_text = df.iloc[:, index_kol].dropna()
    nm_kol = options[index_kol]

    if raw_text.empty:
        flash('Data kosong', 'warning')
        return render_template(
            "prepro.html",
            options=options,
            show_kolom=True)

    else:
        processed_text = raw_text

        raw_text_preview = []
        for i, row in enumerate(raw_text):
            if i < previewindex:
                raw_text_preview.append(row)
            else:
                break
        processed_text_preview = raw_text_preview

        return render_template(
            "prepro.html",
            nm_kol=nm_kol,
            tabledata1=raw_text_preview,
            tabledata2=processed_text_preview,
            datacount1=len(raw_text),
            datacount2=len(processed_text),
            options=options,
            show_kolom=True,
            show_table=True)


@app.route('/preprocessing', methods=['GET', 'POST'])
def preprocessing():
    preprocess_options = []
    global processed_text
    processed_text = raw_text

    for option in request.form.getlist('preprocess_checkbox'):
        if option not in preprocess_options:
            preprocess_options.append(option)
        else:
            preprocess_options.remove(option)

    # Remove username
    if 'remove_username' in preprocess_options:
        def users(text):
            text = nfx.remove_userhandles(text)
            return text

        processed_text = processed_text.apply(users)

    # Remove retweet
    if 'remove_rt' in preprocess_options:
        def rt(text):
            text = re.sub(r'^RT[\s]+', '', text)
            return text

        processed_text = processed_text.apply(rt)

    # Remove hashtag
    if 'remove_hashtag' in preprocess_options:
        def hastag(text):
            text = nfx.remove_hashtags(text)
            return text

        processed_text = processed_text.apply(hastag)

    # Remove url
    if 'remove_url' in preprocess_options:
        def urls(text):
            text = nfx.remove_urls(text)
            text = re.sub(r'https?:\/\/.[\r\n]', '', text)
            text = re.sub(r'http\S+', '', text)
            text = re.sub(r'\bhttp\b', '', text)
            text = re.sub(r'www.\S+', '', text)
            text = re.sub(r'\S+.com', '', text)
            text = re.sub(r'\S+.net', '', text)
            text = re.sub(r'\S+.org', '', text)
            return text

        processed_text = processed_text.apply(urls)

    # Remove punctuation
    if 'remove_punctuation' in preprocess_options:
        def remove_punctuations(text):
            punct = '''.,;:-?!'"()[]/`_'''
            pattern = f'[{re.escape(punct)}]'
            text = re.sub(pattern, '', text)
            return text

        processed_text = processed_text.apply(remove_punctuations)

    # Remove symbol
    if 'remove_symbol' in preprocess_options:
        def remove_symbols(text):
            punct = '''.,;:-?!'"()[]/`_'''
            pattern = rf'[^\w\s{re.escape(punct)}]'
            text = re.sub(pattern, '', text)
            return text

        processed_text = processed_text.apply(remove_symbols)

    # Remove number
    if 'remove_number' in preprocess_options:
        def remove_numbers(text):
            pattern = r'\d+'
            text = re.sub(pattern, '', text)
            return text

        processed_text = processed_text.apply(remove_numbers)

    # Remove duplicate
    if 'remove_duplicate' in preprocess_options:
        Y = processed_text
        Y = Y.drop_duplicates(keep='first')
        processed_text = Y

    # Replace slang
    if 'replace_slang' in preprocess_options:
        def r_slang(text):

            # Membaca dataset dari file menggunakan pandas
            slang_dataset = pd.read_csv(app.root_path + '/assets/slang_dataset.csv', delimiter=';',
                                        names=['slang', 'replacement'])
            slang_dict = dict(zip(slang_dataset['slang'], slang_dataset['replacement']))
            words = text.split()
            replaced_words = []

            for word in words:
                replacement = slang_dict.get(word)
                if replacement is not None:
                    replaced_words.append(replacement)
                else:
                    replaced_words.append(word)
            replaced_text = ' '.join(replaced_words)
            return replaced_text

        processed_text = processed_text.apply(r_slang)

    # Replace abbreviation
    if 'replace_abbreviation' in preprocess_options:
        def r_abbre(text):

            # Membaca dataset dari file menggunakan pandas
            abbre_dataset = pd.read_csv(app.root_path + '/assets/abbre_dataset.csv', delimiter=' = ',
                                        names=['abbre', 'replacement'])
            abbre_dict = dict(zip(abbre_dataset['abbre'], abbre_dataset['replacement']))
            words = text.split()
            replaced_words = []

            for word in words:
                replacement = abbre_dict.get(word)
                if replacement is not None:
                    replaced_words.append(replacement)
                else:
                    replaced_words.append(word)
            replaced_text = ' '.join(replaced_words)
            return replaced_text

        processed_text = processed_text.apply(r_abbre)

    # Replace elongated character
    if 'replace_elochar' in preprocess_options:
        def replace_elongated_characters(text):
            elochart_data = pd.read_csv(app.root_path + '/assets/elochar_dataset.csv', names=['elochar'])
            elochar_list = elochart_data['elochar'].tolist()
            elochar_dict = {word.lower(): None for word in elochar_list}
            words = text.split()
            processed_words = []

            for word in words:
                found = False
                for key in elochar_dict.keys():
                    if key in word.lower():
                        found = True
                        break
                if found:
                    processed_words.append(word)
                else:
                    pattern = re.compile(r'(\w)\1+')
                    replaced_word = re.sub(pattern, r'\1', word)
                    processed_words.append(replaced_word)

            processed_text = ' '.join(processed_words)
            return processed_text

        processed_text = processed_text.apply(replace_elongated_characters)

    # Lower case
    if 'lower_case' in preprocess_options:
        def c_folding(text):
            text = text.lower()
            return text

        processed_text = processed_text.apply(c_folding)

    # Remove stopword
    if 'remove_stopword' in preprocess_options:
        def remove_stopwords(text):
            if type(text) == list:
                stop_words = set(stopwords.words('indonesian'))
                filtered_words = [word for word in text if word.lower() not in stop_words]
                result = filtered_words
            else:
                text = text.split()
                stop_words = set(stopwords.words('indonesian'))
                filtered_words = [word for word in text if word.lower() not in stop_words]
                result = ' '.join(filtered_words)
            return result

        processed_text = processed_text.apply(remove_stopwords)

    # Stemming
    if 'stemming' in preprocess_options:
        def stem_text(text):
            stemmed_text = stemmer.stem(text)
            return stemmed_text

        processed_text = processed_text.apply(stem_text)

    # Join case
    if 'join_case' in preprocess_options:
        def joincase(text):
            if type(text) == list:
                text = ''.join(text)
                text = [text]
            else:
                text = text.replace(" ", "")
            return text

        processed_text = processed_text.apply(joincase)

    # Tokenize
    if 'tokenizing' in preprocess_options:
        def Tokenize(text):
            tokens = word_tokenize(text)
            return tokens

        processed_text = processed_text.apply(Tokenize)

    processed_text_preview = []
    for i, row in enumerate(processed_text):
        if i < previewindex:
            processed_text_preview.append(row)
        else:
            break

    return render_template(
        'prepro.html',
        nm_kol=nm_kol,
        tabledata1=raw_text_preview,
        tabledata2=processed_text_preview,
        datacount1=len(raw_text),
        datacount2=len(processed_text),
        preprocess_options=preprocess_options,
        options=options,
        show_kolom=True,
        show_table=True)


@app.route('/reset', methods=['GET', 'POST'])
def reset():
    global processed_text
    preprocess_options.clear
    processed_text = raw_text
    processed_text_preview = raw_text_preview

    return render_template(
        'prepro.html',
        nm_kol=nm_kol,
        tabledata1=raw_text_preview,
        tabledata2=processed_text_preview,
        datacount1=len(raw_text),
        datacount2=len(processed_text),
        preprocess_options=preprocess_options,
        options=options,
        show_kolom=True,
        show_table=True)


@app.route('/downloader', methods=['GET', 'POST'])
def download():
    data = processed_text
    csv_data = data.to_csv(header=True, index=False)

    return Response(
        csv_data,
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment;filename=data_series.csv'}
    )


# Fungsi debuging
if __name__ == '__main__':
    app.run(debug=True)
