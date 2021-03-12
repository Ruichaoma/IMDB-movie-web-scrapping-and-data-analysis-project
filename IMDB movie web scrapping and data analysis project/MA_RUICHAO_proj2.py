#!/usr/bin/env python
# coding: utf-8

# In[4]:


import data_source_one as imdb_dataset
import data_source_two as omdb_dataset
import data_source_three as oscar_award_dataset
#import sys
import pandas as pd
import argparse

def grab_data_remotely():
    imdb_top_250_movies = imdb_dataset.get_imdb_dataset()
    omdb_api = omdb_dataset.get_omdb_movie_dataset()
    oscar_awarded_movie = oscar_award_dataset.get_oscar_award_dataset()
    return [imdb_top_250_movies,omdb_api, oscar_awarded_movie]

def grab_data_remotely_gradeflag():
    imdb_top_250_movies_gradeflag = imdb_dataset.get_imdb_dataset_gradeflag()
    omdb_api_gradeflag = omdb_dataset.get_omdb_movie_dataset_gradeflag()
    oscar_awarded_movie_gradeflag = oscar_award_dataset.get_oscar_award_dataset_gradeflag()
    return [imdb_top_250_movies_gradeflag,omdb_api_gradeflag, oscar_awarded_movie_gradeflag]
    
def grab_data_locally():
    imdb_top_250_movies = pd.read_csv('data/imdb_top_250_movies_raw.csv')    
    omdb_api = pd.read_csv('data/omdb_api_raws.csv')
    oscar_awarded_movie = pd.read_csv('data/oscar_awarded_movie_raws.csv')
    return [imdb_top_250_movies,omdb_api, oscar_awarded_movie]


def process_data(data):
    
    imdb_top_250_movies = data[0]
    omdb_api = data[1]
    oscar_awarded_movie = data[2]
    return [imdb_top_250_movies,omdb_api, oscar_awarded_movie]

def process_data_gradeflag(data):
    
    imdb_top_250_movies_gradeflag = data[0]
    omdb_api_gradeflag = data[1]
    oscar_awarded_movie_gradeflag = data[2]
    return [imdb_top_250_movies_gradeflag,omdb_api_gradeflag, oscar_awarded_movie_gradeflag]

def add_data_to_model(processed_data):
    '''save these data as csv files'''
    processed_data[0].to_csv("imdb_top_250_movies.csv", index=False, sep=',')
    processed_data[1].to_csv("omdb_api.csv", index=False, sep=',')
    processed_data[2].to_csv("oscar_awarded_movie.csv", index=False, sep=',')
    print('Successfully! data have been already stored as csv files in the data sub folder')
    print('There shall be three files totally')
    
def add_data_to_model_gradeflag(processed_data_gradeflag):
    '''save these data as csv files'''
    processed_data_gradeflag[0].to_csv("imdb_top_250_movies_gradeflag.csv", index=False, sep=',')
    processed_data_gradeflag[1].to_csv("omdb_api_gradeflag.csv", index=False, sep=',')
    processed_data_gradeflag[2].to_csv("oscar_awarded_movie_gradeflag.csv", index=False, sep=',')
    print('Successfully! data have been already stored as csv files in the data sub folder')
    print('There shall be three files totally')


def main():
     # Create the argument parser.  The description will print out when you invoke -h or --help
    parser = argparse.ArgumentParser(description="This is our test program")
    # Add an argument:  First, name the argument
    parser.add_argument("--option", 
                        # The "choices" parameter allows us to specify a list of acceptable parameters for our argument
                        choices=['local','remote','gradeflag'], 
                        # This argument is required; normally options with "--" are described as positional options are optional, but we can force it to be required
                        required=True,
                        # You can specify the type as well
                        type=str, 
                        # A help string to print out when you use -h or --help
                        help="An Option to choose!")
    args = parser.parse_args()
   
    mychoice = args.option
    if mychoice =='local':
        data = grab_data_locally()
        data = process_data(data)
        add_data_to_model(data)        
    elif mychoice =='remote':
        data = grab_data_remotely()
        data = process_data(data)
        add_data_to_model(data)
    elif mychoice == 'gradeflag':
        data = grab_data_remotely_gradeflag()
        data = process_data_gradeflag(data)
        add_data_to_model_gradeflag(data)
        
    
    
    
    
    
    
        

    
        

    

if __name__ == '__main__':
    main()
    
    
    
    


# In[ ]:





# In[ ]:




