#!/usr/bin/env python
# coding: utf-8

# <img src="Figs/GEOS_Logo.pdf" width="500"/> 

# 
# # Step **2** of **`G2FNL`**: <font color=blue>"preprocess_data.ipynb"</font>
# #### Oct 2, 2021  <font color=red>(v. 1.0.2)</font> 
# ##### Jeonghyeop Kim (jeonghyeop.kim@gmail.com) 
# 
# 
# > input files: **`GNSS data: STID.txt`** & **`station_list_full.dat`**\
# > output files: **`pre_%d`**
# 
# 0. This code is a part of G2FNL process (Project1: GNSS to FNL)
# 1. This code preprocess the downloaded GNSS position data 
# 
# > **Remove header** \
# > **SAVE the following columns:** 
# > time e n v se sn sv corr(e,n) network 
# 
# <div class="alert alert-danger">
# Do NOT run this code twice without re-starting the kernel
# </div>
# 

# In[1]:


import numpy as np
import pandas as pd
import os 

network_flag = 1
# This is for GNSS network index.
# If you don't jointly invert multiple GNSS networks, 
# This can be any integer. 


# In[2]:


current_dir = os.getcwd()
archive_dir = os.path.join(current_dir,'data', 'archive')
processing_dir = os.path.join(current_dir, 'data', 'processing')
os.getcwd()


# In[3]:


list_file='station_list_full.dat'
df_list=pd.read_csv(list_file ,header=None, names=['Sta'])
os.chdir(processing_dir) # cp to processing directory


# In[5]:


os.getcwd() # make sure you are in 'processing directory'


# In[6]:


os.environ["DATA_PATH"] = archive_dir
get_ipython().system('cp $DATA_PATH/*.txt .')
for index, row in df_list.iterrows():
    
    data_file=row["Sta"]+".txt" # data file name
    output_num=index+1 
    output_name="pre_"+str(output_num) # output file name
    
    #DataFrame does NOT read a header by its default
    df_data=pd.read_csv(data_file, sep=r'(?:,|\s+)', 
                            comment='#', engine='python') 
    
    #SAVE columns 
    df_data=df_data[['YYMMMDD','__east(m)','_north(m)','____up(m)',                  'sig_e(m)','sig_n(m)','sig_u(m)','__corr_en']]
    
    # Add network index
    df_data['flag']=np.array([network_flag] * len(df_data))
    
    
    # SAVE file
    df_data.to_csv(output_name, header=None,                    index=None, sep=' ',float_format='%g')


# In[ ]:




