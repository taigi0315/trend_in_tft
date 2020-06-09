import time
from datetime import date

import pymongo
from pymongo import MongoClient

from analyser.analyser import TFTDataAnalyser
from builder.builder import TFTDataBuilder

def get_sample_data(db):

    match_data = db.collection.find({})
    return list(match_data[:30])

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
    data = get_sample_data(db)
    # data = get_match_data_between_dates(db, start_date, end_date, region='na1')
    print(f"match_data length: {len(data)}")

    # Builder create DataFrame
    DataBuilder = TFTDataBuilder(
        start_date=start_date,
        end_date=end_date,
        region=region,
        match_data=data
    )
    DataBuilder.build_champion_dataframe()

    # DataBuilder.build_units_dataframe(save=True)
    # # DataBuilder.build_items_dataframe(save=True)
    # DataBuilder.build_units_item_placement_dataframe(save=True) 

    TFTDataAnalyser = TFTDataAnalyser(
        DataBuilder = DataBuilder
    )
    # # TFTDataAnalyser.units_count_tier_plot()
    TFTDataAnalyser.champion_count_placement(DataBuilder.champion_count_placement_df)
    TFTDataAnalyser.champion_count_tier(DataBuilder.champion_count_tier_df)
    TFTDataAnalyser.champion_item_placement(DataBuilder.champion_item_placement_df)
    # # # ALl Items
    # # TFTDataAnalyser.items_plot(items_df = DataBuilder.items_df)
    # TFTDataAnalyser.units_item_placement()
