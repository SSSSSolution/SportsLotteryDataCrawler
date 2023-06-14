import time
import requests
from bs4 import BeautifulSoup
import chardet
import random
import logging
import pickle

def format_percent(percentage_str, n):
    try:
        num = float(percentage_str.rstrip("%"))
    except ValueError:
        return ""
    decimal_str = "{:.{}f}".format(num / 100, n)
    return decimal_str


def save_cookies(cookies, file):
    try:
        with open(file, 'wb') as f:
            pickle.dump(cookies, f)
    except Exception as e:
        logging.warning(f"Failed to save cookies to {file}: {e}")


def load_cookies(file):
    try:
        with open(file, 'rb') as f:
            cookies = pickle.load(f)
            return cookies
    except Exception as e:
        logging.warning(f'Failed to load cookies from {file}: {e}')
        return None


class OkoooDataGetter:
    def __init__(self):
        self.url = 'https://www.okooo.com/jingcai/shengpingfu'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/114.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
                      '*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
        }
        self.session = requests.Session()
        self.cookies_file = 'okooo_cookies.json'

        cookies = load_cookies(self.cookies_file)
        if cookies is not None:
            self.session.cookies = cookies

    def get_teams_name(self, td, data) -> None:
        a_tags = td.find_all('a')
        data['host'] = a_tags[0].get_text()
        data['guest'] = a_tags[1].get_text()


    def get_betfair_index(self, tables, data) -> None:
        trs = tables[1].find_all('tr')
        # print(trs[2].prettify())
        tds = trs[2].find_all('td')
        data['betfair_index_h'] = format_percent(tds[3].get_text(), 4)

        tds = trs[3].find_all('td')
        data['betfair_index_d'] = format_percent(tds[3].get_text(), 4)

        tds = trs[4].find_all('td')
        data['betfair_index_a'] = format_percent(tds[3].get_text(), 4)

    def get_save_rate(self, tables, data) -> None:
        trs = tables[1].find_all('tr')
        # print(trs[2].prettify())
        tds = trs[2].find_all('td')
        data['save_rate_h'] = format_percent(tds[4].get_text(), 4)

        tds = trs[3].find_all('td')
        data['save_rate_d'] = format_percent(tds[4].get_text(), 4)

        tds = trs[4].find_all('td')
        data['save_rate_a'] = format_percent(tds[4].get_text(), 4)


    def get_popularity_rate(self, tables, data) -> None:
        # print(tables[0].prettify())
        trs = tables[0].find_all('tr')

        tds = trs[2].find_all('td')
        data['popularity_rate_h'] = format_percent(tds[12].get_text(), 4)

        tds = trs[3].find_all('td')
        data['popularity_rate_d'] = format_percent(tds[12].get_text(), 4)

        tds = trs[4].find_all('td')
        data['popularity_rate_a'] = format_percent(tds[12].get_text(), 4)


    def get_exchanges_data(self, url, data):
        time.sleep(random.uniform(3, 6))
        response = self.session.get(url, headers=self.headers)
        save_cookies(self.session.cookies, self.cookies_file)
        print(self.session.cookies)
        encoding = chardet.detect(response.content)['encoding']
        response.encoding = encoding
        # print(response.text)

        soup = BeautifulSoup(response.text, 'html.parser')
        tables = soup.find('div', class_='matchboxbg').find_all('table')
        self.get_betfair_index(tables=tables, data=data)
        self.get_save_rate(tables=tables, data=data)
        self.get_popularity_rate(tables=tables, data=data)


    def get_data(self):
        okooo_datas = []
        time.sleep(random.uniform(3, 6))
        response = self.session.get(self.url, headers=self.headers)
        save_cookies(self.session.cookies, self.cookies_file)
        print(self.session.cookies)

        encoding = chardet.detect(response.content)['encoding']
        response.encoding = encoding
        # print(response.text)

        soup = BeautifulSoup(response.text, 'html.parser')

        trs = soup.find('div', id='gametablesend').find_all('tr', isover='1')

        for tr in trs:
            data = {}

            tds = tr.find_all('td')
            league = tds[0].find('a').get_text()
            data['league'] = league
            data['match_num'] = tr['id'][2:]

            match_time = tds[1].find('span', class_='MatchTime').get_text()

            self.get_teams_name(td=tds[2], data=data)

            match_url=tds[2].find('a')['href']
            parts = match_url.rsplit('trends/', 1)
            match_url = 'https:' + parts[0] + 'exchanges/'
            print(f'match_url={match_url}')

            okooo_datas.append(data)
            self.get_exchanges_data(url=match_url, data=data)


        return okooo_datas
