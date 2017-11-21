
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.5** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# # Assignment 3 - More Pandas
# This assignment requires more individual learning then the last one did - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.

# ### Question 1 (20%)
# Load the energy data from the file `Energy Indicators.xls`, which is a list of indicators of [energy supply and renewable electricity production](Energy%20Indicators.xls) from the [United Nations](http://unstats.un.org/unsd/environment/excel_file_tables/2013/Energy%20Indicators.xls) for the year 2013, and should be put into a DataFrame with the variable name of **energy**.
# 
# Keep in mind that this is an Excel file, and not a comma separated values file. Also, make sure to exclude the footer and header information from the datafile. The first two columns are unneccessary, so you should get rid of them, and you should change the column labels so that the columns are:
# 
# `['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']`
# 
# Convert `Energy Supply` to gigajoules (there are 1,000,000 gigajoules in a petajoule). For all countries which have missing data (e.g. data with "...") make sure this is reflected as `np.NaN` values.
# 
# Rename the following list of countries (for use in later questions):
# 
# ```"Republic of Korea": "South Korea",
# "United States of America": "United States",
# "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
# "China, Hong Kong Special Administrative Region": "Hong Kong"```
# 
# There are also several countries with numbers and/or parenthesis in their name. Be sure to remove these, 
# 
# e.g. 
# 
# `'Bolivia (Plurinational State of)'` should be `'Bolivia'`, 
# 
# `'Switzerland17'` should be `'Switzerland'`.
# 
# <br>
# 
# Next, load the GDP data from the file `world_bank.csv`, which is a csv containing countries' GDP from 1960 to 2015 from [World Bank](http://data.worldbank.org/indicator/NY.GDP.MKTP.CD). Call this DataFrame **GDP**. 
# 
# Make sure to skip the header, and rename the following list of countries:
# 
# ```"Korea, Rep.": "South Korea", 
# "Iran, Islamic Rep.": "Iran",
# "Hong Kong SAR, China": "Hong Kong"```
# 
# <br>
# 
# Finally, load the [Sciamgo Journal and Country Rank data for Energy Engineering and Power Technology](http://www.scimagojr.com/countryrank.php?category=2102) from the file `scimagojr-3.xlsx`, which ranks countries based on their journal contributions in the aforementioned area. Call this DataFrame **ScimEn**.
# 
# Join the three datasets: GDP, Energy, and ScimEn into a new dataset (using the intersection of country names). Use only the last 10 years (2006-2015) of GDP data and only the top 15 countries by Scimagojr 'Rank' (Rank 1 through 15). 
# 
# The index of this DataFrame should be the name of the country, and the columns should be ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations',
#        'Citations per document', 'H index', 'Energy Supply',
#        'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008',
#        '2009', '2010', '2011', '2012', '2013', '2014', '2015'].
# 
# *This function should return a DataFrame with 20 columns and 15 entries.*

# In[ ]:




# In[82]:

import pandas as pd

def answer_one():
    # load Energy data
    energy = pd.read_excel("Energy Indicators.xls", sheetname='Energy', header=15, skiprows=0, skip_footer=38)
    
    # Clean columns
    energy.columns = ['useless', 'useless2','Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']
    del energy['useless']
    del energy['useless2']
    energy.drop(energy.index[0], inplace=True)
    
    # Convert Energy Supply to gigajoules 
    energy['Energy Supply'] *= 1000000
    
    # Missing data as np.NaN
    energy['Energy Supply'] = pd.to_numeric(energy['Energy Supply'], errors='coerce')
    energy['Energy Supply per Capita'] = pd.to_numeric(energy['Energy Supply per Capita'], errors='coerce')

    #Rename countries 
    energy['Country'] = energy['Country'].replace({'Republic of Korea': 'South Korea'}, regex=True)
    energy['Country'] = energy['Country'].replace({'United Kingdom of Great Britain and Northern Ireland': 'United Kingdom'}, regex=True)
    energy['Country'] = energy['Country'].replace({'United States of America': 'United States'}, regex=True)
    energy['Country'] = energy['Country'].replace({'China, Hong Kong Special Administrative Region': 'Hong Kong'}, regex=True)
    energy['Country'] = energy['Country'].replace({'[0-9]+| \(.+\)': ''}, regex=True)
    
    #load GDP data
    GDP = pd.read_csv('world_bank.csv',header=4)
    
    #Rename countries 
    GDP['Country Name'] = GDP['Country Name'].replace({'Korea, Rep.': 'South Korea'}, regex=True)
    GDP['Country Name'] = GDP['Country Name'].replace({'Iran, Islamic Rep.': 'Iran'}, regex=True)
    GDP['Country Name'] = GDP['Country Name'].replace({'Hong Kong SAR, China': 'Hong Kong'}, regex=True)

    #load SciEn data
    ScimEn = pd.read_excel('scimagojr-3.xlsx')
     
    #Join datasets: GDP(last 10 years only), Energy, and ScimEn(top 15 ranks)
    GDP10y = GDP[['Country Name','Country Code','Indicator Name','Indicator Code','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015']]
    
    merged1 = pd.merge(energy, ScimEn[:15], how='inner', left_on='Country', right_on='Country') 
    merged2 = pd.merge(merged1, GDP10y, how='inner', left_on='Country', right_on='Country Name')
    
    result = merged2.set_index('Country')
    result = result.drop(['Country Name', 'Country Code','Indicator Name', 'Indicator Code'], axis=1)

    return result

answer_one()


# ### Question 2 (6.6%)
# The previous question joined three datasets then reduced this to just the top 15 entries. When you joined the datasets, but before you reduced this to the top 15 items, how many entries did you lose?
# 
# *This function should return a single number.*

# In[83]:

get_ipython().run_cell_magic('HTML', '', '<svg width="800" height="300">\n  <circle cx="150" cy="180" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="blue" />\n  <circle cx="200" cy="100" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="red" />\n  <circle cx="100" cy="100" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="green" />\n  <line x1="150" y1="125" x2="300" y2="150" stroke="black" stroke-width="2" fill="black" stroke-dasharray="5,3"/>\n  <text  x="300" y="165" font-family="Verdana" font-size="35">Everything but this!</text>\n</svg>')


# In[84]:

import pandas as pd

def answer_two():
    
    # load Energy data
    energy = pd.read_excel("Energy Indicators.xls", sheetname='Energy', header=15, skiprows=0, skip_footer=38)
    energy.columns = ['useless', 'useless2','Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']
    del energy['useless']
    del energy['useless2']
    energy.drop(energy.index[0], inplace=True)
    energy['Energy Supply'] *= 1000000
    energy['Energy Supply'] = pd.to_numeric(energy['Energy Supply'], errors='coerce')
    energy['Energy Supply per Capita'] = pd.to_numeric(energy['Energy Supply per Capita'], errors='coerce')
    energy['Country'] = energy['Country'].replace({'Republic of Korea': 'South Korea'}, regex=True)
    energy['Country'] = energy['Country'].replace({'United Kingdom of Great Britain and Northern Ireland': 'United Kingdom'}, regex=True)
    energy['Country'] = energy['Country'].replace({'United States of America': 'United States'}, regex=True)
    energy['Country'] = energy['Country'].replace({'China, Hong Kong Special Administrative Region': 'Hong Kong'}, regex=True)
    energy['Country'] = energy['Country'].replace({'[0-9]+|\(.+\)': ''}, regex=True)
    #load GDP data
    GDP = pd.read_csv('world_bank.csv',header=4)
    GDP['Country Name'] = GDP['Country Name'].replace({'Korea, Rep.': 'South Korea'}, regex=True)
    GDP['Country Name'] = GDP['Country Name'].replace({'Iran, Islamic Rep.': 'Iran'}, regex=True)
    GDP['Country Name'] = GDP['Country Name'].replace({'Hong Kong SAR, China': 'Hong Kong'}, regex=True)
    GDP10y = GDP[['Country Name','Country Code','Indicator Name','Indicator Code','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015']]

    #load SciEn data
    ScimEn = pd.read_excel('scimagojr-3.xlsx')
    
    
    merge_en_GDP = pd.merge(energy, GDP10y, how='inner', left_on='Country', right_on='Country Name')
    merge_en_Sci = pd.merge(energy, ScimEn, how='inner', left_on='Country', right_on='Country') 
    merge_Sci_GDP =pd.merge(ScimEn, GDP10y, how='inner', left_on='Country', right_on='Country Name')
    
    merged_all = pd.merge((pd.merge(energy, ScimEn, how='inner', left_on='Country', right_on='Country')), GDP10y, how='inner', left_on='Country', right_on='Country Name')
    
    return (len(energy) + len(GDP) + len(ScimEn) - len(merge_en_Sci) - len(merge_en_GDP) - len(merge_Sci_GDP))

answer_two()
#len(ScimEn) = 191
    #merge_en_Sci 171
#len(energy) = 227
    #merge_en_GDP 184
#len(GDP) = 264
    #merge_Sci_GDP 161
        #all 160



# <br>
# 
# Answer the following questions in the context of only the top 15 countries by Scimagojr Rank (aka the DataFrame returned by `answer_one()`)

# ### Question 3 (6.6%)
# What is the average GDP over the last 10 years for each country? (exclude missing values from this calculation.)
# 
# *This function should return a Series named `avgGDP` with 15 countries and their average GDP sorted in descending order.*

# In[85]:

import numpy as np
    
def answer_three():
    df = answer_one()
    df = df.drop(['Energy Supply', 'Energy Supply per Capita', '% Renewable', 'Rank','Documents', 'Citable documents', 'Citations', 'Self-citations',
       'Citations per document', 'H index'],axis=1)
    
    def average(row):
        data = row[['2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014','2015']]
        return pd.Series({'avg': np.mean(data)})

    avgGDP = df.apply(average, axis=1)
    avgGDP = avgGDP.sort_values('avg', axis=0, ascending=False)
    
    avgGDP = avgGDP['avg']
    return avgGDP

answer_three()

#How to convert pd.DataFrame to pd.Series ?


# ### Question 4 (6.6%)
# By how much had the GDP changed over the 10 year span for the country with the 6th largest average GDP?
# 
# *This function should return a single number.*

# In[87]:

def answer_four():
    df = answer_one()
    df = df.drop(['Energy Supply', 'Energy Supply per Capita', '% Renewable', 'Rank','Documents', 'Citable documents', 'Citations', 'Self-citations',
       'Citations per document', 'H index'],axis=1)
    
    def average(row):
        data = row[['2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014','2015']]
        return pd.Series({'avg': np.mean(data)})

    avgGDP = df.apply(average, axis=1)
    avgGDP['2006'] = df['2006']
    avgGDP['2015'] = df['2015']
    avgGDP = avgGDP.sort_values('avg', axis=0, ascending=False)

    return abs(avgGDP.iloc[5]['2006'] - avgGDP.iloc[5]['2015'])

answer_four()


# ### Question 5 (6.6%)
# What is the mean `Energy Supply per Capita`?
# 
# *This function should return a single number.*

# In[101]:

def answer_five():
    df = answer_one()

    return np.mean(df['Energy Supply per Capita'])

answer_five()


# ### Question 6 (6.6%)
# What country has the maximum % Renewable and what is the percentage?
# 
# *This function should return a tuple with the name of the country and the percentage.*

# In[91]:

def answer_six():
    df = answer_one()
    df = df.drop(['Energy Supply', 'Energy Supply per Capita','2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014','2015', 'Rank','Documents', 'Citable documents', 'Citations', 'Self-citations',
       'Citations per document', 'H index'],axis=1)
    df = df.sort_values('% Renewable', axis=0, ascending=False)
    df = df.reset_index()
    return tuple(df.iloc[0])

answer_six()


# ### Question 7 (6.6%)
# Create a new column that is the ratio of Self-Citations to Total Citations. 
# What is the maximum value for this new column, and what country has the highest ratio?
# 
# *This function should return a tuple with the name of the country and the ratio.*

# In[92]:

def answer_seven():
    df = answer_one()
    df = df.drop(['Energy Supply', 'Energy Supply per Capita','2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014','2015',
                  'Rank','% Renewable','Citations per document','Documents', 'Citable documents', 'H index'],axis=1)
    
    #df = df.sort_values('% Renewable', axis=0, ascending=False)
    
    df['Ratio']=df['Self-citations']/df['Citations']
    df = df.sort_values('Ratio', axis=0, ascending=False)

    df = df.drop(['Citations','Self-citations'],axis=1)
    df = df.reset_index()

    return tuple(df.iloc[0])

answer_seven()


# ### Question 8 (6.6%)
# 
# Create a column that estimates the population using Energy Supply and Energy Supply per capita. 
# What is the third most populous country according to this estimate?
# 
# *This function should return a single string value.*

# In[129]:

def answer_eight():
    df = answer_one()
    df = df.drop(['2006', '2007', '2008', '2009', '2010','2015','2011', '2012', '2013', '2014','Citations','Self-citations',
                  'Rank','% Renewable','Citations per document','Documents', 'Citable documents', 'H index'],axis=1)
    df['Pop_est']=df['Energy Supply']/df['Energy Supply per Capita']
    df = df.sort_values('Pop_est',axis=0,ascending=False)
    df = df.reset_index()
    
    return df.iloc[2]['Country']

answer_eight()


# ### Question 9 (6.6%)
# Create a column that estimates the number of citable documents per person. 
# What is the correlation between the number of citable documents per capita and the energy supply per capita? Use the `.corr()` method, (Pearson's correlation).
# 
# *This function should return a single number.*
# 
# *(Optional: Use the built-in function `plot9()` to visualize the relationship between Energy Supply per Capita vs. Citable docs per Capita)*

# In[139]:

def answer_nine():
    df = answer_one()
    df = df.drop(['2006', '2007', '2008', '2009', '2010','2015', '2011', '2012', '2013', '2014','Citations','Self-citations',
                  'Rank','% Renewable','Citations per document','Documents','H index'],axis=1)
    df['Population']=df['Energy Supply']/df['Energy Supply per Capita']
    df['Citable doc/capita'] = df['Citable documents']/df['Population']
 
    return df.corr().loc['Citable doc/capita']['Energy Supply per Capita']

answer_nine()


# In[137]:

def plot9():
    import matplotlib as plt
    get_ipython().magic('matplotlib inline')
    
    Top15 = answer_one()
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15['Citable docs per Capita'] = Top15['Citable documents'] / Top15['PopEst']
    Top15.plot(x='Citable docs per Capita', y='Energy Supply per Capita', kind='scatter', xlim=[0, 0.0006])


# In[138]:

#plot9() # Be sure to comment out plot9() before submitting the assignment!


# ### Question 10 (6.6%)
# Create a new column with a 1 if the country's % Renewable value is at or above the median for all countries in the top 15, and a 0 if the country's % Renewable value is below the median.
# 
# *This function should return a series named `HighRenew` whose index is the country name sorted in ascending order of rank.*

# In[181]:

def answer_ten():
    df = answer_one()
    df = df[['% Renewable','Rank']]
    df = df.sort_values('Rank',axis=0,ascending=True)
    
    median = np.median(df['% Renewable'])
    df['Bool'] = df['% Renewable'] >= median
    df = df.drop(['% Renewable','Rank'],axis=1)
    df['Bool'] *=1
    
    HighRenew = df['Bool']

    return HighRenew

answer_ten()


# ### Question 11 (6.6%)
# Use the following dictionary to group the Countries by Continent, then create a dateframe that displays the sample size (the number of countries in each continent bin), and the sum, mean, and std deviation for the estimated population of each country.
# 
# ```python
# ContinentDict  = {'China':'Asia', 
#                   'United States':'North America', 
#                   'Japan':'Asia', 
#                   'United Kingdom':'Europe', 
#                   'Russian Federation':'Europe', 
#                   'Canada':'North America', 
#                   'Germany':'Europe', 
#                   'India':'Asia',
#                   'France':'Europe', 
#                   'South Korea':'Asia', 
#                   'Italy':'Europe', 
#                   'Spain':'Europe', 
#                   'Iran':'Asia',
#                   'Australia':'Australia', 
#                   'Brazil':'South America'}
# ```
# 
# *This function should return a DataFrame with index named Continent `['Asia', 'Australia', 'Europe', 'North America', 'South America']` and columns `['size', 'sum', 'mean', 'std']`*

# In[4]:

import numpy as np 

ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}

def answer_eleven():
    df = answer_one()
    df['Population']=df['Energy Supply']/df['Energy Supply per Capita']
    df = df.drop(['2006', '2007', '2008','Energy Supply per Capita', '2009', '2010','2015', '2011', '2012', '2013', '2014','Citations','Self-citations',
                  'Rank','Energy Supply','Citable documents','% Renewable','Citations per document','Documents','H index'],axis=1)
    df = df.reset_index()

    for i in range(0,len(df)):
        df.set_value(i,'Continent',ContinentDict[df.iloc[i]['Country']])

    #group the Countries by Continent
    output = df.groupby('Continent')['Population'].agg({'size':np.size, 'mean':np.mean, 'sum':np.sum, 'std':np.std})

    return output


answer_eleven()


# ### Question 12 (6.6%)
# Cut % Renewable into 5 bins. Group Top15 by the Continent, as well as these new % Renewable bins. How many countries are in each of these groups?
# 
# *This function should return a __Series__ with a MultiIndex of `Continent`, then the bins for `% Renewable`. Do not include groups with no countries.*

# In[27]:

def answer_twelve():
    df = answer_one()
    df = df.reset_index()
    df = df[['% Renewable', 'Country']]
    
    for i in range(0,len(df)):
        df.set_value(i,'Continent',ContinentDict[df.iloc[i]['Country']])
    df['%Renew bin'] = pd.cut(df['% Renewable'],5)
    
    #group Continent, %Renewbins
    output = df.groupby(['Continent','%Renew bin'])['Country'].agg({'size':np.size})
    
    #Convert df to Series
    s = output['size']
    return s

answer_twelve()


# ### Question 13 (6.6%)
# Convert the Population Estimate series to a string with thousands separator (using commas). Do not round the results.
# 
# e.g. 317615384.61538464 -> 317,615,384.61538464
# 
# *This function should return a Series `PopEst` whose index is the country name and whose values are the population estimate string.*

# In[75]:

def answer_thirteen():
    df = answer_one()
    df['PopEst'] = df['Energy Supply']/df['Energy Supply per Capita']
    df = df['PopEst']
    df = df.apply(str)
    #yo = df.str.extract('([0-9][0-9][0-9]\.)')
    #df = df.replace({yo:'yo.'}, regex=False)

    #df = df.format(number)
    #("{0:,g}"
    #df = df.map('{0:,g}'.format)
    #df = df.apply(str)
    return 123

answer_thirteen()


# ### Optional
# 
# Use the built in function `plot_optional()` to see an example visualization.

# In[60]:

def plot_optional():
    import matplotlib as plt
    get_ipython().magic('matplotlib inline')
    Top15 = answer_one()
    ax = Top15.plot(x='Rank', y='% Renewable', kind='scatter', 
                    c=['#e41a1c','#377eb8','#e41a1c','#4daf4a','#4daf4a','#377eb8','#4daf4a','#e41a1c',
                       '#4daf4a','#e41a1c','#4daf4a','#4daf4a','#e41a1c','#dede00','#ff7f00'], 
                    xticks=range(1,16), s=6*Top15['2014']/10**10, alpha=.75, figsize=[16,6]);

    for i, txt in enumerate(Top15.index):
        ax.annotate(txt, [Top15['Rank'][i], Top15['% Renewable'][i]], ha='center')

    print("This is an example of a visualization that can be created to help understand the data. This is a bubble chart showing % Renewable vs. Rank. The size of the bubble corresponds to the countries' 2014 GDP, and the color corresponds to the continent.")


# In[61]:

#plot_optional() # Be sure to comment out plot_optional() before submitting the assignment!


# In[ ]:



