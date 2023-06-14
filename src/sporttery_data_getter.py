import time
import requests
import json
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


class SportteryDataGetter:
    def __init__(self):
        self.webApi = 'https://webapi.sporttery.cn'
        self.curSelectedGame = 'hhad,had'
        self.curSportType = 1
        self.dataChannel = 'c'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/114.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            }
        self.session = requests.Session()
        self.cookies_file = 'sporttery_cookies.json'

        cookies = load_cookies(self.cookies_file)
        if cookies is not None:
            self.session.cookies = cookies

    def get_data(self):
        match_datas = []
        url = self.webApi + '/gateway/jc/football/getMatchCalculatorV1.qry?poolCode=' \
              + self.curSelectedGame + '&channel=' + self.dataChannel
        print(f'url={url}')

        time.sleep(random.uniform(3, 6))
        response = self.session.get(url, headers=self.headers, timeout=20)
        save_cookies(self.session.cookies, self.cookies_file)
        print(self.session.cookies)
        response.raise_for_status()

        json_data = json.loads(response.text)

        for match_list in json_data['value']['matchInfoList']:
            for match in match_list['subMatchList']:
                # print(json.dumps(match, ensure_ascii=False, indent=4))
                match_data = {}
                match_data['match_id'] = match['matchId']
                match_data['match_num'] = str(match['matchNum'])
                match_data['match_date'] = match['matchDate']
                match_data['business_date'] = match['businessDate']
                match_data['match_time'] = match['matchTime']
                match_data['home_team'] = match['homeTeamAbbName']
                match_data['away_team'] = match['awayTeamAbbName']
                match_data['league'] = match['leagueAbbName']
                match_data['had_h'] = match['had']['h']
                match_data['had_d'] = match['had']['d']
                match_data['had_a'] = match['had']['a']
                match_data['hhad_h'] = match['hhad']['h']
                match_data['hhad_d'] = match['hhad']['d']
                match_data['hhad_a'] = match['hhad']['a']
                match_datas.append(match_data)

        self.get_support_rate(match_datas)
        return match_datas

    def get_support_rate(self, match_datas):
        match_ids = [data['match_id'] for data in match_datas]
        match_ids_str = ','.join(str(match_id) for match_id in match_ids)
        print(f'match_ids={match_ids_str}')

        url = self.webApi + '/gateway/jc/common/getSupportRateV1.qry?matchIds=' + match_ids_str \
              + '&poolCode=hhad,had&sportType=' + str(self.curSportType)
        print(f'url={url}')

        time.sleep(random.uniform(3, 6))
        response = self.session.get(url, headers=self.headers, timeout=20)
        save_cookies(self.session.cookies, self.cookies_file)
        print(self.session.cookies)
        json_data = json.loads(response.text)

        for match_data in match_datas:
            sr_data = json_data['value']['_' + str(match_data['match_id'])]
            match_data['had_hsr'] = format_percent(sr_data['HAD']['hSupportRate'], 4)
            match_data['had_dsr'] = format_percent(sr_data['HAD']['dSupportRate'], 4)
            match_data['had_asr'] = format_percent(sr_data['HAD']['aSupportRate'], 4)
            match_data['hhad_hsr'] = format_percent(sr_data['HHAD']['hSupportRate'], 4)
            match_data['hhad_dsr'] = format_percent(sr_data['HHAD']['dSupportRate'], 4)
            match_data['hhad_asr'] = format_percent(sr_data['HHAD']['aSupportRate'], 4)
