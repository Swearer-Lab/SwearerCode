# -*- coding: utf-8 -*-
"""
.srs. to .csv Converter

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
   
    

"edit the name of your file here!"
name = 'FTIR_240713_PtAL2O3_overKBr_CO_100ppm_steadystate300C440nm50bw90mW0000' # Base name for your series, before the number of the split file
i = 0 
i_str = f'{str(i):0>4}'

while os.path.exists(name + i_str +'.spa'):
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
df_csv.to_csv(name + ".csv")

    
