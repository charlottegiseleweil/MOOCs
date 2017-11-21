def answer_one():
    
    maximum = max(df['Gold'])
    return df[df['Gold']>= maximum].index[0]

answer_one()



def answer_two():
    
    biggest_diff = max(df['Gold']-df['Gold.1'])
    return df[(df['Gold']-df['Gold.1'])>= biggest_diff].index[0]

answer_two()




def answer_three():
    
    
    #Only include countries that have won at least 1 gold in both summer and winter.
    df2 = df[(df['Gold']>0) & (df['Gold.1']>0)]
    
    #biggest difference 
    biggest_diff = max( (df2['Gold']-df2['Gold.1'])/df2['Gold.2']  )
    return df2[((df2['Gold']-df2['Gold.1'])/df2['Gold.2'])>= biggest_diff].index[0]


answer_three()





def answer_four():
    Points = df[['Gold.2','Silver.2','Bronze.2']]
    Points['Gold.2'] *=3
    Points['Silver.2'] *=2
    Points['Pts']=Points['Gold.2']+Points['Silver.2']+Points['Bronze.2']
    Points.drop(['Gold.2','Silver.2','Bronze.2'], axis=1, inplace=True)
    return Points

answer_four()



def answer_five():
    Counties = census_df[['SUMLEV','STNAME','CTYNAME']]
    Counties = Counties[Counties['SUMLEV']==50]
    Counties.drop('SUMLEV',axis=1,inplace=True)
    
    #Counties_per_state = Counties_per_state.set_index(['STNAME', 'CTYNAME'])
    #Group by and count
    df_Cty_per_St = pd.DataFrame(Counties.groupby('STNAME').size().rename('Count'))
    maximum = max(df_Cty_per_St['Count'])
    
    return  df_Cty_per_St[df_Cty_per_St['Count']>=maximum].index[0]

answer_five()



def answer_six():
    
    #Useful columns
    df = census_df[['SUMLEV','STNAME','CTYNAME','CENSUS2010POP']]
    df = df[df['SUMLEV']==50]
    df.drop('SUMLEV',axis=1,inplace=True)
    df['ST'] = df['STNAME']
    df['CTY'] = df['CTYNAME']
    
    #Group by states
    df = df.set_index(['ST','CTY']) #    df_grouped = pd.DataFrame(df.groupby('STNAME')
    
    #Grouped by states, sort counties on population, pick 3 largest, sum
    df = pd.DataFrame(df.groupby('STNAME')['CENSUS2010POP'].apply(lambda grp: grp.nlargest(3).sum()))

    #Sort states on population and keep only top 3
    df = df.sort('CENSUS2010POP',ascending=False).head(3)
    
    #Convert to  list of string values (in order of highest population to lowest population)
    return df.index.tolist()
                 
answer_six()




import numpy as np

def answer_seven():
    
    #Useful columns
    df = census_df[['SUMLEV','STNAME','CTYNAME','POPESTIMATE2010','POPESTIMATE2011','POPESTIMATE2012','POPESTIMATE2013','POPESTIMATE2014','POPESTIMATE2015']]
    df = df[df['SUMLEV']==50]
    df.drop('SUMLEV',axis=1,inplace=True)
        
    df2 = pd.DataFrame(df['CTYNAME'])    
    ###df2['MaxPop'] = np.zeros(len(df2.index))
    ###df2['MinPop'] = np.zeros(len(df2.index))
    df2['Diff'] = np.zeros(len(df2.index))
    
    for index, row in df.iterrows():
        maxi = max(row['POPESTIMATE2010'],row['POPESTIMATE2011'],row['POPESTIMATE2012'],row['POPESTIMATE2013'],row['POPESTIMATE2014'],row['POPESTIMATE2015'])
        mini = min(row['POPESTIMATE2010'],row['POPESTIMATE2011'],row['POPESTIMATE2012'],row['POPESTIMATE2013'],row['POPESTIMATE2014'],row['POPESTIMATE2015'])
        ###df2.set_value(index, 'MaxPop', maxi)
        ###df2.set_value(index, 'MinPop', mini)
        df2.set_value(index, 'Diff', (maxi-mini))
        
    # I can't manage to sort on Diff column :(
    ###df2.sort_values(by='Diff', axis=1, ascending=False)
    
    return df2[df2['Diff']>= max(df2['Diff'])]['CTYNAME'].values[0]
    

answer_seven()




def answer_eight():
    
    #Useful columns
    df = census_df[['SUMLEV','STNAME','CTYNAME','REGION','POPESTIMATE2014','POPESTIMATE2015']]
    df = df[df['SUMLEV']==50]
    df.drop('SUMLEV',axis=1,inplace=True)
    
    #Conditions
    region_condition = ((df['REGION']== 1) | (df['REGION']== 2))
    pop_condition = (df['POPESTIMATE2015']>df['POPESTIMATE2014'])
    query_condition = region_condition & pop_condition
    df = df[query_condition]
    
    #name condition:
    df = df[df['CTYNAME'].str.match("Washington")]
    
    df = df.sort(ascending=True)
    
    df = df.drop(['REGION','POPESTIMATE2014','POPESTIMATE2015'],axis=1)
    return df

answer_eight()