import time
from datetime import date

import pymongo
from pymongo import MongoClient

from analyser.analyser import TFTDataAnalyser
from builder.builder import TFTDataBuilder


def get_match_data_between_dates(db, start_date, end_date, region='na1'):
    unix_start_date = int(time.mktime(date.fromisoformat(str(start_date)).timetuple())*1000)
    unix_end_date = int(time.mktime(date.fromisoformat(str(end_date)).timetuple())*1000)
    regx = "^" + region.upper()

    match_data = db.collection.find({
            '_id': {'$regex':regx},
            'match.info.game_datetime': {"$gte": unix_start_date, "$lte": unix_end_date}
    })

    return list(match_data)


if __name__ == "__main__":
    db_client = MongoClient('localhost', 27017)
    db = db_client['match_data']
    region = 'na1'
    start_date = '2020-05-30'
    end_date = '2020-05-31'

    # Collector collect data 
    data = get_match_data_between_dates(db, start_date, end_date, region='na1')
    print(f"match_data length: {len(data)}")

    # Builder create DataFrame
    DataBuilder = TFTDataBuilder(
        start_date=start_date,
        end_date=end_date,
        region=region,
        match_data=data
    )
    
    # All Units
    DataBuilder.build_units_dataframe(save=True)
    TFTDataAnalyser = TFTDataAnalyser(db)
    TFTDataAnalyser.default_units_plot(units_df=DataBuilder.units_df)

    # Winner/Loser Units
    DataBuilder.build_winner_loser_dataframe(save=True)  
    TFTDataAnalyser.win_lose_units_plot(
        win_units_df=DataBuilder.winner_units_df,
        lose_units_df=DataBuilder.loser_units_df
    )
    
    # ALl Items
    DataBuilder.build_items_dataframe(save=True)
    TFTDataAnalyser.default_items_plot(DataBuilder.items_df)

# Get list of name for each cost and save it under set3 
