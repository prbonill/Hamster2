
# Scenarios: Metodo para generara escenarios
# Parametros:
# - source(string): Path del archivo de origen de informacion
# - separator(string): Delimitador de columnas
# - name(string): Nombre del escenario
# - unit(char): Medida, puede ser s: segundos, m: minutos, h: horas o d:dias
# - elapse(int): Cantidad de horas, minutos o seguntos transcurridos
# - quantity(int): Cantidad de medidas hacia atras a obtener
# - variables(arreglo de strings): Variables a medir

import pandas as pd
import numpy as np
import os

def Scenarios(source,separator,name, unit, elapse, quantity, variables):
    #Craga del dataframe data mediante lectura del archivo de origen
    path=os.getcwd()
    data=pd.read_csv(path+"\\"+source,sep=separator)
    
    
    #Dataframe donde se almacenara el resultado final
    dft = pd.DataFrame() 
    #Recorrer el listado de variables ingresadas
    for i in range(0,len(variables)):
        #Variable actual con la que se trabajara
        variable=variables[i]
        #Sumatoria de la variable especificada agrupada por segundos
        def seconds(var):
            group=["anio","mes","dia", "hora","minutos","segundos"]
            df1=data.groupby(group,as_index=False) [var].sum()
            group.append(var)
            df2=df1[group]
            df2[var]=df1.groupby(np.arange(len(df1)) // elapse)[var].cumsum()
            return df2.iloc[(elapse-1):(-1*elapse):elapse]
        #Sumatoria de la variable especificada agrupada por minutos
        def minutes(var):
            group=["anio","mes","dia", "hora","minutos"]
            df1=data.groupby(group,as_index=False) [var].sum()
            group.append(var)
            df2=df1[group]
            df2[var]=df1.groupby(np.arange(len(df1)) // elapse)[var].cumsum()
            return df2.iloc[(elapse-1):(-1*elapse):elapse]
        #Sumatoria de la variable especificada agrupada por horas
        def hours(var):
            group=["anio","mes","dia", "hora"]
            df1=data.groupby(group,as_index=False) [var].sum()
            group.append(var)
            df2=df1[group]
            df2[var]=df1.groupby(np.arange(len(df1)) // elapse)[var].cumsum()
            return df2.iloc[(elapse-1):(-1*elapse):elapse]
        #Sumatoria de la variable especificada agrupada por dias
        def days(var):
            group=["anio","mes","dia"]
            df1=data.groupby(group,as_index=False) [var].sum()
            group.append(var)
            df2=df1[group]
            df2[var]=df1.groupby(np.arange(len(df1)) // elapse)[var].cumsum()
            return df2.iloc[(elapse-1):(-1*elapse):elapse]
        #Sumatoria de la variable especificada agrupada por meses
        def months(var):
            group=["anio","mes"]
            df1=data.groupby(group,as_index=False) [var].sum()
            group.append(var)
            df2=df1[group]
            df2[var]=df1.groupby(np.arange(len(df1)) // elapse)[var].cumsum()
            return df2.iloc[(elapse-1):(-1*elapse):elapse]
        #Sumatoria de la variable especificada agrupada por años
        def years(var):
            group=["anio"]
            df1=data.groupby(group,as_index=False) [var].sum()
            group.append(var)
            df2=df1[group]
            df2[var]=df1.groupby(np.arange(len(df1)) // elapse)[var].cumsum()
            return df2.iloc[(elapse-1):(-1*elapse):elapse]
        #Diccionario de opciones de agrupamiento
        options = {"s":seconds, "m":minutes, "h":hours, "d":days, "M":months, "y":years}
        #Carga del dataframe df3 segun la opicon seleccionada del diccionario de opciones de agrupamiento
        df3 = options[unit](variable)
        #Generacion del primer campo de regrecion
        df3[variable+"-"+str(elapse)+unit] = df3[variable].shift()
        #Generacion del segundo al n(quantity) campo de regrecion
        for j in range(2,quantity):
            df3[variable+"-"+str(elapse*j)+unit] = df3[variable+"-"+str(elapse*(j-1))+unit].shift()
        #Verificamos si es la primera variable
        if i==0:
            #Asignamos resultado para la primera variable al dataframe de resultados vacio
            dft=df3
        else:
            #Para las siguientes varibales combinamos el resultado con el dataframe de resultados 
            #que contiene los resultados de las variables anteriores
            frames=[dft,df3]
            dft=pd.merge(dft,df3)
    #Imprimimos una muestra del resultado en pantalla
    print(dft.head(5))
    #Escritura del archivo del escenario
    dft.to_csv(path+"\\Scenarios\\"+name+".txt",sep=separator)       
