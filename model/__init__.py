import requests
from bs4 import BeautifulSoup


class Robot:
    base_url = 'https://simak.ipb.ac.id'
    authenticated = False

    def __init__(self, username, password):
        ''' Inisiasi Robot penelusur '''
        self.username = username
        self.password = password
        self.request = None
        self.response = None
        self.url_found = {}
        self.soup = None
        print(f'\033[32mBeep boop ! robot untuk {username} siap\33[0m')

    def login(self, method='GET'):
        ''' Method untuk request ke login page'''
        login_url = self.base_url + '/Account/Login'
        if method == 'POST_LOGIN':
            # param = '?ReturnUrl=%2FHome'
            data = self._construct_login_data()
            self._do_request(login_url, method, data)
        else:
            self._do_request(login_url, method)

    def list_sidebar(self):
        ''' Method melihat menu pada sidebar '''
        if self.authenticated == False:
            raise RuntimeError('\033[31mBzzz bzzz ! anda belum login\33[0m')

        menu = self.soup.select('ul.sidebar-menu > li > a')
        print('Memberikan hasil pencarian menu sidebar: ')
        for element in menu:
            self.url_found[element.contents[1].strip()] = element["href"]
            print(
                f'Halaman :{element.contents[1]} ({self.base_url+element["href"]})')
        return menu

    def goto_page(self, page_name='Beranda'):
        if not (page_name in self.url_found):
            raise ValueError(
                '\033[31mBzzz bzzz ! nama halaman sepertinya salah\33[0m')

        if self.authenticated == False:
            raise RuntimeError('\033[31mBzzz bzzz ! anda belum login\33[0m')

        print(f'Mencoba pindah ke {page_name} : {self.url_found[page_name]}')
        self._do_request(url=self.base_url + self.url_found[page_name])

    def _do_request(self, url='', method='GET', data={}):
        ''' Method untuk membuat request '''
        cookies = {}
        if self.response is not None:
            for cookie in self.response.cookies:
                cookies[cookie.name] = cookie.value

        print(f'Mencoba melakukan {method} ke alamat : {url}')
        with requests.Session() as sess:
            if method == 'POST_LOGIN':
                self.response = sess.post(
                    url, data=data, cookies=cookies, allow_redirects=False)
                if self.response.status_code == 302:
                    print('\033[32mBeep boop ! berhasil login\33[0m')
                    self.authenticated = True
                    self._do_request(self.base_url + '/Home')
                else:
                    print('\033[31mBzzz bzzz ! sepertinya gagal login\33[0m')
            else:
                self.response = sess.get(url, cookies=cookies)

            self.soup = BeautifulSoup(self.response.content, 'html.parser')
            self.request = self.response.request
        print(
            f'\033[32mBeep boop ! sekarang anda berada di {self.response.url}\33[0m')

    def _construct_login_data(self):
        ''' Method untuk membangun data login '''
        if self.soup is not None:
            token_tag = self.soup.select(
                'input[name="__RequestVerificationToken"]')[0]['value']
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
