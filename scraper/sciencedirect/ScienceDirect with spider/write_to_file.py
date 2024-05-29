#conding:utf8



class Write_to_file(object):
    def __init__(self):
        self.ok = 'ok'

    def write_to_txt(self, KeyWords,count,title_en,abstract_en,title_cn,abstract_cn,new_url):

        filename = '.\\Data_tommy\\' + KeyWords + '\\' + KeyWords + '.txt'

        # open a file
        file_txt = open(filename, 'a', encoding='utf8')

        # Write the list to a txt file 
        file_txt.write('【' + str(count) + '】:  '
                       'title: '+ title_en + '\n'
                        'Title: ' + title_cn + '\n'
                       'abstract: ' + abstract_en + '\n'
                       'Abstract: '+ abstract_cn + '\n'
                       'Link:' + new_url + '\n\n')