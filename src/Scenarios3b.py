import pandas as pd
import numpy as np
import os

def Scenarios(source,separator,name, unit, elapse, quantity, variables):
    path=os.getcwd()
    data=pd.read_csv(path+"\\"+source,sep=separator)
    dft = pd.DataFrame() 
    group=gunit(unit) 
    for i in range(0,len(variables)):
        variable=variables[i]
        df1=data.groupby(group,as_index=False) [variable].sum()
        df1[variable]=df1.groupby(np.arange(len(df1)) // elapse)[variable].cumsum()
        #df2=df1.iloc[(elapse-1):(-1*elapse):elapse]
        df1[variable+"-"+str(elapse)+unit] = df1[variable].shift()
        for j in range(2,quantity):
            df1[variable+"-"+str(elapse*j)+unit] = df1[variable+"-"+str(elapse*(j-1))+unit].shift()
        if i==0:
            dft=df1
        else:
            frames=[dft,df1]
            dft=pd.merge(dft,df1)
    print(dft.head(5))
    dft.to_csv(path+"\\Scenarios\\"+name+".txt",sep=separator)