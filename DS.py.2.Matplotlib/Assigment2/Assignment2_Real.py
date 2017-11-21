# encoding: utf-8

import pandas as pd
import numpy as np
import sys

reload(sys)  
sys.setdefaultencoding('UTF8')

#Load data
df = pd.read_csv('e00cfcd1d1d1916abdb064ff551e86ada31b13fa80069b52fa0261ad.csv',sep =",")

    #Remove column ID
del df['ID']

    #Split date into Year and Day-Month
df2 = pd.DataFrame(df.Date.str.split('-',1).tolist(),columns = ['Date_yr','Date_day'])
df['Year']=df2['Date_yr']
df['Day']=df2['Date_day']
del df['Date']
df['Year'] = df['Year'].apply(pd.to_numeric, errors='ignore')

#Pivot table because Need: Days en rows, Years en cols pour pouvir faire les 10years Max et Min
df_pivoted = pd.pivot_table(df, values='Data_Value',index=["Day",'Element'], columns=("Year"))

    # To be able to use the MultiIndex(pivoted table), must reset indexs 
df_pivoted.reset_index(inplace=True)
df_pivoted.set_index(['Day'],inplace=True)

#DF:My final data
DF = pd.DataFrame()
DF['2015Max'] = df_pivoted[2015].groupby(level=0).max()
DF['2015Min'] = df_pivoted[2015].groupby(level=0).min()

del df_pivoted['Element']
del df_pivoted[2015]

df_pivoted['10yMAX']=df_pivoted.max(axis=1)
df_pivoted['10yMIN']=df_pivoted.min(axis=1)
DF['10yMax']=df_pivoted['10yMAX'].groupby(level=0).max()
DF['10yMin']=df_pivoted['10yMIN'].groupby(level=0).min() 

#Keep only 2015 records (i.e when 2015Max > 10yMax)
for i in DF.index:
    if DF.loc[i]['2015Max'] <= DF.loc[i]['10yMax']:        
        DF.loc[i,'2015Max'] = ''
    if DF.loc[i]['2015Min'] >= DF.loc[i]['10yMin']:
        DF.loc[i,'2015Min'] = ''
DF = DF.apply(pd.to_numeric, errors='ignore')

#DF.index to Date
    #Remove Feb 29th
DF = DF.drop(DF.index[59])
DF.index = pd.to_datetime(DF.index,format='%m-%d', errors='coerce')

#Date format appearance !! 
    #from datetime import datetime
    #thedate = datetime.strptime('12-03', '%m-%d')
    #formatted_date = (datetime.strptime('12-03', '%m-%d')).strftime('%d %b')
    #print(formatted_date)

##  ------  ------  ------  ------  ------  ------  ------  ------  ------  ------  ------  ------ 
##  ------  ------  ------  ------   Figure  ------  ------  ------  ------  ------  ------  --
##  ------  ------  ------  ------  ------  ------  ------  ------  ------  ------  ------  ------ 
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

fig = plt.figure(figsize=(20,7))

# --- --- --- --- --- -
# --- LINE PLOT --- ---
# --- --- --- --- --- -

plt.plot(DF.index,DF['10yMax'],'r-',linewidth=1.6)
plt.plot(DF.index,DF['10yMin'],'b-',linewidth=1.6)

ax = plt.gca()
ax.get_lines()[0].set_color("#9b0a0a")
ax.get_lines()[1].set_color("#3366ff")
ax.fill_between(DF.index,DF['10yMin'],DF['10yMax'],facecolor='#a798d3',alpha=0.35)

# --- --- --- --- ---
# --- SCATTERPLOT ---
# --- --- --- --- ---

plt.scatter(DF.index, DF['2015Max'], marker='^',c='purple', label='2015 Max')
plt.scatter(DF.index, DF['2015Min'], marker='v',c='purple', label='2015 Min')

# Aesthetics & labels
plt.xlabel('Days of the year')
plt.ylabel('Temperature extremes 2005-2015 (°F)')
plt.title('Climate Change in Lausanne, Switzerland?',fontsize='xx-large',fontweight='bold')
plt.legend(['Max daily (2005-2014)', 'Min daily (2005-2014)','2015 max higher than avg','2015 min lower than avg'])

ax.spines["top"].set_visible(False)
ax.margins(x=0,y=0)

date_format = mdates.DateFormatter('                         %b') #Okay this is really ugly - oops. (Couldn't get to show only month-15 and not month 1st)
ax.xaxis.set_major_formatter(date_format)

plt.show()
fig.savefig('Assignmt2_Fig.jpg')
