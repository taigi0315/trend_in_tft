import time
from datetime import date
import os
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
        '_id': {'$regex': regx},
        'match.info.game_datetime': {"$gte": unix_start_date, "$lte": unix_end_date}
    })

    return list(match_data)

def get_file_name_prefix(region, tier, start, end):
    return f"{region}_{tier}_{start}_{end}"


if __name__ == "__main__":
    db_client = MongoClient('localhost', 27017)
    db = db_client['match_data']
    region = 'na1'
    tier = 'challenger'
    start_date = '2020-05-30'
    end_date = '2020-05-31'

    file_name_prefix = get_file_name_prefix(region, tier, start_date, end_date)
    data_save_flag = True
    if data_save_flag:
        if not os.path.exists(f"assets/data/{file_name_prefix}"):
            os.makedirs(f"assets/data/{file_name_prefix}")
            os.makedirs(f"assets/data/{file_name_prefix}/champion_item_placement")
        if not os.path.exists(f"assets/plot/{file_name_prefix}"):
            os.makedirs(f"assets/plot/{file_name_prefix}")


    # data = get_sample_data(db)
    data = get_match_data_between_dates(db, start_date, end_date, region='na1')
    print(f"match_data length: {len(data)}")
#---------------------Builder-------------------------
    # Builder create DataFrame
    DataBuilder = TFTDataBuilder(
        match_data=data,
        file_name_prefix=file_name_prefix,
        save=data_save_flag
    )
    DataBuilder.build_champion_dataframe()

    # DataBuilder.build_units_dataframe(save=True)
    # DataBuilder.build_items_dataframe(save=True)
    # DataBuilder.build_units_item_placement_dataframe(save=True)

#------------------Analyser---------------------------

    TFTDataAnalyser = TFTDataAnalyser(
        DataBuilder = DataBuilder,
        file_name_prefix=file_name_prefix
    )
    # TFTDataAnalyser.units_count_tier_plot()
    TFTDataAnalyser.champion_count_placement(DataBuilder.champion_count_placement_df)
    TFTDataAnalyser.champion_count_tier(DataBuilder.champion_count_tier_df)
    TFTDataAnalyser.champion_item_placement()
    # ALl Items
    # TFTDataAnalyser.items_plot(items_df = DataBuilder.items_df)
    # TFTDataAnalyser.units_item_placement()
