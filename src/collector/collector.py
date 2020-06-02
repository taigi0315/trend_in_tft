import datetime
import json
import time

import pymongo
import requests
from pymongo import MongoClient
#from requests.packages.urllib3.util.retry import Retry
from urllib3.util import Retry

from utils.timeout_http_adapter import TimeoutHTTPAdapter


class TFTMatchDataCollector:
    def __init__(self, db, token=None):
        """
        Arguments:
            db: MongoDB connection
        """
        # token needs to be updated daily
        self.token = token
        self.header = {
            'X-Riot-Token': self.token
        }
        self.db = db
        
        # Pull existing match ids
        self.match_ids_in_db = self.db.collection.find().distinct('_id')
        # Init requests set up
        self.setup_requests()

    def setup_requests(self):
        self.http = requests.Session()
        
        assert_status_hook = lambda response, *args, **kwargs: response.raise_for_status()
        self.http.hooks["response"] = [assert_status_hook]
        
        retries = Retry(total=7, backoff_factor=10, status_forcelist=[429, 500, 502, 503, 504])
        self.http.mount("https://", TimeoutHTTPAdapter(max_retries=retries))


    def get_summoner_names(self, tier='challenger', region='na1'):
        """
        Get list of summoner names in the region
        Arguments:
            region(String)
        Returns: 
            summoner_names(List)
        """
        url = f'https://{region}.api.riotgames.com/tft/league/v1/{tier}'
        res = self.http.get(url, headers=self.header)

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
        res = self.http.get(url, headers=self.header)
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
        for index, name in enumerate(summoner_names):
            if index % 10 == 0 and index != 0:
                print(f'Getting {index}th puu_id...')

            puu_ids.append(self.get_puu_id(name, region))
        
        return puu_ids
    
    def get_user_match_ids(self, puu_id, region='na1', count=20):
        url = f'https://{region}.api.riotgames.com//tft/match/v1/matches/by-puuid/{puu_id}/ids?count={count}'
        res = self.http.get(url, headers=self.header)
    
        return res.json()
    
    def get_match_data(self, match_id, region='americas'):
        url = f'https://americas.api.riotgames.com/tft/match/v1/matches/{match_id}'
        res = self.http.get(url, headers=self.header)
        
        return res.json()
    
    def get_n_matches(self, region='na1', tier='challenger', count=20):
        """
        Get list of match ids with provided conditions
        """
        print(f'Getting summners names\n region:{region} tier: {tier}')
        summoner_names = self.get_summoner_names(tier, region)
        
        print(f'Getting puu_ids for #{len(summoner_names)} summoners')
        puu_ids = self.get_puu_ids(summoner_names, region)

        print(f'Getting match data from #{len(puu_ids)} puu_ids')
        match_ids = []
        for id in puu_ids:
            # TODO - will need to handle region change (na1 -> america)
            match_ids += self.get_user_match_ids(puu_id=id, region='americas', count=count)
        
        # Delete duplicated match ids
        match_ids = list(set(match_ids))
        
        # Delete match ids existing in DB
        match_ids_to_pull = [i for i in match_ids if i not in self.match_ids_in_db]
        
        print(f'Found {len(match_ids_to_pull)} match ids to request')
        
        print("Start requesting match data")
        for index, id in enumerate(match_ids_to_pull):
            # TODO - Region handling
            if index % 10 == 0 and index != 0:
                print(f'Getting {index}th match data...')
            match_data = self.get_match_data(match_id=id)
            try:
                self.db.collection.insert_one({
                    "_id":match_data['metadata']['match_id'],
                    "region":region,
                    "tier":tier,
                    "match": match_data
                })
            except:
                print(f"Exception Storing Data to DB")
            
        print('Data Pulling Done')

if __name__ == "__main__":
    db_client = MongoClient('localhost', 27017)
    db = db_client['match_data']
    token = "RGAPI-dff47123-b41c-4acd-8ea4-f5a59598e2f6"
    MatchDataCollector = TFTMatchDataCollector(db, token)
    MatchDataCollector.get_n_matches(
        region='na1',
        tier='challenger',
        count=300
    )
