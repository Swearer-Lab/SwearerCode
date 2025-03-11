# -*- coding: utf-8 -*-
"""
.srs to .csv Converter

Loads from a folder with a split Omnic IR series and compiles it into a 
.csv file with the wavenumber on the rows and the time in seconds on the columns
Created on Mon Jul  8 13:59:34 2024

Instructions: 
1. Ensure you're python has been set up according to the sprectrochempy instructions. (Virtual environment is fine)
2. Place py file inside a folder with ONLY the split spa files from the series you want to convert. These should be named like "experiment name" + 0000, 0001, 0002, ...
3. Open your preferred terminal.
4. Navigate to the folder. (usually 'cd (folder you made)')
5. Run 'python spa_to_csv.py'
6. Your folder now contains a csv with all the series data.
@author: JAmie North
"""

'''import numpy as np'''
import pandas as pd
import spectrochempy as scp
import os  
import numpy as np
from tqdm import tqdm   
    

"edit the name of your file here!"
name = 'FTIR_070125_CuPtSiO2_1_700_ERN3_96_CO_500ppm_585_50nm_113mW_200s' # Base name for your series, before the number of the split file
i = 0 
i_str = f'{str(i):0>4}'
while os.path.exists(name + i_str +'.spa'):
    i += 1
    i_str = f'{str(i):0>4}'
i_limit = i
print(i_limit)
i=0
i_str = f'{str(i):0>4}'
for x in tqdm(range(i_limit)):
    spec_slice = scp.read_omnic(name + i_str +'.spa')#Grab data
    #Getting time information from the name of the spectra and converting it into an axis on which to stack the spectra
    #Can currently accomodate s and minute timescales
    spec_slice_name = spec_slice.name
    timename = float(spec_slice.name.replace('Linked spectrum at ','').replace(' min.','').replace(' sec.',''))
    if spec_slice_name[-4:] == "min.":
        timecoord = scp.Coord(data = [timename*60],name = 'Time', units = 's')
    elif spec_slice_name[-4:] == "sec.":
        timecoord = scp.Coord(data = [timename],name = 'Time', units = 's')
    spec_slice.y = timecoord
    if i == 0:
        
        spec_2D = spec_slice
    else:
        spec_2D = scp.concatenate(spec_2D,spec_slice,axis ='y')#Code for stacking the data
    i += 1
    i_str = f'{str(i):0>4}'
spec_2D.name = name


csv = spec_2D.data
df_csv = pd.DataFrame(np.transpose(csv), index = spec_2D.x.data, columns = spec_2D.y.data)
split_val = 10/3 #In seconds
y_bin = 0
n_begin = 0
new_index = 0
df_bin_csv = df_csv.drop(df_csv.columns,axis=1) 
for n,y in enumerate(df_csv.columns):
    
    if y >= split_val*(y_bin+1):
        
        new_columns = split_val*(y_bin+1-0.5)
        srs_new_x = df_csv.iloc[:,n_begin:n]
        for x in srs_new_x.columns:
            if x == new_columns:
                print("oof")
                srs_new_x = srs_new_x.rename(columns ={x:x*1.0001})
                #safe_to_div=False
                print(srs_new_x)
        srs_new_y= np.average(srs_new_x.values, weights=(split_val/abs((srs_new_x.columns)-new_columns)) ,axis=1)
        df_new_y = pd.DataFrame(data = srs_new_y,index = srs_new_x.index, columns =[new_columns] )
        df_bin_csv = pd.concat([df_bin_csv,df_new_y],axis=1) 
        y_bin = y_bin + 1
        n_begin = n
        
new_columns = split_val*(y_bin+1-0.5)       
srs_new_x = df_csv.iloc[:,n_begin:]
for x in srs_new_x.columns:
            if x == new_columns:
                print("oof")
                srs_new_x = srs_new_x.rename(columns ={x:x*1.0001})

srs_new_y= np.average(srs_new_x.values, weights=(split_val/abs((srs_new_x.columns)-new_columns)) ,axis=1)
df_new_y = pd.DataFrame(data = srs_new_y,index = srs_new_x.index, columns =[new_columns] )
df_bin_csv = pd.concat([df_bin_csv,df_new_y],axis = 1)  

    
    
df_bin_csv.to_csv(name +str(round(split_val,2))+"s_split"+ ".csv")




split_val = 20/7 #In seconds
y_bin = 0
n_begin = 0
new_index = 0
df_bin_csv = df_csv.drop(df_csv.columns,axis=1) 
for n,y in enumerate(df_csv.columns):
    
    if y >= split_val*(y_bin+1):
        
        new_columns = split_val*(y_bin+1-0.5)
        srs_new_x = df_csv.iloc[:,n_begin:n]
        for x in srs_new_x.columns:
            if x == new_columns:
                print("oof")
                srs_new_x = srs_new_x.rename(columns ={x:x*1.0001})
                #safe_to_div=False
                print(srs_new_x)
        srs_new_y= np.average(srs_new_x.values, weights=(split_val/abs((srs_new_x.columns)-new_columns)) ,axis=1)
        df_new_y = pd.DataFrame(data = srs_new_y,index = srs_new_x.index, columns =[new_columns] )
        df_bin_csv = pd.concat([df_bin_csv,df_new_y],axis=1) 
        y_bin = y_bin + 1
        n_begin = n
        
new_columns = split_val*(y_bin+1-0.5)       
srs_new_x = df_csv.iloc[:,n_begin:]
for x in srs_new_x.columns:
            if x == new_columns:
                print("oof")
                srs_new_x = srs_new_x.rename(columns ={x:x*1.0001})

srs_new_y= np.average(srs_new_x.values, weights=(split_val/abs((srs_new_x.columns)-new_columns)) ,axis=1)
df_new_y = pd.DataFrame(data = srs_new_y,index = srs_new_x.index, columns =[new_columns] )
df_bin_csv = pd.concat([df_bin_csv,df_new_y],axis = 1)  

    
    
df_bin_csv.to_csv(name +str(round(split_val,2))+"s_split"+ ".csv")






split_val = 5 #In seconds
y_bin = 0
n_begin = 0
new_index = 0
df_bin_csv = df_csv.drop(df_csv.columns,axis=1) 
for n,y in enumerate(df_csv.columns):
    
    if y >= split_val*(y_bin+1):
        
        new_columns = split_val*(y_bin+1-0.5)
        srs_new_x = df_csv.iloc[:,n_begin:n]
        for x in srs_new_x.columns:
            if x == new_columns:
                print("oof")
                srs_new_x = srs_new_x.rename(columns ={x:x*1.0001})
                #safe_to_div=False
                print(srs_new_x)
        srs_new_y= np.average(srs_new_x.values, weights=(split_val/abs((srs_new_x.columns)-new_columns)) ,axis=1)
        df_new_y = pd.DataFrame(data = srs_new_y,index = srs_new_x.index, columns =[new_columns] )
        df_bin_csv = pd.concat([df_bin_csv,df_new_y],axis=1) 
        y_bin = y_bin + 1
        n_begin = n
        
new_columns = split_val*(y_bin+1-0.5)       
srs_new_x = df_csv.iloc[:,n_begin:]
for x in srs_new_x.columns:
            if x == new_columns:
                print("oof")
                srs_new_x = srs_new_x.rename(columns ={x:x*1.0001})

srs_new_y= np.average(srs_new_x.values, weights=(split_val/abs((srs_new_x.columns)-new_columns)) ,axis=1)
df_new_y = pd.DataFrame(data = srs_new_y,index = srs_new_x.index, columns =[new_columns] )
df_bin_csv = pd.concat([df_bin_csv,df_new_y],axis = 1)  

    
    
df_bin_csv.to_csv(name +str(round(split_val,2))+"s_split"+ ".csv")


    
