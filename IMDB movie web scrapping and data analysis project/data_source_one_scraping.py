#!/usr/bin/env python
# coding: utf-8

# In[14]:


import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
import warnings
warnings.filterwarnings('ignore')


# In[ ]:





# In[15]:


##using web scraping, to get all top 250 movies in IMDB beautifulsoup in text form.
url="https://www.imdb.com/chart/top?ref_=nv_mv_250"
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')


# In[16]:


##get every top 250 movie's hyperlink
top_movie_link = []
for i in soup.find_all('a',href=True):
    top_movie_link.append(i.get('href'))
top_250 = []
for i in top_movie_link:
    if i is not None and i.startswith('/title/tt'):
        top_250.append('https://www.imdb.com'+i.strip())
## select unique movie hyperlink list
top_250 = top_250[0:len(top_250):2]


# In[17]:


import numpy as np
## for loops in here means that I need to scrape every movie's features, which should corresponding to my dataframe columns
def get_imdb_dataset():
    ## create a empty dataframe first with following features
    features = ['ranking among 250','movie name', 'url link','IMDB rating score','highest rating score','number of rating','number of audience(thousands)',
                    'movie type','movie length','movie genre','movie released date','stars','gross worldwide profit',
                    'number of production company','Budget(thousands in unit)','profits in USA','movie description']
    df = pd.DataFrame(columns=features)
    
    for i in np.arange(0, len(top_250)):
        ranking = i+1
        URL = top_250[i]
        R = requests.get(URL)
        Soup = BeautifulSoup(R.text, 'html.parser')
        ##getting movie_name, imdb rating scores, highest rating score, number of audience and people who score this movie.
        movie_name=(Soup.find("div",{"class":"title_wrapper"}).get_text(strip=True).split('|')[0]).split('(')[0]
        rating_score = Soup.find("span",{"itemprop":"ratingValue"}).text
        best_rating = Soup.find("span",{"itemprop":"bestRating"}).text
        rating_count = Soup.find("span",{"itemprop":"ratingCount"}).text.replace(',','')
        review_count = Soup.find("span",{"itemprop":"reviewCount"}).text[:3].replace(',','')
        movie_more_info= Soup.find("div",{"class":"subtext"}).get_text(strip=True).split('|')
        ## some movies missing movie type, if so, elements in movie_more_info equal 3 and execute second if statement, otherwises,
        ## elements in movie_more_info equal 4(contains movie_type), execute first if statement
        if len(movie_more_info)==4:
            movie_type = movie_more_info[0]
            movie_length = movie_more_info[1]
            movie_genre = movie_more_info[2]
            movie_date = movie_more_info[3]
        if len(movie_more_info)<4:
            movie_type = 'No type recorded'
            movie_length = movie_more_info[0]
            movie_genre = movie_more_info[1]
            movie_date = movie_more_info[2]
        ## find a list which contains movie's director, writers, stars information
        episode_containers = Soup.find_all('div', class_='credit_summary_item')
        director_writer_star = ['Director','Writers','Stars']
        def director_writer_star_info(ele):
            info = ''
            for i in episode_containers:
                ## in find_all('a'), the first element is movie's director information
                if ele == 'Director':
                    director = [x.text for x in episode_containers[0].find_all('a')]
                    for dire in range(len(director)-1):
                        info += director[dire]+','
                ## in find_all('a'), the second element is movie's director information
                if ele == 'Writers':
                    Writers = [x.text for x in episode_containers[1].find_all('a')]
                    for w in range(len(Writers)-1):
                        info += Writers[w]+','
                ## in find_all('a'), the third element is movie's director information,I only need to know three most famous stars
                if ele == 'Stars':
                    Stars = [x.text for x in episode_containers[2].find_all('a')][:3]
                    for s in range(len(Stars)-1):
                        info += Stars[s]+','
            return info
        ## get directors, writers, stars info to from above function
        directors = director_writer_star_info('Director')
        writers = director_writer_star_info('Writers')
        stars = director_writer_star_info('Stars')       


        required_tags = ['Budget', 'Opening Weekend USA', 'Gross USA','Cumulative Worldwide Gross']
        ## find a list which contains movie's 'Budget', 'Opening Weekend USA', 'Gross USA',
        ##'Cumulative Worldwide Gross' information
        main_containers = Soup.find_all('div', class_='txt-block')

        def getValue(tag):
            result = ''
            ##format for extracting 'Budget', 'Opening Weekend USA', 'Gross USA' are same. They are all in 'attribute'
            ##class.
            for element in main_containers:
                if tag!='Production Co' and tag in str(element):
                ## extracting 'Budget', 'Opening Weekend USA', 'Gross USA' from main_containers
                    try:
                        result += str(element).replace(" ", "").split('$')[1].split('<')[0].strip()
                        extra = [x.text for x in element.find_all('span',class_='attribute')]
                        if len(extra) > 0:
                            result += " "+ extra[0]
                    ## if indexerror happens, just ignore it and append none to result
                    except IndexError:
                        result += ''

                ## the way to extract 'production company' is to get text form in find_all('a'), which hides all company info    
                if tag == 'Production Co':
                    try:
                        if 'Production Co' in str(element):
                            prodco = [x.text for x in element.find_all('a')]
                            for prod in range(len(prodco) -1):
                                result += prodco[prod] + ", "
                    ## if indexerror happens, just ignore it and append none to result
                    except IndexError:
                        result += ''

            return result
        ## get movie budget, gross_usa, gross_wide, number of production company from getValue function
        budget = getValue('Budget')[:6]
        gross_usa = getValue('Gross USA')
        gross_worldwide = getValue('Cumulative Worldwide Gross')
        production_co = getValue('Production Co')
        number_production_co = len(production_co)


        ##extract movie_description information.
        movie_description=Soup.find("div",{"class":"summary_text"}).get_text(strip=True).strip()
        ##append all above movies' feature to dataframe.
        feature_dicts = {
            'ranking among 250':ranking,
            'movie name':movie_name,
            'url link':URL,
            'IMDB rating score':rating_score,
            'highest rating score':best_rating,
            'number of rating':rating_count,
            'number of audience(thousands)':review_count,
            'movie type':movie_type,
            'movie length':movie_length,
            'movie genre':movie_genre,
            'movie released date':movie_date,
            'stars':stars,
            'gross worldwide profit':gross_worldwide,
            'number of production company':number_production_co,
            'Budget(thousands in unit)':budget,
            'profits in USA':gross_usa,
            'movie description':movie_description             
            }
        

        df = df.append(pd.DataFrame.from_records([feature_dicts],columns=feature_dicts.keys()))
        
        
        df=df[features]
        
    
    df['profits in USA']=df['profits in USA'].str.replace(',','')# removing comma from column data
    df['profits in USA'] = pd.to_numeric(df['profits in USA'])
    df['profits in USA'].fillna(df['profits in USA'].median(), inplace=True)
    df['Budget(thousands in unit)']=df['Budget(thousands in unit)'].str.replace(',','')# removing comma from column data
    df['Budget(thousands in unit)'] = pd.to_numeric(df['Budget(thousands in unit)'])
    df['Budget(thousands in unit)'].fillna(df['Budget(thousands in unit)'].median(), inplace=True) # find out median value then replace with 'nan'
    df['gross worldwide profit']=df['gross worldwide profit'].str.replace(',','')# removing comma from column data
    df['gross worldwide profit'] = pd.to_numeric(df['gross worldwide profit'])
    df['gross worldwide profit'].fillna(df['gross worldwide profit'].median(), inplace=True) # find out median value then replace with 'nan'
    #df=df.set_index(['ranking among 250'], drop=True)
    return df
    
    
    
 
            
    
                
        
    
    
   
     
        
    
    
    
    
    
    
    
    
    
 


# In[18]:


def get_imdb_dataset_gradeflag():
    ## create a empty dataframe first with following features
    features = ['ranking among 250','movie name', 'url link','IMDB rating score','highest rating score','number of rating','number of audience(thousands)',
                    'movie type','movie length','movie genre','movie released date','stars','gross worldwide profit',
                    'number of production company','Budget(thousands in unit)','profits in USA','movie description']
    df = pd.DataFrame(columns=features)
    ##GET MAXIMUM OF 3 CALLS
    for i in np.arange(0, 3):
        ranking = i+1
        URL = top_250[i]
        R = requests.get(URL)
        Soup = BeautifulSoup(R.text, 'html.parser')
        ##getting movie_name, imdb rating scores, highest rating score, number of audience and people who score this movie.
        movie_name=(Soup.find("div",{"class":"title_wrapper"}).get_text(strip=True).split('|')[0]).split('(')[0]
        rating_score = Soup.find("span",{"itemprop":"ratingValue"}).text
        best_rating = Soup.find("span",{"itemprop":"bestRating"}).text
        rating_count = Soup.find("span",{"itemprop":"ratingCount"}).text.replace(',','')
        review_count = Soup.find("span",{"itemprop":"reviewCount"}).text[:3].replace(',','')
        movie_more_info= Soup.find("div",{"class":"subtext"}).get_text(strip=True).split('|')
        ## some movies missing movie type, if so, elements in movie_more_info equal 3 and execute second if statement, otherwises,
        ## elements in movie_more_info equal 4(contains movie_type), execute first if statement
        if len(movie_more_info)==4:
            movie_type = movie_more_info[0]
            movie_length = movie_more_info[1]
            movie_genre = movie_more_info[2]
            movie_date = movie_more_info[3]
        if len(movie_more_info)<4:
            movie_type = 'No type recorded'
            movie_length = movie_more_info[0]
            movie_genre = movie_more_info[1]
            movie_date = movie_more_info[2]
        ## find a list which contains movie's director, writers, stars information
        episode_containers = Soup.find_all('div', class_='credit_summary_item')
        director_writer_star = ['Director','Writers','Stars']
        def director_writer_star_info(ele):
            info = ''
            for i in episode_containers:
                ## in find_all('a'), the first element is movie's director information
                if ele == 'Director':
                    director = [x.text for x in episode_containers[0].find_all('a')]
                    for dire in range(len(director)-1):
                        info += director[dire]+','
                ## in find_all('a'), the second element is movie's director information
                if ele == 'Writers':
                    Writers = [x.text for x in episode_containers[1].find_all('a')]
                    for w in range(len(Writers)-1):
                        info += Writers[w]+','
                ## in find_all('a'), the third element is movie's director information,I only need to know three most famous stars
                if ele == 'Stars':
                    Stars = [x.text for x in episode_containers[2].find_all('a')][:3]
                    for s in range(len(Stars)-1):
                        info += Stars[s]+','
            return info
        ## get directors, writers, stars info to from above function
        directors = director_writer_star_info('Director')
        writers = director_writer_star_info('Writers')
        stars = director_writer_star_info('Stars')       


        required_tags = ['Budget', 'Opening Weekend USA', 'Gross USA','Cumulative Worldwide Gross']
        ## find a list which contains movie's 'Budget', 'Opening Weekend USA', 'Gross USA',
        ##'Cumulative Worldwide Gross' information
        main_containers = Soup.find_all('div', class_='txt-block')

        def getValue(tag):
            result = ''
            ##format for extracting 'Budget', 'Opening Weekend USA', 'Gross USA' are same. They are all in 'attribute'
            ##class.
            for element in main_containers:
                if tag!='Production Co' and tag in str(element):
                ## extracting 'Budget', 'Opening Weekend USA', 'Gross USA' from main_containers
                    try:
                        result += str(element).replace(" ", "").split('$')[1].split('<')[0].strip()
                        extra = [x.text for x in element.find_all('span',class_='attribute')]
                        if len(extra) > 0:
                            result += " "+ extra[0]
                    ## if indexerror happens, just ignore it and append none to result
                    except IndexError:
                        result += ''

                ## the way to extract 'production company' is to get text form in find_all('a'), which hides all company info    
                if tag == 'Production Co':
                    try:
                        if 'Production Co' in str(element):
                            prodco = [x.text for x in element.find_all('a')]
                            for prod in range(len(prodco) -1):
                                result += prodco[prod] + ", "
                    ## if indexerror happens, just ignore it and append none to result
                    except IndexError:
                        result += ''

            return result
        ## get movie budget, gross_usa, gross_wide, number of production company from getValue function
        budget = getValue('Budget')[:6]
        gross_usa = getValue('Gross USA')
        gross_worldwide = getValue('Cumulative Worldwide Gross')
        production_co = getValue('Production Co')
        number_production_co = len(production_co)


        ##extract movie_description information.
        movie_description=Soup.find("div",{"class":"summary_text"}).get_text(strip=True).strip()
        ##append all above movies' feature to dataframe.
        feature_dicts = {
            'ranking among 250':ranking,
            'movie name':movie_name,
            'url link':URL,
            'IMDB rating score':rating_score,
            'highest rating score':best_rating,
            'number of rating':rating_count,
            'number of audience(thousands)':review_count,
            'movie type':movie_type,
            'movie length':movie_length,
            'movie genre':movie_genre,
            'movie released date':movie_date,
            'stars':stars,
            'gross worldwide profit':gross_worldwide,
            'number of production company':number_production_co,
            'Budget(thousands in unit)':budget,
            'profits in USA':gross_usa,
            'movie description':movie_description             
            }
        

        df = df.append(pd.DataFrame.from_records([feature_dicts],columns=feature_dicts.keys()))
        
        
        df=df[features]
        
    
    df['profits in USA']=df['profits in USA'].str.replace(',','')# removing comma from column data
    df['profits in USA'] = pd.to_numeric(df['profits in USA'])
    df['profits in USA'].fillna(df['profits in USA'].median(), inplace=True)
    df['Budget(thousands in unit)']=df['Budget(thousands in unit)'].str.replace(',','')# removing comma from column data
    df['Budget(thousands in unit)'] = pd.to_numeric(df['Budget(thousands in unit)'])
    df['Budget(thousands in unit)'].fillna(df['Budget(thousands in unit)'].median(), inplace=True) # find out median value then replace with 'nan'
    df['gross worldwide profit']=df['gross worldwide profit'].str.replace(',','')# removing comma from column data
    df['gross worldwide profit'] = pd.to_numeric(df['gross worldwide profit'])
    df['gross worldwide profit'].fillna(df['gross worldwide profit'].median(), inplace=True) # find out median value then replace with 'nan'
    #df=df.set_index(['ranking among 250'], drop=True)
    return df


# In[19]:


##generate csv file by using above dataframe
#combined_data = get_imdb_dataset().to_csv('imdb_top_250_movies_raw.csv')
#combined_data


# In[20]:


##generate csv file by using above dataframe
#combined_data_gradeflag = get_imdb_dataset_gradeflag().to_csv('imdb_top_250_movies_raw_gradeflag.csv')
#combined_data_gradeflag


# In[ ]:




