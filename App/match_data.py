import datetime
import json
import time

import requests

from utils import pickle_data


class TFTMatchData:
    def __init__(self):
        self.token = "RGAPI-6e06e1d5-d0fa-40bc-852b-d220405efa2e"
        self.header = {
            'X-Riot-Token': self.token
        }
        self.puu_ids = []
        self.match_ids = []
        self.all_match_data = []
        self.request_counter = 0

    def send_request(self, url):
        retry = 0
        try:
            res = requests.get(url, headers=self.header)
            if res.status_code == 429:
                if retry == 0:
                    time.sleep(1.5)
                    retry = retry + 1
                if retry == 1:
                    print('Request Rate Limit Exceeded Waiting 130 seconds...')
                    time.sleep(130)
                    retry = retry + 1
                else:
                    print(f'Failed Request: {url}')
                    return None
                res = requests.get(url, headers=self.header)

            if res.status_code != 200:
                print(f"Request Failed : {res.status_code}")
                return None
            return res

        except:
            print("Exception while send API request")
            return None
        
    def get_summoner_names(self, tier='challenger', region='na1'):
        """
        Get list of summoner names in the region
        Arguments:
            region(String)
        Returns: 
            summoner_names(List)
        """
        url = f'https://{region}.api.riotgames.com/tft/league/v1/{tier}'
        res = self.send_request(url)
        summoner_names = []
        for summoner in res.json()['entries']:
            summoner_names.append(summoner['summonerName'])
        
        return summoner_names
    
    def get_puu_id(self, summoner_name, region='na1'):
        """
        Get an puuid of id, puuid is required to get match data
        Arguments:
            region(String)
            summoner_name(String)
        Returns:
            puu_id(String)
        """
        url = f'https://{region}.api.riotgames.com/tft/summoner/v1/summoners/by-name/{summoner_name}'
        res = self.send_request(url)
        puu_id = res.json()['puuid']

        return puu_id

    def get_puu_ids(self, summoner_names, region='na1'):
        """
        Get list of puu_id for each with provided list of ids
        Arguments:
            region(String)
            summoner_names(List)
        Returns:
            puu_ids(List): list of puu_ids matching with provided ids
        """
        puu_ids = []
        for name in summoner_names:
            self.puu_ids.append(self.get_puu_id(name, region))
    
    def get_user_match_ids(self, puu_id, region='na1', count=20):
        url = f'https://{region}.api.riotgames.com//tft/match/v1/matches/by-puuid/{puu_id}/ids?count={count}'
        res = self.send_request(url)
    
        return res.json()
    
    def get_match_data(self, match_id, region='americas'):
        url = f'https://americas.api.riotgames.com/tft/match/v1/matches/{match_id}'
        res = self.send_request(url)
        
        return res.json()
    
    def get_n_matches(self, region='na1', tier='challenger', count=20):
        """
        Get list of match ids with provided conditions
        """
        print(f'Getting summners names\n region:{region} tier: {tier}')
        summoner_names = self.get_summoner_names(tier, region)
        print(f'Getting puu_ids for #{len(summoner_names)} summoners')
        self.get_puu_ids(summoner_names, region)

        print(f'Getting match data from #{len(self.puu_ids)} puu_ids')
        for id in self.puu_ids:
            # will need to handle region change (na1 -> america)
            # if region in america -> america .... 
            self.match_ids = list(set(self.match_ids + self.get_user_match_ids(puu_id=id, region='americas', count=count)))

        for id in self.match_ids:
            # Region handling
            self.all_match_data.append(self.get_match_data(match_id=id))
        print('Data Pulling Done')
        print(f'Number of Matches: {len(self.all_match_data)}')
        
        # Store the match ids
        file_name = f"../data/{str(datetime.date.today())}_{tier}_{region}_match_ids.p"
        pickle_data(self.all_match_data, file_name)

        # Store the data
        file_name = f"../data/{str(datetime.date.today())}_{tier}_{region}_match_data.p"
        pickle_data(self.all_match_data, file_name)
