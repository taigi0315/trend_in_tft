def build_trait_df(match_data):
    trait_df = {}
    for match in match_data:
        participants = match['match']['info']['participants']
        for player in participants:
            player_placement = player['placement']
            for index, this_trait in enumerate(player['traits']):
                # Ignore zero tier traits
                if this_trait['tier_current'] != 0:
                    traits_with_tier = f"{this_trait['name']}_{this_trait['tier_current']}"
                    additional_traits = player['traits'].copy()
                    # all_traits - this_trait = other_traits
                    additional_traits.pop(index)

                    # Add placement to each traits in additional_traits                
                    for add_trait in additional_traits:
                        add_trait['placement'] = player_placement

                    if traits_with_tier not in trait_df.keys():
                        trait_df[traits_with_tier] = {
                            "count": 1,
                            "placement": player_placement,
                            "additional_traits": additional_traits
                        }
                    else:
                        trait_df[traits_with_tier]['count'] += 1
                        trait_df[traits_with_tier]['placement'] += player_placement
                        trait_df[traits_with_tier]['additional_traits'] += additional_traits

    
    # Hashing additional_traits
    for trait_name, trait_data in trait_df.items():
        additional_traits_hash = {}
       
        for add_trait in trait_data['additional_traits']:
            # Ignore zero tier traits
            if add_trait['tier_current'] != 0:
                traits_with_tier = f"{add_trait['name']}_{add_trait['tier_current']}"

                if traits_with_tier not in additional_traits_hash.keys():
                    additional_traits_hash[traits_with_tier] = {
                        "count": 1,
                        "placement": add_trait['placement']
                    }
                else:
                    additional_traits_hash[traits_with_tier]['count'] += 1
                    additional_traits_hash[traits_with_tier]['placement'] += add_trait['placement']
            
        
        total_add_traits_count = 0
        for add_trait_data in additional_traits_hash.values():
            total_add_traits_count += add_trait_data['count']

        for add_trait_data in additional_traits_hash.values():
            # Calculate average placement 
            add_trait_data['average_placement'] = add_trait_data['placement'] / add_trait_data['count']
            # Calculate count in percent
            add_trait_data['count(%)'] = add_trait_data['count'] /total_add_traits_count * 100
        
        # Replace additional_trait column with hashed one
        trait_df[trait_name]['additional_traits'] = additional_traits_hash

    
    return trait_df
