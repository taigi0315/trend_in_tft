def split_match_data_win_lose(match_data):
    """
    Split match data into winner and lower group
    Arguments:
        match_data(List)
    Returns:
        winner(List): list of winner participant data
        lower(List): list of loser participant data 
    """
    winner_match = []
    loser_match = []
    
    for match in match_data:
        participants = match['match']['info']['participants']
        loser = []
        for index, p in enumerate(participants):
            # Remove all loser participants from original data
            if p['placement'] > 4:
                loser.append(participants.pop(index))
        
        # Store match data with only winner participants
        winner_match.append(match)
        
        # Replace participants data with lower
        match['match']['info']['participants'] = loser
        # Store match data with only loser participants
        loser_match.append(match)
    
    return [winner_match, loser_match]

