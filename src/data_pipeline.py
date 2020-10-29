import argparse
import numpy as np
import pandas as pd

#Instantiating a few lists to aid in the parsing of the raw data and then 
# establishing it as a Pandas Dataframe

states = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
        "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois",
        "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland",
        "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana",
        "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York",
        "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania",
        "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah",
        "Vermont", "West Virginia", "Virginia", "Washington", "Wisconsin", "Wyoming"]
abbrev = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "WV", "VA", "WA", "WI", "WY"]
columns = ['state', 'numcol', 'yieldpercol', 'totalprod', 'stocks', 
        'priceperlb', 'prodvalue', 'year']

def clean_raw_data(file, num):
    '''
    Takes in a raw txt file and returns a list of lists breaking down info by state.

    Parameters
    ----------
    file - The filepath to the raw data.

    num - The year of the associated data.

    Returns
    ----------
    year - A list of sublists, each sublist representing the data from a single state.
    '''

    year = open(file, 'r').read()

    punc = ['.', ':', ',']
    for cha in punc:
        year = year.replace(cha, '')
    for state, abb in zip(states, abbrev):
        year = year.replace(state, abb)

    year = year.split('\n')

    for idx in range(len(year)):
        year[idx] = year[idx].split()

    #Had a consistent empty list in the final index after splitting
    year.pop()

    for idx in range(len(year)):
        year[idx][1] = int(year[idx][1]) * 1000
        year[idx][2] = int(year[idx][2])
        year[idx][3] = int(year[idx][3]) * 1000
        year[idx][4] = int(year[idx][4]) * 1000
        year[idx][5] = int(year[idx][5]) / 100
        year[idx][6] = int(year[idx][6]) * 1000
        year[idx].append(num)

    return year

def collate_raw(lst):
    '''
    Takes in any number of raw data text files and merges them into a single 
    Pandas Dataframe using clean_raw_data. Was used for initial cleaning
    now kept here in case of file loss and recreation.

    Parameters
    ----------
    lst - A list of sublist, each sublist containing a file path and 
    associated year as needed by clean_raw_data.

    Return
    ----------
    new - A Pandas Dataframe of all cleaned data.
    '''

    new = []
    for pair in lst:
        new.extend(clean_raw_data(pair[0], pair[1]))
    return pd.DataFrame(new, columns=columns)

def write_csv(original, new, file_path):
    '''
    Combines newly cleaned data  with any pre-existing cleaned data and writes 
    a new csv file of said combination.

    Parameters
    ----------
    original - A file path to a .csv containing any previous data.

    new - A Pandas Dataframe of any newly cleaned data.

    file_path - A filepath to where the newly combined dataframe should be 
        saved as a .csv file.
    '''

    full = pd.concat([original, new], ignore_index=True)
    full.to_csv(file_path, index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Graphing functions')
    parser.add_argument('-d', '--data', type=str, 
        default='/Users/ianhetterich/Desktop/Galvanize/capstones/bee-capstone/data/complete_data.csv', 
        help='The file path to the base dataset')
    parser.add_argument('-n', '--new_data', type=str, 
        help='The file path to the new year of data being added')
    parser.add_argument('-y', '--year', type=int, help='The year being added')
    parser.add_argument('-f', '--final', type=str, 
        help='The filepath to save the new csv')
    args = parser.parse_args()
    old = args.data
    new = args.new_data
    year = args.years
    final = args.final

    addition = clean_raw_data(new, year)
    original = pd.read_csv(old)

    write_csv(original, addition, final)