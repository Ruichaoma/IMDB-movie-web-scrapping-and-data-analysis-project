#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import urllib.request 
import numpy as np
from bs4 import BeautifulSoup


# In[2]:




## request for given page
req = urllib.request.Request('https://en.wikipedia.org/wiki/List_of_Academy_Award-winning_films', headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36","X-Requested-With": "XMLHttpRequest"})
page = urllib.request.urlopen(req)
## beatiful soup for given page
soup = BeautifulSoup(page,"html.parser")
## get the html table
table = soup.find("table",{"class":"wikitable"})
## since the table contains colspan,rowspan we will need to process them before initializing them  into dataframe.The following helpers are used for the preprocessing of table html data
def pre_process_table(table):
    """
    INPUT:
        1. table - a bs4 element that contains the desired table: ie <table> ... </table>
    OUTPUT:
        a tuple of: 
            1. rows - a list of table rows ie: list of <tr>...</tr> elements
            2. num_rows - number of rows in the table
            3. num_cols - number of columns in the table


    """
    rows = [x for x in table.find_all('tr')]


    num_rows = len(rows)


    # get an initial column count. Most often, this will be accurate
    num_cols = max([len(x.find_all(['th','td'])) for x in rows])


    # sometimes, the tables also contain multi-colspan headers. This accounts for that:
    header_rows_set = [x.find_all(['th', 'td']) for x in rows if len(x.find_all(['th', 'td']))>num_cols/2]


    num_cols_set = []


    for header_rows in header_rows_set:
        num_cols = 0
        for cell in header_rows:
            row_span, col_span = get_spans(cell)
            num_cols+=len([cell.getText()]*col_span)


        num_cols_set.append(num_cols)


    num_cols = max(num_cols_set)


    return (rows, num_rows, num_cols)



def get_spans(cell):
        """
        INPUT:
            1. cell - a <td>...</td> or <th>...</th> element that contains a table cell entry
        OUTPUT:
            1. a tuple with the cell's row and col spans
        """
        if cell.has_attr('rowspan'):
            rep_row = int(cell.attrs['rowspan'])
        else: # ~cell.has_attr('rowspan'):
            rep_row = 1
        if cell.has_attr('colspan'):
            rep_col = int(cell.attrs['colspan'])
        else: # ~cell.has_attr('colspan'):
            rep_col = 1 


        return (rep_row, rep_col)


def process_rows(rows, num_rows, num_cols):
    """
    INPUT:
        1. rows - a list of table rows ie <tr>...</tr> elements
    OUTPUT:
        1. data - a Pandas dataframe with the html data in it
    """
    data = pd.DataFrame(np.ones((num_rows, num_cols))*np.nan)
    for i, row in enumerate(rows):
        try:
            col_stat = data.iloc[i,:][data.iloc[i,:].isnull()].index[0]
        except IndexError:
            print(i, row)


        for j, cell in enumerate(row.find_all(['td', 'th'])):
            rep_row, rep_col = get_spans(cell)
            while any(data.iloc[i,col_stat:col_stat+rep_col].notnull()):
                col_stat+=1


            data.iloc[i:i+rep_row,col_stat:col_stat+rep_col] = cell.getText()
            if col_stat<data.shape[1]-1:
                col_stat+=rep_col


    return data
## preprocess the html table to get the rows,number of columns,number of rows
def get_oscar_award_dataset():
    rows, num_rows, num_cols = pre_process_table(table)
    ## process each row in table to enter data into dataframe by taking into consideration colspan and rowspan of html table
    df = process_rows(rows, num_rows, num_cols)
    ## set headers
    new_header = df.iloc[0] #grab the first row for the header
    df = df[1:] #take the data less the header row
    df.columns = new_header.replace('\n','', regex=True) #set the header row as the df header
    ## Convert year to float to filter data to get movies between 1966-2019
    df = df.replace('\n','', regex=True)
    df["Year"] =df["Year"].apply(lambda x:x.split("/")[0])
    df["Year"] = pd.to_numeric(df["Year"])
    df= df[(df["Year"]>=1966) & (df["Year"]<=2019)]
    return df


# In[3]:


def get_oscar_award_dataset_gradeflag():
    rows, num_rows, num_cols = pre_process_table(table)
    ## process each row in table to enter data into dataframe by taking into consideration colspan and rowspan of html table
    df = process_rows(rows, num_rows, num_cols)
    ## set headers
    new_header = df.iloc[0] #grab the first row for the header
    df = df[1:] #take the data less the header row
    df.columns = new_header.replace('\n','', regex=True) #set the header row as the df header
    ## Convert year to float to filter data to get movies between 1966-2019
    df = df.replace('\n','', regex=True)
    df["Year"] =df["Year"].apply(lambda x:x.split("/")[0])
    df["Year"] = pd.to_numeric(df["Year"])
    df= df[(df["Year"]>=1966) & (df["Year"]<=2019)]
    ##GRAB MAXIMUM OF 3 DATA IN THIS SOURCE
    df=df[:3]
    return df


# In[4]:


#combined_data = get_oscar_award_dataset().to_csv('oscar_awarded_movie_raws.csv')
#combined_data


# In[5]:


#combined_data_gradeflag = get_oscar_award_dataset_gradeflag().to_csv('oscar_awarded_movie_raws_gradeflag.csv')
#combined_data_gradeflag


# In[ ]:




