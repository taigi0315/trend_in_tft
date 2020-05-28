def split_match_data_win_and_lose(match_data):
    """
    Split match data into winner and lower group
    Arguments:
        match_data(List)
    Returns:
        winner(List): list of winner participant data
        lower(List): list of loser participant data 
    """
    winner = []
    loser = []
    for match in match_data:
        participants = match['info']['participants']
        for p in participants:
            if p['placement'] >= 4:
                winner.append(p)
            else:
                loser.append(p)
    return [winner, loser]

# winner_match_data, loser_match_data = split_match_data_win_and_lose(sample_data)

# winner_unit_list = get_units_from_player_list(winner_match_data)
# loser_unit_list = get_units_from_player_list(loser_match_data)

# winner_match_hashtable = get_unit_hashtable(winner_unit_list)
# loser_match_hashtable  = get_unit_hashtable(loser_unit_list)

# winner_unit_use_count_tier_item_df = build_unit_use_count_tier_item_df(winner_match_hashtable)
# loser_unit_use_count_tier_item_df = build_unit_use_count_tier_item_df(loser_match_hashtable)