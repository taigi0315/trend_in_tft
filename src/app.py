import pymongo
from pymongo import MongoClient

from builder.builder import TFTDataBuilder
from analyser.analyser import TFTDataAnalyser

if __name__ == "__main__":
    db_client = MongoClient('localhost', 27017)
    db = db_client['match_data']

    DataBuilder = TFTDataBuilder(db)

    DataBuilder.get_match_data_from_db()
    DataBuilder.build_all_df()
    #DataBuilder.build_winner_loser_df()
    
    print(f"match_data length: {len(DataBuilder.match_data)}")
    
    DataBuilder.units_df.to_csv('experiments/dataframe/units_df.csv')
    #DataBuilder.items_df.to_csv('experiments/dataframe/items_df.csv')
    #DataBuilder.traits_df.to_csv('experiments/dataframe/traits_df.csv')

    TFTDataAnalyser = TFTDataAnalyser(db)
    TFTDataAnalyser.plot_units_df(units_df=DataBuilder.units_df)
  
  
# Get list of name for each cost and save it under set3 