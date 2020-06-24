import requests
from bs4 import BeautifulSoup


class Robot:
    base_url = 'https://simak.ipb.ac.id/'

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
            data = self._constructLoginData()
            print(
                f"Melakukan login ke alamat : {url}\ndengan data sebagai berikut: ")
            print(data)
            self._doRequest(url, method, data)
        else:
            self._doRequest(url, method)

    def _doRequest(self, url='', method='GET', data={}):
        ''' Method untuk membuat request '''
        cookies = {}
        if self.response is not None:
            for cookie in self.response.cookies:
                cookies[cookie.name] = cookie.value

        with requests.Session() as sess:
            if method == 'POST':
                self.response = sess.post(url, data=data, cookies=cookies)
            else:
                self.response = sess.get(url, cookies=cookies)

        self.soup = BeautifulSoup(self.response.content, 'html.parser')
        self.request = self.response.request

    def _constructLoginData(self):
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
                f'\033[31mBzzz bzzz ! hasil soup tidak ditemukan\33[0m')
