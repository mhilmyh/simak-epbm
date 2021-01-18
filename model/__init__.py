import requests
from bs4 import BeautifulSoup
from random import randint


class Robot:
    base_url = 'https://simak.ipb.ac.id'
    authenticated = False

    def __init__(self, username, password):
        ''' Inisiasi Robot penelusur '''
        self.username = username
        self.password = password
        self.list_matkul = {}
        self.request = None
        self.response = None
        self.url_found = {}
        self.cookie_jar = {}
        self.headers = requests.utils.default_headers()
        self.headers.update({
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Mobile Safari/537.36',
        })
        self.soup = None
        print(f'\033[32mBeep boop ! robot untuk {username} siap\33[0m')

    def login(self, method='GET'):
        ''' Method untuk request ke login page'''
        login_url = self.base_url + '/Account/Login'
        if method == 'POST_LOGIN':
            data = self._construct_login_data()
            self._do_request(login_url, method, data)
        else:
            self._do_request(login_url, method)

    def sidebar(self):
        ''' Method melihat menu pada sidebar '''
        if self.authenticated == False:
            raise RuntimeError('\033[31mBzzz bzzz ! anda belum login\33[0m')

        menu = self.soup.select('ul.sidebar-menu > li > a')
        print('Memberikan hasil pencarian menu sidebar: ')
        for element in menu:
            self.url_found[element.contents[1].strip()] = element['href']
            print(
                f'Halaman :{element.contents[1]} ({self.base_url+element["href"]})')
        return menu

    def goto_page(self, page_name='Beranda'):
        ''' Method pindah halaman '''
        if not (page_name in self.url_found):
            raise ValueError(
                '\033[31mBzzz bzzz ! nama halaman sepertinya salah atau belum ditemukan\33[0m')

        if self.authenticated == False:
            raise RuntimeError('\033[31mBzzz bzzz ! anda belum login\33[0m')

        self._do_request(url=self.base_url + self.url_found[page_name])

    def get_list_epbm(self):
        ''' Method melihat list epbm '''
        if self.response.url == self.url_found.get('EPBM'):
            raise ValueError(
                '\033[31mBzzz bzzz ! anda tidak berapa di halaman EPBM\33[0m')

        if self.authenticated == False:
            raise RuntimeError('\033[31mBzzz bzzz ! anda belum login\33[0m')

        tags = self.soup.select(
            'div.box-body > div.row > div.col-md-6 > a')
        print('Memberikan hasil matakuliah yang belum diisi EPBM nya :')
        for tag in tags:
            link = tag['href']
            name = tag.select(
                'div.panel-danger > div.panel-heading > table > tr > td > table > tr > td > font')
            if name:
                print(name)
                self.list_matkul[name[0].string] = link
                print(f'{name[0].string}: {self.base_url + link}')

        if not self.list_matkul:
            print(
                f'\033[33mDrrt drrt ! tidak bisa menemukan EPBM yang belum terisi\33[0m')
        return self.list_matkul

    def find_and_click_epbm_button(self):
        a = self.soup.select_one('a.btn.btn-primary')
        url = self.base_url + a['href']
        self._do_request(url)

    def fill_epbm(self, kode_matkul=None):
        ''' Method mengisi epbm '''
        if kode_matkul is None:
            raise ValueError('\033[31mBzzz bzzz ! kode matkul salah\33[0m')

        if self.authenticated == False:
            raise RuntimeError('\033[31mBzzz bzzz ! anda belum login\33[0m')

        yakin = input(
            f'\033[32mBeep boop ! apa anda yakin mengisi epbm {kode_matkul} ? (y/n) \33[0m')
        if yakin == 'y':
            self._do_request(self.base_url + self.list_matkul[kode_matkul])
            data = self._construct_epbm_data()
            print('Form yang akan dikirim : ', end='')
            print(' | '.join(map(str, data.keys())))
            self._do_request(
                self.base_url + self.list_matkul[kode_matkul], method='POST_EPBM', data=data)
        elif yakin == 'n':
            print(f'\033[33mDrrt drrt ! batal mengisi {kode_matkul}\33[0m')
        else:
            raise ValueError(
                '\033[31mBzzz bzzz ! tidak bisa memahami input\33[0m')

    def _do_request(self, url='', method='GET', data={}):
        ''' Method untuk membuat request '''
        dont_print = False
        if self.response is not None:
            for cookie in self.response.cookies:
                self.cookie_jar[cookie.name] = cookie.value

        print(f'Mencoba melakukan {method} ke alamat : {url}')
        with requests.Session() as sess:
            if method == 'POST_LOGIN':
                self.response = sess.post(
                    url, data=data, cookies=self.cookie_jar, allow_redirects=False)
                if self.response.status_code == 302:
                    print('\033[32mBeep boop ! berhasil login\33[0m')
                    self.authenticated = True
                    dont_print = True
                    self._do_request(self.base_url + '/Home')
                else:
                    print('\033[31mBzzz bzzz ! sepertinya gagal login\33[0m')
            elif method == 'POST_EPBM':
                self.response = sess.post(
                    url, data=data, cookies=self.cookie_jar)
                soup_tmp = BeautifulSoup(self.response.content, 'html.parser')
                alert = soup_tmp.select_one('div.alert')
                print(
                    f'\033[33mDrrt drrt ! {str(alert.contents[-1]).strip()}\33[0m')
            else:
                self.response = sess.get(url, cookies=self.cookie_jar)

            self.soup = BeautifulSoup(self.response.content, 'html.parser')
            self.request = self.response.request
        if not dont_print:
            print(
                f'\033[32mBeep boop ! sekarang anda berada di {self.response.url}\33[0m')

    def _construct_login_data(self):
        ''' Method untuk membangun data login '''
        if self.soup is not None:
            token_tag = self.soup.select_one(
                'input[name="__RequestVerificationToken"]')['value']
            d = {}
            for input_tag in self.soup.find_all('input'):
                if input_tag['name'] == '__RequestVerificationToken':
                    d['__RequestVerificationToken'] = token_tag
                elif input_tag['name'] == 'UserName':
                    d['UserName'] = self.username
                elif input_tag['name'] == 'Password':
                    d['Password'] = self.password
                else:
                    d[input_tag['name']] = input_tag['value']
            return d

        else:
            raise RuntimeError(
                '\033[31mBzzz bzzz ! hasil soup tidak ditemukan\33[0m')

    def _construct_epbm_data(self):
        krsid = self.soup.select_one('input[name="KRSID"]')
        pengaturan_jadwal_sistem = self.soup.select_one(
            'input[name="PengaturanJadwalSistemID"]')

        hitung_p_mk = self.soup.select_one('input[name^="HitungPertanyaanMK"]')
        hitung_p_dosen = self.soup.select(
            'input[name^="HitungPertanyaanDosen"]')
        jumlah_dosen = self.soup.select_one(
            'input[name="HitungDosenRealisasi"]')
        list_id_dosen = self.soup.select('input[name^="PengajarMKID"]')

        data = {
            krsid['name']: krsid['value'],
            pengaturan_jadwal_sistem['name']: pengaturan_jadwal_sistem['value']
        }

        for i in range(1, int(hitung_p_mk['value']) + 1):
            data['Jawaban_' + str(i)] = randint(3, 4)
        data[hitung_p_mk['name']] = hitung_p_mk['value']

        for i in range(int(jumlah_dosen['value'])):
            data[list_id_dosen[i]['name']] = list_id_dosen[i]['value']
            for j in range(int(hitung_p_dosen[i]['value'])):
                data['JawabanDosen_' + str(i + 1) + str(j + 1)] = randint(3, 4)
            data[hitung_p_dosen[i]['name']] = hitung_p_dosen[i]['value']
        data[jumlah_dosen['name']] = jumlah_dosen['value']
        data['Saran'] = ''
        data['Pernyataan'] = ['true', 'false']

        return data
