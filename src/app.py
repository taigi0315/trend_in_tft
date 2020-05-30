import pymongo
from pymongo import MongoClient

from builder.builder import TFTDataBuilder

if __name__ == "__main__":
    db_client = MongoClient('localhost', 27017)
    db = db_client['match_data']

    DataBuilder = TFTDataBuilder(db)

    DataBuilder.get_match_data_from_db()
    DataBuilder.build_all_df()
    DataBuilder.build_winner_loser_df()
    
    print(f"match_data length: {len(DataBuilder.match_data)}")
    
    DataBuilder.units_df.to_csv('dataframe/units_df.csv')
    DataBuilder.items_df.to_csv('dataframe/items_df.csv')
    DataBuilder.traits_df.to_csv('dataframe/traits_df.csv')
