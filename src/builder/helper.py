import copy

def split_match_data_win_lose(match_data):
    """
    Split match data into winner and lower group
    Arguments:
        match_data(List)
    Returns:
        winner_match_list(List): list of match data with winner participants
        loser_match_list(List): list of match data with loser participants
    """
    winner_match_list = []
    loser_match_list = []
    
    for match in match_data:
        win_match = copy.deepcopy(match)
        lose_match = copy.deepcopy(match)
        # Empty out the participants
        win_match['match']['info']['participants'] = []
        lose_match['match']['info']['participants'] = []
        
        participants = match['match']['info']['participants']
        for player in participants:
            # Remove winnder/loser from copied match data
            if player['placement'] > 4:
                lose_match['match']['info']['participants'].append(player)
            else:
                win_match['match']['info']['participants'].append(player)

        winner_match_list.append(win_match)
        loser_match_list.append(lose_match)
    return [winner_match_list, loser_match_list]

