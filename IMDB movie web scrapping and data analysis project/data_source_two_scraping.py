#!/usr/bin/env python
# coding: utf-8

# In[1]:


from IPython import get_ipython
import os
os.system('pip install omdb')


# In[2]:


os.system('pip install omdbapi')


# In[3]:


os.system('pip install IMDbPY')
from imdb import IMDb


# In[4]:


##import GetMovie package
from omdbapi.movie_search import GetMovie


# In[5]:


import pandas as pd
##filter warning
import warnings
warnings.filterwarnings('ignore')


# In[6]:


ia = IMDb()
# getting top 250 movies 
search = ia.get_top250_movies() 
movie_list = []
##append each top 250 movie name to movie_list
for i in range(250): 
    movie_name = search[i]['title']
    movie_list.append(movie_name)


# In[7]:


def get_omdb_movie_dataset():
    ##create new dataframe with following features
    features = ['Ranking among 250','Title','Metascore','Rotten Tomatoes Score','Year','Country','Runtime(min)','Language','Director','Writer','Production Company','Type',
                'Plot']
    df = pd.DataFrame(columns=features)
    title_list = []
    country_list = []
    release_year_list = []
    language_list = []
    metascore_rating_list = []
    rating_list = []
    director_list = []
    writer_list = []
    plot_list = []
    type_list = []
    runtime_list = []
    production_company_list = []
    words = ['Title','Metascore','Year','Country','Runtime','Language','Director','Writer','Production','Type','Plot']
    ##for each movie, extract corresponding 'Title','Metascore','Year',
    ##'Country','Runtime','Language','Production','Type','Plot' by using getMovie package from omdb library wrapper
    for i in range(len(movie_list)):
        movie = GetMovie(title=movie_list[i], api_key='6de2ae04', plot='full')
        title = movie.get_data('Title')
        title_list.append(title)
        metascore_rating = movie.get_data('Metascore')
        metascore_rating_list.append(metascore_rating)
        release_year = movie.get_data('Year')
        release_year_list.append(release_year)    
        country = movie.get_data('Country')
        country_list.append(country)
        runtime = movie.get_data('Runtime')
        runtime_list.append(runtime)
        language = movie.get_data('Language')
        language_list.append(language)
        rating = movie.get_data('Ratings')
        rating_list.append(rating)
        director = movie.get_data('Director')
        director_list.append(director)
        writer = movie.get_data('Writer')
        writer_list.append(writer)
        production_company = movie.get_data('Production')
        production_company_list.append(production_company)
        Type = movie.get_data('Type')
        type_list.append(Type)
        plot = movie.get_data('Plot')
        plot_list.append(plot)

        ## each list constituted by dict which contain features name and corresponding feature value,
        ## below function only extract feature values
        def transform(my_list,word):
            new_value = []
            for x in range(0,len(my_list)):
                Str=my_list[x][word]
                new_value.append(Str) 
            return new_value[i]



        ##rating list contains dict which included imdb rating score, rotten tomatoes score and metascore, we only
        ##need rotten tomato score from rating list by using below function
        def transform_rotten_tomatoes_rating(My_list):
            output_list = []
            for rating in My_list:
                rotten_tomato_value = rating['Ratings'][1]['Value'].replace('%', '')[:2]
                output_list.append(rotten_tomato_value)
            return output_list[i]
        ##apply above two functions to every list
        title_ = transform(title_list,words[0])
        metascore_ = transform(metascore_rating_list,words[1])
        release_year_ = transform(release_year_list,words[2])
        country_ = transform(country_list,words[3])
        runtime_ = transform(runtime_list,words[4])[:3]
        language_ = transform(language_list,words[5])
        director_ = transform(director_list,words[6])
        writer_ = transform(writer_list,words[7])        
        production_company_ = transform(production_company_list,words[8])
        type_ = transform(type_list,words[9])
        plot_ = transform(plot_list,words[10])
        ## if indexerror happens, just ignore it and append none to rotten_tomatoes_score
        try:
            rotten_tomatoes_score = transform_rotten_tomatoes_rating(rating_list)
        except IndexError:
            rotten_tomatoes_score = ''


        ##append all above movies' feature to dataframe.
        feature_dicts = {
            'Ranking among 250':i+1,
            'Title':title_,
            'Metascore':metascore_,
            'Rotten Tomatoes Score':rotten_tomatoes_score,
            'Year':release_year_,
            'Country':country_,
            'Runtime(min)':runtime_,
            'Language':language_,
            'Director':director_,
            'Writer':writer_,
            'Production Company':production_company_,
            'Type':type_,
            'Plot':plot_       
        }

        df = df.append(pd.DataFrame.from_records([feature_dicts],columns=feature_dicts.keys()))
        df=df[features]
        ##using movies ranking as index in dataframe
    df['Metascore']=df['Metascore'].str.replace('N/A','')# removing comma from column data
    df['Metascore'] = pd.to_numeric(df['Metascore'])
    df['Metascore'].fillna(df['Metascore'].median(), inplace=True)
    df['Rotten Tomatoes Score'] = pd.to_numeric(df['Rotten Tomatoes Score'])
    df['Rotten Tomatoes Score'].fillna(df['Rotten Tomatoes Score'].median(), inplace=True)
    #df=df.set_index(['Ranking among 250'], drop=True)    
    return df
    
    
    
    
    
    
    
    
    
    
    
    
    


# In[8]:


def get_omdb_movie_dataset_gradeflag():
    ##create new dataframe with following features
    features = ['Ranking among 250','Title','Metascore','Rotten Tomatoes Score','Year','Country','Runtime(min)','Language','Director','Writer','Production Company','Type',
                'Plot']
    df = pd.DataFrame(columns=features)
    title_list = []
    country_list = []
    release_year_list = []
    language_list = []
    metascore_rating_list = []
    rating_list = []
    director_list = []
    writer_list = []
    plot_list = []
    type_list = []
    runtime_list = []
    production_company_list = []
    words = ['Title','Metascore','Year','Country','Runtime','Language','Director','Writer','Production','Type','Plot']
    ##for each movie, extract corresponding 'Title','Metascore','Year',
    ##'Country','Runtime','Language','Production','Type','Plot' by using getMovie package from omdb library wrapper
    
    
    ##GET MAXIMUM OF 3 CALLS
    for i in range(3):
        movie = GetMovie(title=movie_list[i], api_key='6de2ae04', plot='full')
        title = movie.get_data('Title')
        title_list.append(title)
        metascore_rating = movie.get_data('Metascore')
        metascore_rating_list.append(metascore_rating)
        release_year = movie.get_data('Year')
        release_year_list.append(release_year)    
        country = movie.get_data('Country')
        country_list.append(country)
        runtime = movie.get_data('Runtime')
        runtime_list.append(runtime)
        language = movie.get_data('Language')
        language_list.append(language)
        rating = movie.get_data('Ratings')
        rating_list.append(rating)
        director = movie.get_data('Director')
        director_list.append(director)
        writer = movie.get_data('Writer')
        writer_list.append(writer)
        production_company = movie.get_data('Production')
        production_company_list.append(production_company)
        Type = movie.get_data('Type')
        type_list.append(Type)
        plot = movie.get_data('Plot')
        plot_list.append(plot)

        ## each list constituted by dict which contain features name and corresponding feature value,
        ## below function only extract feature values
        def transform(my_list,word):
            new_value = []
            for x in range(0,len(my_list)):
                Str=my_list[x][word]
                new_value.append(Str) 
            return new_value[i]



        ##rating list contains dict which included imdb rating score, rotten tomatoes score and metascore, we only
        ##need rotten tomato score from rating list by using below function
        def transform_rotten_tomatoes_rating(My_list):
            output_list = []
            for rating in My_list:
                rotten_tomato_value = rating['Ratings'][1]['Value'].replace('%', '')[:2]
                output_list.append(rotten_tomato_value)
            return output_list[i]
        ##apply above two functions to every list
        title_ = transform(title_list,words[0])
        metascore_ = transform(metascore_rating_list,words[1])
        release_year_ = transform(release_year_list,words[2])
        country_ = transform(country_list,words[3])
        runtime_ = transform(runtime_list,words[4])[:3]
        language_ = transform(language_list,words[5])
        director_ = transform(director_list,words[6])
        writer_ = transform(writer_list,words[7])        
        production_company_ = transform(production_company_list,words[8])
        type_ = transform(type_list,words[9])
        plot_ = transform(plot_list,words[10])
        ## if indexerror happens, just ignore it and append none to rotten_tomatoes_score
        try:
            rotten_tomatoes_score = transform_rotten_tomatoes_rating(rating_list)
        except IndexError:
            rotten_tomatoes_score = ''


        ##append all above movies' feature to dataframe.
        feature_dicts = {
            'Ranking among 250':i+1,
            'Title':title_,
            'Metascore':metascore_,
            'Rotten Tomatoes Score':rotten_tomatoes_score,
            'Year':release_year_,
            'Country':country_,
            'Runtime(min)':runtime_,
            'Language':language_,
            'Director':director_,
            'Writer':writer_,
            'Production Company':production_company_,
            'Type':type_,
            'Plot':plot_       
        }

        df = df.append(pd.DataFrame.from_records([feature_dicts],columns=feature_dicts.keys()))
        df=df[features]
        ##using movies ranking as index in dataframe
    df['Metascore']=df['Metascore'].str.replace('N/A','')# removing comma from column data
    df['Metascore'] = pd.to_numeric(df['Metascore'])
    df['Metascore'].fillna(df['Metascore'].median(), inplace=True)
    df['Rotten Tomatoes Score'] = pd.to_numeric(df['Rotten Tomatoes Score'])
    df['Rotten Tomatoes Score'].fillna(df['Rotten Tomatoes Score'].median(), inplace=True)
    #df=df.set_index(['Ranking among 250'], drop=True)    
    return df


# In[9]:


#combined_data = get_omdb_movie_dataset().to_csv('omdb_api_raws.csv')
#combined_data


# In[10]:


#combined_data_gradeflag = get_omdb_movie_dataset_gradeflag().to_csv('omdb_api_raw_gradeflag.csv')
#combined_data_gradeflag


# In[ ]:




