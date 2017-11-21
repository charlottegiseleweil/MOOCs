
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.1** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# In[3]:

import pandas as pd
import numpy as np
from scipy.stats import ttest_ind


# # Assignment 4 - Hypothesis Testing
# This assignment requires more individual learning than previous assignments - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.
# 
# Definitions:
# * A _quarter_ is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
# * A _recession_ is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
# * A _recession bottom_ is the quarter within a recession which had the lowest GDP.
# * A _university town_ is a city which has a high percentage of university students compared to the total population of the city.
# 
# **Hypothesis**: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (`price_ratio=quarter_before_recession/recession_bottom`)
# 
# The following data files are available for this assignment:
# * From the [Zillow research data site](http://www.zillow.com/research/data/) there is housing data for the United States. In particular the datafile for [all homes at a city level](http://files.zillowstatic.com/research/public/City/City_Zhvi_AllHomes.csv), ```City_Zhvi_AllHomes.csv```, has median home sale prices at a fine grained level.
# * From the Wikipedia page on college towns is a list of [university towns in the United States](https://en.wikipedia.org/wiki/List_of_college_towns#College_towns_in_the_United_States) which has been copy and pasted into the file ```university_towns.txt```.
# * From Bureau of Economic Analysis, US Department of Commerce, the [GDP over time](http://www.bea.gov/national/index.htm#gdp) of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file ```gdplev.xls```. For this assignment, only look at GDP data from the first quarter of 2000 onward.
# 
# Each function in this assignment below is worth 10%, with the exception of ```run_ttest()```, which is worth 50%.

# In[6]:

# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}


# In[4]:

def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list.'''
    
    #Load data
    univ_towns = pd.read_csv('university_towns.txt',error_bad_lines=False,header=None)
    univ_towns.columns = ['RegionName']
    
    #Clean data
    univ_towns['IsState'] = univ_towns['RegionName'].str.contains('\[edit\]')
    for i in range (0,len(univ_towns)):     #New column 'State' based on Names with [edit]
        if univ_towns.iloc[i]['IsState']:
            univ_towns.set_value(i, 'State', univ_towns.iloc[i]['RegionName'])
        else:
            univ_towns.set_value(i, 'State', univ_towns.iloc[i-1]['State'])

    univ_towns = univ_towns[univ_towns['IsState']==False][['State','RegionName']]
    univ_towns = univ_towns.replace({'\[.*\]':''},regex=True)
    univ_towns['RegionName'] = univ_towns['RegionName'].replace({' \(.*\)':''},regex=True)
    return univ_towns

get_list_of_university_towns()


# In[6]:

def get_GDP():
    '''Load and clean GDP data'''
    
    #Load data
    GDPraw = pd.read_excel('gdplev.xls',header=4)
    GDP = GDPraw[['Unnamed: 4','GDP in billions of chained 2009 dollars.1']]
    
    #Clean data
    GDP = GDP.dropna()
    GDP = GDP[GDP['Unnamed: 4'].str.match('2.*')]
    GDP.columns = ['quarter','GDP']
    GDP = GDP.set_index('quarter')
    
    return GDP

get_GDP()


# In[9]:

def get_recession_start():
    '''Identify recession start (two consecutive quarters of GDP decline)'''
    
    GDP = get_GDP()  
    
    for j in range(0,len(GDP)-2):
        if (GDP.iloc[j].GDP > GDP.iloc[j+1].GDP) & (GDP.iloc[j+1].GDP > GDP.iloc[j+2].GDP):
            recession_start = GDP.iloc[j].name
            break
    
    return recession_start


# In[11]:

def get_recession_end():
    '''Identify recession end (two consecutive quarters of GDP growth)'''
    
    GDP = get_GDP()  
    
    for j in range(GDP.index.get_loc(get_recession_start()),len(GDP)):
        if (GDP.iloc[j].GDP > GDP.iloc[j-1].GDP) & (GDP.iloc[j-1].GDP > GDP.iloc[j-2].GDP):
            recession_end = GDP.iloc[j].name
            break
    
    return recession_end


# In[12]:

def get_recession_bottom():
    '''Recession bottom is the quarter within a recession which had the lowest GDP'''

    GDP = get_GDP()  
    years_in_recession = []
    
    for j in range(GDP.index.get_loc(get_recession_start()),GDP.index.get_loc(get_recession_end())+1):
        years_in_recession.append(GDP.iloc[j].GDP)
    
    return GDP[GDP['GDP'] == min(years_in_recession)].index.tolist()[0]


# In[60]:

import re

def convert_housing_data_to_quarters():
    
    #Load data
    housing_raw = pd.read_csv('City_Zhvi_AllHomes.csv', header=0)

    #My computationally expensive version for changing to quarters
    #yrs = []
    #for x in range(2000,2017):
    #    for i in range (0,4):
    #        yrs.append(x)
    #    x +=1 
    #quarters = []    
    #for i in range(0,len(yrs)):
    #    q = str(yrs[i]) + 'q' + str(i%4+1)
    #    quarters.append(q)
    #
    #for i in range(0,len(quarters)):   
    #    def make_quarters(row):
    #        if re.search('q1',quarters[i]):
    #            data = row[[(str(yrs[i])+'-01'),(str(yrs[i])+'-02'),(str(yrs[i])+'-03')]]
    #        if re.search('q2',quarters[i]):
    #            data = row[[(str(yrs[i])+'-04'),(str(yrs[i])+'-05'),(str(yrs[i])+'-06')]]
    #        if re.search('q3',quarters[i]):
    #            data = row[[(str(yrs[i])+'-07'),(str(yrs[i])+'-08'),(str(yrs[i])+'-09')]]
    #        if re.search('q4',quarters[i]):
    #            data = row[[(str(yrs[i])+'-10'),(str(yrs[i])+'-11'),(str(yrs[i])+'-12')]]
    #        return pd.Series({quarters[i]: np.mean(data)})
    #    housing[quarters[i]] = housing_raw.apply(make_quarters, axis=1)

    #List of all columns names from 2000-1 to 2016-8
    months = [] 
    for i in housing_raw.columns:
        if re.search('20',i):
            months.append(i)
            
    #Re-sample housing_raw to quarters    
    df_toresample = housing_raw[months]
    df_toresample.columns = pd.to_datetime(df_toresample.columns)
    housing = df_toresample.resample('Q',axis=1).mean() 
    
    housing.columns = housing.columns.to_series().apply(lambda datetime: '{:}q{:}'.format(datetime.year,datetime.quarter))
    
    housing[['State','RegionName']] = housing_raw[['State','RegionName']]
    for i in range(0,len(housing)):         #States names according the 'states' dictionary
        housing.set_value(i,'State',states[housing.iloc[i]['State']])
    housing = housing.set_index(['State','RegionName'])

    #returns it as mean values in df: col: 2000q1>2016q3,  multi-index ["State","RegionName"]
    #The resulting dataframe should have 67 columns, and 10,730 rows.

    return housing


# In[ ]:

def get_recession_start_before():
    '''Identify quarter before recession '''
    GDP = get_GDP()  
    
    for j in range(0,len(GDP)-2):
        if (GDP.iloc[j].GDP > GDP.iloc[j+1].GDP) & (GDP.iloc[j+1].GDP > GDP.iloc[j+2].GDP):
            recession_before = GDP.iloc[j-1].name
            break
    
    return recession_before

def run_ttest():
    '''TTest comparing the univ town ratio values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind().'''
    
    '''The value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    
    
    #Create df, using univ_towns and housing with bool colmn if univ town
    univ_towns = get_list_of_university_towns()
    housing = convert_housing_data_to_quarters()
    qbottom = get_recession_bottom()
    qbefore = get_recession_start_before()
    
    univ_towns['Univ town'] = True

    housing_price = housing[[qbefore,qbottom]]
    housing_price['ratio']=housing[qbefore]/housing[qbottom]
        
    df = pd.merge(univ_towns, housing_price, how='right', left_on=['State','RegionName'], right_index=True)
    df['Univ town'] = df['Univ town'].fillna(False)
    df = df.dropna()
    
    ttest = ttest_ind(df[df['Univ town']]['ratio'], df[df['Univ town']==False]['ratio']) 
    
    different = 0
    if ttest.pvalue > 0.01:
        different = False
    if ttest.pvalue < 0.01:
        different = True
        
    better = 0
    if df[df['Univ town']]['ratio'].mean() < df[df['Univ town']==False]['ratio'].mean():
        better = "university town"
    if df[df['Univ town']==False]['ratio'].mean() < df[df['Univ town']]['ratio'].mean():
        better = "non-university town"
    
    return (different,ttest.pvalue,better)

run_ttest()


# In[ ]:



