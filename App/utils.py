import pickle

def pickle_data(data, file_name):

    print(f"Pickling Data\n File: {file_name}")
    try:    
        output_file = open(file_name, "wb")
        pickle.dump(data, output_file)
        output_file.close()
    except:
        print('Exception While Pickling')


# Example converting game_datetime to readable format
# sample_datetime = '1589564943684'
# your_dt = datetime.datetime.fromtimestamp(int(sample_datetime)/1000)  # using the local timezone
# print(your_dt.strftime("%Y-%m-%d"))