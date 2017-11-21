# encoding: utf-8

##  ------  ------  ------  ------  ------  ------  ------  ------  ------  ------  ------  ------ 
##  ------  ------  ------  ------  ------  ------  ------  ------  ------  ------  ------  ------ 
##  ------  ------  ------  ------  ------  ------  ------  ------  ------  ------  ------  ------ 
##  ------  ------  ------  ------   Data loading  ------  ------  ------  ------  ------  ------ 
##  ------  ------  ------  ------  ------  ------  ------  ------  ------  ------  ------  ------ 
##  ------  ------  ------  ------  ------  ------  ------  ------  ------  ------  ------  ------ 
##  ------  ------  ------  ------  ------  ------  ------  ------  ------  ------  ------  ------ 

#!\ Graph is year long of 10 years records! Make cols 2005, 2006... Then take max and make col TMAX(10y) and TMIN(10y)
#>> REMOVE February 29th

import pandas as pd
import sys

reload(sys)  
sys.setdefaultencoding('UTF8')


#Load data
df = pd.read_csv('random_city_assgnmt2.csv',sep ="E", header=None)
df = df.head(300)


#Split first column into: id, date, element, 0 (=day1)
df.rename(columns={0: 'first_col'}, inplace=True)
df['first_col'].replace(to_replace="AG000060390", value='id ', regex=True, inplace=True)
df['first_col'].replace(to_replace="TMAX", value=" TMAX", regex=True, inplace=True)
df['first_col'].replace(to_replace="TMIN", value=" TMIN", regex=True, inplace=True)
df2 = pd.DataFrame(df.first_col.str.split(' ',3).tolist(),columns = ['id','yr_month','element','value'])
df['yr_month'] = df2['yr_month']
df['element'] = df2['element']
df['0'] = df2['value']

#Remove PRCP data and useless columns
df = df[df.element != '']
del df['first_col']
del df[31]

#Date format !! Goal here would be to concatenate les rows qui correspondent chacune a 1 mois, ??????????????
#pour mettre date (days) en index, et TMAX et TMIN comme 2 columns.
#Because galeere, let's just do a month for now: Janvier 1940.

df = df.iloc[[0,1]].transpose()
df.rename(columns={0: 'TMAX',1: 'TMIN'}, inplace=True)

df = df.drop(['yr_month','element'])

#Index +1 et re-order
df['day']= df.index
df['day']=df['day'].astype(int) + 1
df = df.set_index('day')
df = df.sort_index()

#Make temperatures type float (was object)
df = df.apply(pd.to_numeric, errors='ignore')

#TODO TODO TODO TODO TODO Transform to date format

df.index



##  ------  ------  ------  ------  ------  ------  ------  ------  ------  ------  ------  ------ 
##  ------  ------  ------  ------  ------  ------  ------  ------  ------  ------  ------  ------ 
##  ------  ------  ------  ------  ------  ------  ------  ------  ------  ------  ------  ------ 
##  ------  ------  ------  ------   Line Plot  ------  ------  ------  ------  ------  ------  --
##  ------  ------  ------  ------  ------  ------  ------  ------  ------  ------  ------  ------ 
##  ------  ------  ------  ------  ------  ------  ------  ------  ------  ------  ------  ------ 
##  ------  ------  ------  ------  ------  ------  ------  ------  ------  ------  ------  ------ 

##  ------  ------  ------  ------  ------  ------  ------  ------  ------  ------  ------  ------ 
## TODO: 
##				Date format


#%matplotlib notebook
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()

plt.plot(df['TMAX'],'r-',df['TMIN'],'b-',linewidth=2.6)

ax = plt.gca()

ax.get_lines()[0].set_color("#cc0000")
ax.get_lines()[1].set_color("#3366ff")
ax.fill_between(df.index,df['TMIN'],df['TMAX'],facecolor='blue',alpha=0.15)

ax.spines["top"].set_visible(False)
ax.margins(x=0,y=0.09)

plt.xlabel('Time')
plt.ylabel('Temperature extremes 2005-2015 (°F)')
plt.title('Climate Change in Lausanne, Switzerland?')


# --- --- --- --- ---
# --- SCATTERPLOT ---
# --- --- --- --- ---

#Fake data
df['2015']=range(len(df))
df['2015'] *= 7

#Keep only 2015 records (i.e when 2015Max > 10yMax)
df['2015_max_records'] = ""
df['2015_min_records'] = ""
for i in range(1,len(df)+1):
    if df.loc[i]['2015'] > df.loc[i]['TMAX']:        
        df.loc[i,'2015_max_records'] = df.loc[i]['2015']
    if df.loc[i]['2015'] < df.loc[i]['TMIN']:
        df.loc[i,'2015_min_records'] = df.loc[i]['2015']
df = df.apply(pd.to_numeric, errors='ignore')

#Make a scatter

#plt.scatter(df.index, df['2015'], marker='^',c='purple', label='2015 Max')
plt.scatter(df.index, df['2015_max_records'], marker='^',c='purple', label='2015 Max')
plt.scatter(df.index, df['2015_min_records'], marker='v',c='purple', label='2015 Min')
plt.legend(['Max daily (2005-2014)', 'Min daily (2005-2014)','2015 max higher than avg','2015 min lower than avg'])
#plt.legend(loc=2, frameon=False, title='Legend')

plt.show()
print(df)


# ##-------##

# ## Fill avec photo du lac ## 
# #Add Lac Léman
# image= "lac_leman.jpg"

# from matplotlib.path import Path
# from matplotlib.patches import PathPatch
# from matplotlib.offsetbox import OffsetImage, AnnotationBbox

# def img_to_path( fn, path, zoom=0.72, ax = None, **kwargs):
#     if ax==None: ax=plt.gca()
#     kwargs.pop("facecolor", None)
#     im = plt.imread(fn, format='jpg')
#     if type(path) == Path:
#         xmin = path.vertices[:,0].min()
#         ymin = path.vertices[:,1].min()
#         patch = PathPatch(path, facecolor='none', zorder=3, **kwargs)
#     else:
#         patch = path
#         xmin = patch.get_verts()[:,0].min()
#         ymin = patch.get_verts()[:,1].min()

#     ax.add_patch(patch)
#     imagebox = OffsetImage(im, zoom=zoom, clip_path=patch, zorder=-10)
#     boxoffset = np.array(im.shape[:2][::-1])/2.*zoom
#     ab = AnnotationBbox(imagebox, (xmin,ymin), xycoords='data',
#                         xybox=boxoffset, boxcoords="offset points", 
#                         pad=0, frameon=False)
#     ax.add_artist(ab)
    
# path = Path(np.c_[df.index,df['TMAX']],[1]+df['TMAX'])
# img_to_path(image, path, edgecolor="white", lw=4, ax=ax )
# #plt.legend(loc=2, frameon=False, title='Legend')