import requests
from bs4 import BeautifulSoup


class Robot:
    base_url = 'https://simak.ipb.ac.id/'
    authenticated = False

    def __init__(self, username, password):
        ''' Inisiasi Robot penelusur '''
        self.username = username
        self.password = password
        self.request = None
        self.response = None
        self.soup = None
        print(f'\033[32mBeep boop ! robot untuk {username} siap\33[0m')

    def login(self, method='GET'):
        ''' Method untuk request ke login page'''
        url = self.base_url + 'Account/Login'
        if method == 'POST':
            url += '?ReturnUrl=%2FHome'
            data = self._construct_login_data()
            self._do_request(url, method, data)
        else:
            self._do_request(url, method)

    def list_sidebar(self):
        ''' Method melihat menu pada sidebar '''
        if self.authenticated == False:
            raise RuntimeError("\033[31mBzzz bzzz ! anda belum login\33[0m")

    def _do_request(self, url='', method='GET', data={}):
        ''' Method untuk membuat request '''
        cookies = {}
        if self.response is not None:
            for cookie in self.response.cookies:
                cookies[cookie.name] = cookie.value

        print(f"Mencoba melakukan {method} ke alamat : {url}")
        with requests.Session() as sess:
            if method == 'POST':
                self.response = sess.post(url, data=data, cookies=cookies)
                if self.response.status_code == 200 and self.response.url.count("/Home"):
                    print("\033[32mBeep boop ! berhasil login\33[0m")
                    self.authenticated = True
                else:
                    print("\033[31mBzzz bzzz ! sepertinya gagal login\33[0m")
            else:
                self.response = sess.get(url, cookies=cookies)

        self.soup = BeautifulSoup(self.response.content, 'html.parser')
        self.request = self.response.request

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
