import pprint

import pymongo
from pymongo import MongoClient

from item_df import build_item_df
from trait_df import build_trait_df
from unit_df import build_unit_df
from utils.helper import split_match_data_win_lose

class TFTDataBuilder:
    def __init__(self, db, region='na1'):
        self.region=region
        self.match_data = None

    def get_match_data_from_db(self, region='na1'):
        regx = "^" + region.upper()
        match_data = list(db.collection.find( {'_id': {'$regex':regx} }))
        
        self.match_data = match_data
    
    def build_all_df(self):
        self.unit_df = build_unit_df(self.match_data)
        self.item_df = build_item_df(self.unit_df['Item'])
        self.trait_df = build_trait_df(self.match_data)
    
    def build_winner_loser_df(self):
        winner_match_data, loser_match_data = split_match_data_win_lose(self.match_data)
        # Build unit_df for winner & loser
        self.winner_unit_df = build_unit_df(winner_match_data)
        self.loser_unit_df = build_unit_df(loser_match_data)
        
        # Build item_df for winner & loser
        self.winner_item_df = build_item_df(self.winner_unit_df['Item'])
        self.loser_item_df = build_item_df(self.loser_unit_df['Item'])

        # Build trait_df for winner & loser
        
    


if __name__ == "__main__":
    db_client = MongoClient('localhost', 27017)
    db = db_client['match_data']

    DataBuilder = TFTDataBuilder(db)

    DataBuilder.get_match_data_from_db()
    DataBuilder.build_all_df()
    #DataBuilder.build_winner_loser_df()

    pp = pprint.PrettyPrinter(indent=2)
    # print(DataBuilder.unit_df)
    # print(DataBuilder.item_df)
    pp.pprint(DataBuilder.trait_df['Set3_Void_1'])
    # print(DataBuilder.winner_item_df)
