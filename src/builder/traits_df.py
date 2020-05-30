import pandas as pd
from collections import Counter

def get_traits_in_multi_match(multi_match_data):
    traits_list = []
    for match in multi_match_data:
        traits_list += get_traits_in_single_match(match)

    return traits_list


def get_traits_in_single_match(single_match_data):
    """
    Get traits from single match data
    Build ideal trait data structure from the original one
    Arguments:
        single_match_data(Dict): response from Riot API match details
    Returns:
        traits(List): List of trait(Dict)
    Example:
        [{ 'additional_traits': [ {'name': 'Chrono_1', 'placement': 2},
                           {'name': 'Infiltrator_1', 'placement': 2},
                           {'name': 'Set3_Brawler_2', 'placement': 2},
                           {'name': 'Set3_Sorcerer_1', 'placement': 2}],
        'name': 'Set3_Void_1',
        'placement': 2},{ } ... ]
    """
    players = single_match_data['match']['info']['participants']
    traits = []
    for p in players:
        player_placement = p['placement']
        player_traits = p['traits']

        # Delete zero tier traits
        player_traits_with_tier = []
        for trait in player_traits:
            if trait['tier_current'] > 0:
                player_traits_with_tier.append(trait)
        
        # Trim down the Traits data
        player_traits_in_structure = []
        for trait in player_traits_with_tier:
            player_traits_in_structure.append({
                "name": f"{trait['name']}_{trait['tier_current']}",
                "placement": player_placement
            })

        # Convert structure
        """
        Example trait structure
        name: {name_of_trait}_{tier} , Demolitionist_1
        placement: Between 1 and 8
        additional_traits: [List of Other Traits Player Used]
        """
        player_traits_with_additional_traits = []
        for index, trait in enumerate(player_traits_in_structure):
            # Get additional traits
            all_traits = player_traits_in_structure.copy()
            # all_trait - subject_trait = additional_trait
            all_traits.pop(index)
            additional_traits = all_traits
            
            player_traits_with_additional_traits.append({
                'name': trait['name'],
                'placement': trait['placement'],
                'additional_traits': additional_traits
            })

        traits += player_traits_with_additional_traits
    
    return traits


def build_traits_hashtable(traits_list):
    """
    Build traits hashtable
    Arguments:
        traits_list(List): list of all traits used in game
    Returns:
        trait_hash(Dict): 
            Key(String): name of trait
            Value(List): data of each trait
    """
    traits_hash = {}
    for trait in traits_list:
        trait_name = trait['name']
        if trait_name not in traits_hash.keys():
            traits_hash[trait_name] = [trait]
        else:
            traits_hash[trait_name].append(trait)
    
    return traits_hash


def build_additional_traits_hashtable(additional_traits):
    additional_traits_hash = {}
    for add_trait in additional_traits:
        if add_trait['name'] not in additional_traits_hash.keys():
            additional_traits_hash[add_trait['name']] = {
                'count': 1,
                'average_placement': add_trait['placement']
            }

        else:
            additional_traits_hash[add_trait['name']]['count'] += 1
            additional_traits_hash[add_trait['name']]['average_placement'] += add_trait['placement']
    
    # Calculate average placement
    for val in additional_traits_hash.values():
        val['average_placement'] = val['average_placement'] / val['count']

    return additional_traits_hash

def build_traits_df(match_data):
    traits_list = get_traits_in_multi_match(match_data)
    traits_hash = build_traits_hashtable(traits_list)

    traits_df_data = []
    for trait_name, list_of_trait in traits_hash.items():
        placement_list = []
        additional_trait_list = []
        for trait in list_of_trait:
            placement_list.append(trait['placement'])
            additional_trait_list += trait['additional_traits']
        
        traits_placement = dict(Counter(placement_list))
        average_placement = sum(placement_list) / len(list_of_trait)
        traits_df_data.append([trait_name, len(list_of_trait), average_placement, traits_placement,  additional_trait_list])
       
    traits_df = pd.DataFrame(traits_df_data, columns = ['Traits', 'Count', 'Average_Placement', 'Placement_List', 'Additional_Traits']) 
    traits_df['Additional_Traits'] = traits_df.apply(lambda row: build_additional_traits_hashtable(row.Additional_Traits), axis=1)
    
    return traits_df

