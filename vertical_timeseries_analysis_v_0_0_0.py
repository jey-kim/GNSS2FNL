#!/usr/bin/env python
# coding: utf-8

# <img src="Figs/GEOS_Logo.pdf" width="500"/> 

# 
# # Step **11** of **`G2FNL`**: <font color=blue>"vertical_timeseries_analysis.ipynb"</font>
# #### Oct 22, 2021  <font color=red>(v. 0.0.0)</font> 
# ##### Jeonghyeop Kim (jeonghyeop.kim@gmail.com) 
# 
# > input prompts: **`yes`** or **`no`** \
# > input files: **`vertical_analysis_PBO.out`**, **`monthlyAvg_i`**, and **`station_list_full.dat`**\
# > output files: **`elasticOnly_i`** and **`vertical_analysis.out`**
# 
# 
# 0. This code is a part of G2FNL process (Project1: GNSS to FNL)
# 1. This code will analyze the vertical components of each time series data.
# 2. vertical_analysis.out 
# **1stCol=lon**; 
# **2ndCol=lat**;
# **3rdCol=standard1**;
# **4thCol=standard2**;
# **5thCol=standard3**; 
# **6thCol=MaxMonth**
# 
# > standard1 : 0 if vertical position is in max in between May and Oct \
# > standard1 : 1 if vertical position is in max in between Nov and Apr \
# > \
# > standard2 : 0 if the rate of subsidence is larger than -1 during the severe drought between 2012/1 and 12/2016 \
# > standard2 : 1 if the rate of subsidence is less than -1 during the severe drought between 2012/1 and 12/2016 \
# > \
# > standard3 :  standard1 = standard2 = 1 => standard3 = 1 (and then rewrite standard1 = standard2 = 0)
# 
# 
# 

# In[1]:


#import modules
import numpy as np
import pandas as pd
import os


# In[2]:


#check the current dir. 
current_dir=os.getcwd()
os.getcwd()


# In[3]:


station_file = 'station_list_full.dat'
df_stID = pd.read_csv(station_file, header=None)
df_stID.columns = ['stID']
N = len(df_stID)


# In[4]:


# While the user input is not either yes or no, this loop will repeat

while True:      
    print(" > If you are analyzing PBO stations, you can use the previous vertical prosition analysis results.")
    print(" >> If you are analyzing NOTA or all available GNSS data, you can NOT use the previous results.")
    print(" >>> If you use the previous results for NOTA or all stations, it will cause a serious error.")    
    print(" >>>> Do you want to use the previous results? ")
    YESorNO=input(" >>>>> type 'yes' or 'no' :")
    YESorNO=YESorNO.lower()
    
    while YESorNO not in ("yes","no"):
        print("*** Please type 'yes' or 'no' ***")
        YESorNO=input(" type 'yes' or 'no' ")
        YESorNO=YESorNO.lower()
        
    if YESorNO == "no" or YESorNO == "yes":
        break 
        #break the while loop
         

if YESorNO.startswith('y'): 
   
    print(" >>>>>> The previous results will be used to remove some stations affected by 'poroelastic' processes")
    df_vertical_results = pd.read_csv("vertical_analysis_PBO.out", header=None, sep = ' ')
    df_vertical_results.columns = ['lon','lat','standard1','standard2','standard3','MaxMonth']
    bad_stations = df_vertical_results[(df_vertical_results['standard1']==1) | (df_vertical_results['standard2']==1) | (df_vertical_results['standard3']==1)]
    idx_bad_stations=bad_stations.index.values
    idx_bad_stations=idx_bad_stations.tolist()
    
    #save vertical_analysis.out here
    df_vertical_results.to_csv('vertical_analysis.out',header=None,index=None ,float_format='%g', sep=' ')
    
    
# NO!
else: 
    
    print(" >>>>>> A new vertical position analysis will be performed to distinguish and remove stations affected by 'poroelastic' processes")
    # NOT available this method now. It will be updated later. 
    
    ## PERFORM THE VERTICAL POSITION ANALYSIS HERE.
    
    
    
    
    #save vertical_analysis.out here


# In[5]:


#cd to processing directory
processing_dir = os.path.join(current_dir, 'data', 'processing')
os.chdir(processing_dir) # cp to processing directory
os.getcwd()


# In[7]:


for i in range(N):
    input_filename = "monthlyAvg_"+str(i+1)
    df_input = pd.read_csv(input_filename, header=None, sep = ' ')
    if i in idx_bad_stations:
        df_input[:] = 0.0 # Remove the data from stations affected by "poroelastic" processes.
    output_filename = "elasticOnly_"+str(i+1)
    df_input.to_csv(output_filename, header=None,index=None ,float_format='%.6f', sep=' ')


# In[ ]:




