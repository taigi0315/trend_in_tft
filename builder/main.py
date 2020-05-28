import pymongo
from pymongo import MongoClient
from unit_df import build_unit_df


class TFTDataBuilder:
    def __init__(self, db):
        self.unit_df = build_unit_df(db, region='na1')
        # item_df = build unit df
        # trait_df = build trait df



if __name__ == "__main__":
    db_client = MongoClient('localhost', 27017)
    db = db_client['match_data']

    DataBuilder = TFTDataBuilder(db)
    print(DataBuilder.unit_df['Traits'][0])