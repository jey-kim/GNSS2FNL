#!/usr/bin/env python
# coding: utf-8

# <img src="GEOS_Logo.pdf" width="500" />

# 
# # Step **3** of **`G2FNL`**: <font color=blue>"ch_date_unr.ipynb"</font>
# #### Oct 2, 2021  <font color=red>(v. 1.0.2)</font>
# ##### Jeonghyeop Kim (jeonghyeop.kim@gmail.com)
# 
# > input files: **`pre_i"`** and **`coordinate_list_full.dat`** \
# > output files: **`newDate_i`** 
# 
# 0. This code is a part of GPS2FNL process (old name was `ch_date_unr.sh`)
# 1. The original code _ch_date_unr.sh_ is extremely slow.
# 2. This new code **100 times faster** than the original code. 
# 3. This new code also adds longitude and latitude information 
# 
# > The date arrays in 'YYMMMDD' with new date arrays in 'YYYYMMDD' format.\
# > This code uses three python modules:
# > - numpy 
# > - datetime 
# > - `pandas` 
# >><font color=red>A tutorial for pandas is available at: </font> [click](https://www.youtube.com/watch?v=e60ItwlZTKM)
# 
# 
# 

# <div class="alert alert-danger">
# Do NOT run this code twice without re-starting the kernel
# </div>

# In[1]:


# 1. import modules
import numpy as np
from datetime import datetime
import pandas as pd
#pd.__version__
import os


# In[2]:


current_dir=os.getcwd()
os.getcwd()


# In[3]:


# 2. read a file for GPS station coordinates
filename = 'coordinate_list_full.dat'
coordi = pd.read_csv(filename,sep=' ',header=None)
coordi.columns = ['lon','lat']


# In[4]:


processing_dir = os.path.join(current_dir, 'data', 'processing')
os.chdir(processing_dir) # cp to processing directory
os.getcwd()


# In[5]:


N=len(coordi)


# In[6]:


# 3-1. YYMMMDD -> YYYYMMDD
# 3-2. Add lon, lat columns

for i in range(0,N): # i in range(0,how many files?)

    inputfile = "pre_"+str(i+1) #input_file = pre_"$i"
    df_input=pd.read_csv(inputfile,sep=' ',header=None)  #read pre_"$i" 
    df_input.columns = ['time','ue','un','uz','se','sn','sz','corr_en','flag'] #columns
    date_old = df_input.time.tolist() # A DataFrame to a list
    date_new = pd.to_datetime(date_old, format='%y%b%d').strftime('%Y%m%d') # convert date format
    df_input.loc[:,'time'] = date_new # replaces with the new date  in YYYYMMDD

    
    lon=coordi.loc[i,['lon']]
    lat=coordi.loc[i,['lat']]

    row_number=len(date_new)
    lon_float=float(lon) # df -> float
    lat_float=float(lat) # df -> float
    lon_vector=lon_float*np.ones((row_number, 1), dtype=np.int32)
    lat_vector=lat_float*np.ones((row_number, 1), dtype=np.int32)
    
    
    df_input.loc[:,'lon'] = lon_vector # add lon vector
    df_input.loc[:,'lat'] = lat_vector # add lat vector
    df_input.loc[:,'flag'] = df_input.loc[:,'flag'] 

    df_input = df_input[['time', 'lon', 'lat', 'ue', 'un', 'uz', 'se', 'sn', 'sz', 'corr_en', 'flag']]
    #Change the order of the columns lon and lat. 
    
    outputfile = "newDate_"+str(i+1) #output file = newDate_i
    df_input.to_csv(outputfile ,header=None, index=None,sep=' ',float_format='%.6f')


# In[ ]:




