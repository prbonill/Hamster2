
# coding: utf-8

# In[1]:


# Scenarios: Metodo para generara escenarios
# Parametros:
# - source(string): Path del archivo de origen de informacion
# - separator(string): Delimitador de columnas
# - name(string): Nombre del escenario
# - unit(char): Medida, puede ser s: segundos, m: minutos, h: horas o d:dias
# - elapse(int): Cantidad de horas, minutos o seguntos transcurridos
# - quantity(int): Cantidad de medidas hacia atras a obtener
# - variables(arreglo de strings): Variables a medir

#BEGIN*****************************************************************************************************
import pandas as pd
import numpy as np


def Scenarios(source,separator,name, unit, elapse, quantity, variables):
    #Craga del dataframe data mediante lectura del archivo de origen
    data=pd.read_csv(source,sep=separator)
    #Dataframe donde se almacenara el resultado final
    dft = pd.DataFrame() 
    #Recorrer el listado de variables ingresadas
    for i in range(0,len(variables)):
        #Variable actual con la que se trabajara
        variable=variables[i]
        #Sumatoria de la variable especificada agrupada por segundos
        def seconds(var):
            df1=data.groupby(["anio","mes","dia", "hora","minutos","segundos"],as_index=False) [var].sum()
            df2=df1[["anio","mes","dia", "hora","minutos","segundos",var]]
            df2[var]=df1.groupby(np.arange(len(df1)) // elapse)[var].cumsum()
            return df2.iloc[(elapse-1):(-1*elapse):elapse]
        #Sumatoria de la variable especificada agrupada por minutos
        def minutes(var):
            df1=data.groupby(["anio","mes","dia", "hora","minutos"],as_index=False) [var].sum()
            df2=df1[["anio","mes","dia", "hora","minutos",var]]
            df2[var]=df1.groupby(np.arange(len(df1)) // elapse)[var].cumsum()
            return df2.iloc[(elapse-1):(-1*elapse):elapse]
        #Sumatoria de la variable especificada agrupada por horas
        def hours(var):
            df1=data.groupby(["anio","mes","dia", "hora"],as_index=False) [var].sum()
            df2=df1[["anio","mes","dia", "hora",var]]
            df2[var]=df1.groupby(np.arange(len(df1)) // elapse)[var].cumsum()
            return df2.iloc[(elapse-1):(-1*elapse):elapse]
        #Sumatoria de la variable especificada agrupada por dias
        def days(var):
            df1=data.groupby(["anio","mes","dia"],as_index=False) [var].sum()
            df2=df1[["anio","mes","dia",var]]
            df2[var]=df1.groupby(np.arange(len(df1)) // elapse)[var].cumsum()
            return df2.iloc[(elapse-1):(-1*elapse):elapse]
        #Sumatoria de la variable especificada agrupada por meses
        def months(var):
            df1=data.groupby(["anio","mes"],as_index=False) [var].sum()
            df2=df1[["anio","mes",var]]
            df2[var]=df1.groupby(np.arange(len(df1)) // elapse)[var].cumsum()
            return df2.iloc[(elapse-1):(-1*elapse):elapse]
        #Sumatoria de la variable especificada agrupada por años
        def years(var):
            df1=data.groupby(["anio"],as_index=False) [var].sum()
            df2=df1[["anio",var]]
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
    dft.to_csv("C:\\Users\\ADMIN\Documents\\Proyecto Modelo de Datos\\Scenarios\\"+name+".txt",sep=separator)        

#END*****************************************************************************************************    


# In[2]:



#Llamada a la funcion de generacion de escenarios
# Path del archivo de origen de informacion
path="C:\\Users\\ADMIN\Documents\\Proyecto Modelo de Datos\\HAMSTER.txt"
# Delimitador de columnas
sep="\t"
# Nombre del escenario
name="escenario_prueba"
# Unidad de medida, puede ser s: segundos, m: minutos, h: horas o d:dias
unit="m"
# Lapso de tiempo
elapse=15
# Cantidad de medidas hacia atras a obtener
quantity=5
# Variables a calcular, puede ser Sensor1 , Sensor2 o ambos
var=("Sensor1",)
Scenarios(path,sep,name, unit, elapse, quantity,var)

