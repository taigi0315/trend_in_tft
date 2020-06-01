import pymongo
from pymongo import MongoClient

from builder.builder import TFTDataBuilder
from analyser.analyser import TFTDataAnalyser

def get_match_data_from_db(db, region='na1'):
    regx = "^" + region.upper()
    # match_data = list(db.collection.find( {'_id': {'$regex':regx} }))
    # match_data = match_data[:10]
    test_data_ids = ["NA1_3436887139", "NA1_3436855922"]
    match_data = list(db.collection.find({'_id': {'$in': test_data_ids }}))
    return match_data

if __name__ == "__main__":
    db_client = MongoClient('localhost', 27017)
    db = db_client['match_data']

    #Collector collects the data 
    match_data = get_match_data_from_db(db)
    DataBuilder = TFTDataBuilder(match_data=match_data)
    DataBuilder.build_all_df()
    #DataBuilder.build_winner_loser_df()
    
    print(f"match_data length: {len(DataBuilder.match_data)}")
    
    DataBuilder.units_df.to_csv('experiments/dataframe/units_df.csv')
    DataBuilder.items_df.to_csv('experiments/dataframe/items_df.csv')
    #DataBuilder.traits_df.to_csv('experiments/dataframe/traits_df.csv')

    TFTDataAnalyser = TFTDataAnalyser(db)
    #FIx this to read from file
    TFTDataAnalyser.plot_all_units_graph(units_df=DataBuilder.units_df)
  
  
# Get list of name for each cost and save it under set3 