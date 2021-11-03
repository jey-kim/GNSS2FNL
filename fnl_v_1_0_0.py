#!/usr/bin/env python
# coding: utf-8

# <img src="Figs/GEOS_Logo.pdf" width="500" />

# 
# # Step **13** of **`G2FNL`**: <font color=blue>"fnl.ipynb"</font>
# #### Oct 23, 2021  <font color=red>(v. 1.0.0)</font>
# ##### Jeonghyeop Kim (jeonghyeop.kim@gmail.com)
# 
# > input files: **`displacement_i`**, **`displacement_time_label.dat`** and **`station_list_full.dat`** \
# > output files: **`fnl_i.dat`** : preprocessed `final` GNSS data
# 
# 0. This code is a part of GPS2FNL process.
# 1. It will generate fnl_i.dat where i in the number of months with displacements
# 2. Before this code, each of *_i files has time series data for each station. 
# 3. After this code, each fnl_i.dat file has 4-mo (or 6-mo) displacements for a month
# 

# <div class="alert alert-danger">
# Do NOT run this code twice without re-starting the kernel
# </div>

# In[1]:


# 1. import modules
import numpy as np
import pandas as pd
import os


# In[2]:


current_dir=os.getcwd()
os.getcwd()


# In[3]:


# Read a 'time_vector.dat' and get a label 
filename = 'displacement_time_label.dat'
time_vec = pd.read_csv(filename,sep=' ',header=None)
N_month = len(time_vec)

list_full = "station_list_full.dat"
df_list=pd.read_csv(list_full, header=None)
df_list.columns = ['stID']
N_list = len(df_list) 


# In[4]:


processing_dir = os.path.join(current_dir, 'data', 'processing')
os.chdir(processing_dir) # cp to processing directory
os.getcwd()


# In[6]:



for n in range(N_month): #N_month
    array_frame = np.zeros((N_list,8))
    
    
    for i in range(N_list): #N_list:
        inputfile = "displacement_"+str(i+1) #input_file = displacement_"$i"
        df_input=pd.read_csv(inputfile,sep=' ',header=None)  
        df_input.columns = ['lon','lat','ue','un','se','sn','corr_en','flag'] #columns
 
        array_frame[i,:]=df_input.loc[n,:]
    
    
    df_save = pd.DataFrame(array_frame)
    df_save.columns = ['lon','lat','ue','un','se','sn','corr','flag']
    df_save['flag2'] = np.ones((len(df_save),1))*int(20000)
    df_save=df_save[['lon','lat','ue','un','se','sn','corr','flag2','flag']]
    df_save=df_save[(df_save['ue']!=0) & (df_save['un']!=0)]
    df_save['corr']=df_save['corr']/10
    df_save=df_save.reset_index(drop=True)
    savefile = "fnl_"+str(n+1)+".dat" #output file = fnl_"$n".dat
    df_save.to_csv(savefile ,header=None, index=None ,float_format='%g', sep=' ')         

      
    


# In[ ]:




