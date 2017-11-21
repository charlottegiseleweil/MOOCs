import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd

df = pd.read_csv('data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')
df['Day']=df['Date'].str[-5:]

df = df.set_index(['Date'])
df = df.sort_index()

df2015 = df.tail(13757)
df2015 = df2015.set_index('Day')

df = df[:-13757]
df = df.set_index(['Day'])

gb = df.groupby(df.index)
gbmax = gb.max()
gbmax['Data_Value']=gbmax['Data_Value']/10
gbmin = gb.min()
gbmin['Data_Value']=gbmin['Data_Value']/10

gb2015 = df2015.groupby(df2015.index)
gbmax2015 = gb2015.max()
gbmax2015['Data_Value']=gbmax2015['Data_Value']/10
gbmin2015 = gb2015.min()
gbmin2015['Data_Value']=gbmin2015['Data_Value']/10

gbmaxall = gbmax.join(gbmax2015,rsuffix="_2015")
gbminall = gbmin.join(gbmin2015,rsuffix="_2015")

gbmaxall = gbmaxall.where(gbmaxall['Data_Value_2015']>gbmaxall['Data_Value'])
gbminall = gbminall.where(gbminall['Data_Value_2015']<gbminall['Data_Value'])

plt.figure()
obdates = gbmin.index.tolist()
xn = range(len(obdates))

plt.plot(xn,gbmin['Data_Value'],color="blue",label = "Daily Min")
plt.plot(xn,gbmax['Data_Value'],color="red",label = "Daily Max")
plt.gca().fill_between(xn,gbmin['Data_Value'],gbmax['Data_Value'],facecolor='blue',alpha=.1)

plt.scatter(xn,gbmaxall['Data_Value_2015'],color="purple",label="Daily Max Occurred in 2015")
plt.scatter(xn,gbminall['Data_Value_2015'],color="green",label="Daily Min Occurred in 2015")
plt.xlabel('Month')
plt.ylabel('Temperature (C)')
plt.title("Ann Arbor, MI Temperature Records (2005-2015)")
plt.legend(frameon=False)
plt.box(on=None)

xticklabels=['Jan','Feb','Mar','Apr','May','Jun',"Jul",'Aug',"Sep",'Oct','Nov','Dec']
plt.xticks([15,45,75,105,135,165,195,225,255,285,315,345],xticklabels)