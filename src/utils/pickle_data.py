import pickle

def pickle_data(data, file_name):

    print(f"Pickling Data\n File: {file_name}")
    try:    
        output_file = open(file_name, "wb")
        pickle.dump(data, output_file)
        output_file.close()
    except:
        print('Exception While Pickling')
